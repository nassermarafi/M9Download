from flask import Flask, request, render_template, Markup
import markdown
import os

# from requests_toolbelt.adapters import appengine
# appengine.monkeypatch()

app = Flask(__name__)

@app.route("/")
def index():
    content = ""
    with open('readme.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())

@app.route("/m9downloadtool/")
def m9downloadtool():
    content = ""
    with open('m9downloadtool.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('m9downloadtool.html', **locals())

@app.route("/service1/")
def service1():
    content = ""
    with open('service1.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('service1.html', **locals())

@app.route("/service2/")
def service2():
    content = ""
    with open('service2.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('service2.html', **locals())

@app.route("/service3/")
def service3():
    content = ""
    with open('service3.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('service3.html', **locals())

@app.route("/service4/")
def service4():
    content = ""
    with open('service4.md', 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('service4.html', **locals())

# Getting Motions For a Particular LatLon
@app.route('/getMotionFromLatLon', methods=['GET'])
def getMotionFromLatLon():
    # bar = request.args.to_dict()
    Latitude = request.args.get('Latitude')
    Longitude = request.args.get('Longitude')
    Unprocessed = bool(request.args.get('Unprocessed'))
    GetDistanceToRupture = bool(request.args.get('GetDistanceToRupture'))
    ResponseSpectra = bool(request.args.get('ResponseSpectra'))
    SensitivityRuns = bool(request.args.get('SensitivityRuns'))

    import ProcessM9Motion
    # Find Closest Site Code
    StationName, DistanceToClosestSite = ProcessM9Motion.FindClosestStationNameToLatLon(Latitude, Longitude)

    # Get Motion
    import json
    Motions = ProcessM9Motion.GetM9Motion(StationName,
                                          Unprocessed=Unprocessed,
                                          GetDistanceToRupture=GetDistanceToRupture,
                                          ResponseSpectra=ResponseSpectra,
                                          DistanceToClosestSite=DistanceToClosestSite,
                                          SensitivityRuns=SensitivityRuns)
    return json.dumps(Motions)

# Getting Motions For a Particular LatLon
@app.route('/getMotionInCSVFromLatLon', methods=['GET'])
def getMotionInCSVFromLatLon():
    # bar = request.args.to_dict()
    Latitude = request.args.get('Latitude')
    Longitude = request.args.get('Longitude')
    SensitivityRuns = bool(request.args.get('SensitivityRuns'))

    import ProcessM9Motion
    # Find Closest Site Code
    StationName, DistanceToClosestSite = ProcessM9Motion.FindClosestStationNameToLatLon(Latitude, Longitude)

    # Get Motion
    Motions = ProcessM9Motion.GetM9Motion(StationName,
                                          DistanceToClosestSite=DistanceToClosestSite,
                                          SensitivityRuns=SensitivityRuns)

    Line1 = ''
    Line2 = 'Time (s)'
    TimeHistory = []
    import numpy as np
    for i in range(len(Motions)):
        Line2 += ',%s - E-W (g), %s N-S(g), %s Vert.(g)'%(Motions[i]['Realization'],
                                                      Motions[i]['Realization'],
                                                      Motions[i]['Realization'])
        if i == 0:
            Line1 += '# Station Code: %s'%Motions[i]['StationCode'] + ', DistanceToClosestSite: %.5f' % Motions[i]['DistanceToClosestSite']
            TimeHistory.append(np.arange(0,len(Motions[i]['AccelerationHistory-EW']),1)*Motions[i]['TimeStep'])
            TimeHistory.append(Motions[i]['AccelerationHistory-EW'])
            TimeHistory.append(Motions[i]['AccelerationHistory-NS'])
            TimeHistory.append(Motions[i]['AccelerationHistory-Vert'])
        else:
            TimeHistory.append(Motions[i]['AccelerationHistory-EW'])
            TimeHistory.append(Motions[i]['AccelerationHistory-NS'])
            TimeHistory.append(Motions[i]['AccelerationHistory-Vert'])

    TimeHistory = list(np.transpose(TimeHistory))
    TimeHistory = list(map(lambda x: ''.join(list(map(lambda y: ' %.6e,'%y, x)))+'\n', TimeHistory))

    return Line1 + '\n' + Line2 + '\n' + ''.join(TimeHistory)

# Getting Motions For a Particular LatLon
@app.route('/getMotionInCSVFromStationName', methods=['GET'])
def getMotionInCSVFromStationName():
    # bar = request.args.to_dict()
    StationName = request.args.get('StationName')
    SensitivityRuns = bool(request.args.get('SensitivityRuns'))

    import ProcessM9Motion
    # Get Motion
    Motions = ProcessM9Motion.GetM9Motion(StationName,
                                          SensitivityRuns=SensitivityRuns)

    Line1 = ''
    Line2 = 'Time (s)'
    TimeHistory = []
    import numpy as np
    for i in range(len(Motions)):
        Line2 += ',%s - E-W (g), %s N-S(g), %s Vert.(g)'%(Motions[i]['Realization'],
                                                      Motions[i]['Realization'],
                                                      Motions[i]['Realization'])
        if i == 0:
            Line1 += '# Station Code: %s'%Motions[i]['StationCode'] + ', DistanceToClosestSite: %.5f' % Motions[i]['DistanceToClosestSite']
            TimeHistory.append(np.arange(0,len(Motions[i]['AccelerationHistory-EW']),1)*Motions[i]['TimeStep'])
            TimeHistory.append(Motions[i]['AccelerationHistory-EW'])
            TimeHistory.append(Motions[i]['AccelerationHistory-NS'])
            TimeHistory.append(Motions[i]['AccelerationHistory-Vert'])
        else:
            TimeHistory.append(Motions[i]['AccelerationHistory-EW'])
            TimeHistory.append(Motions[i]['AccelerationHistory-NS'])
            TimeHistory.append(Motions[i]['AccelerationHistory-Vert'])

    TimeHistory = list(np.transpose(TimeHistory))
    TimeHistory = list(map(lambda x: ''.join(list(map(lambda y: ' %.6e,'%y, x)))+'\n', TimeHistory))

    return Line1 + '\n' + Line2 + '\n' + ''.join(TimeHistory)

# Getting Motions For a Particular Site Code
@app.route('/getMotionFromStationName', methods=['GET'])
def getMotionFromStationName():
    StationName = request.args.get('StationName')
    Unprocessed = bool(request.args.get('Unprocessed'))
    GetDistanceToRupture = bool(request.args.get('GetDistanceToRupture'))
    ResponseSpectra = bool(request.args.get('ResponseSpectra'))
    SensitivityRuns = bool(request.args.get('SensitivityRuns'))

    import ProcessM9Motion
    import json
    Motions = ProcessM9Motion.GetM9Motion(StationName,
                                          Unprocessed=Unprocessed,
                                          GetDistanceToRupture=GetDistanceToRupture,
                                          ResponseSpectra=ResponseSpectra,
                                          SensitivityRuns=SensitivityRuns)
    return json.dumps(Motions)

def GetJson(Motions):
    import json
    from collections.abc import Mapping, Sequence
    class ScientificNotationEncoder(json.JSONEncoder):
        def iterencode(self, o, _one_shot=False):
            if isinstance(o, float):
                return "{:e}".format(o)
            elif isinstance(o, Mapping):
                return "{{{}}}".format(', '.join('"{}" : {}'.format(str(ok), self.iterencode(ov))
                                                 for ok, ov in o.items()))
            elif isinstance(o, Sequence) and not isinstance(o, str):
                return "[{}]".format(', '.join(map(self.iterencode, o)))
            return ', '.join(super().iterencode(o, _one_shot))
    return json.dumps(Motions, cls=ScientificNotationEncoder)

# --host=128.95.220.180 ... Add this to host globally
# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))


