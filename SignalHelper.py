from __future__ import absolute_import
from __future__ import print_function
from six.moves import range

__author__ = 'marafi'
#### Helper Created by Nasser Marafi
#### This to include in future versions:
#### -Phaseless Filtering using FILFIL command in scipy

def FourierSpectrum(GMData, Dt):
    import numpy as np
    import scipy.fftpack as scifft
    yf = abs(scifft.fft(GMData))
    xf = scifft.fftfreq(len(GMData), d=Dt)
    # xf = np.linspace(0, 1.0/2/Dt, len(GMData)/2)
    xT = 1.0/xf
    class Output:
        def __init__(self):
            self.FourierSpectrum = yf[:len(xT)/2]
            self.FourierFrequencies = xf[:len(xT)/2]
            self.FourierPeriods = xT[:len(xT)/2]
    return Output()

def LowPassFilter(Dt, data, CutOffFrequency, order=6):
    import numpy as np
    from scipy.signal import butter, lfilter, freqz
    def butter_lowpass(cutoff, fs, order=order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=order):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Filter requirements.
    fs = 1.0/Dt       # sample rate, Hz
    cutoff = CutOffFrequency # desired cutoff frequency of the filter, Hz

    # Get the filter coefficients so we can check its frequency response.
    # b, a = butter_lowpass(cutoff, fs, order)

    # Demonstrate the use of the filter.
    # First make some data to be filtered.
    T = len(data)*Dt
    t = np.linspace(0, T, len(data), endpoint=False)

    # Filter the data, and plot both the original and filtered signals.
    y = butter_lowpass_filter(data, cutoff, fs, order)

    b, a = butter_lowpass(cutoff, fs, order)
    w, h = freqz(b, a, worN=8000)
    np.seterr(divide='ignore')
    FilterX = 1.0/(0.5*fs*w/np.pi)
    FilterY = np.abs(h)
    class Output:
        def __init__(self):
            self.Time = t
            self.FilteredSignal = y
            self.Signal = data
            self.FilterPeriod = FilterX
            self.FilterY = FilterY
    return Output()

def HighPassFilter(Dt, data, CutOffFrequency, order=6):
    import numpy as np
    from scipy.signal import butter, lfilter, freqz
    def butter_lowpass(cutoff, fs, order=order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=order):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Filter requirements.
    fs = 1.0/Dt       # sample rate, Hz
    cutoff = CutOffFrequency # desired cutoff frequency of the filter, Hz

    # Get the filter coefficients so we can check its frequency response.
    # b, a = butter_lowpass(cutoff, fs, order)

    # Demonstrate the use of the filter.
    # First make some data to be filtered.
    T = len(data)*Dt
    t = np.linspace(0, T, len(data), endpoint=False)

    # Filter the data, and plot both the original and filtered signals.
    y = butter_lowpass_filter(data, cutoff, fs, order)

    b,a = butter_lowpass(cutoff, fs, order)
    w, h = freqz(b, a, worN=8000)
    np.seterr(divide='ignore')
    FilterX = 1.0/(0.5*fs*w/np.pi)
    FilterY = np.abs(h)
    class Output:
        def __init__(self):
            self.Time = t
            self.FilteredSignal = y
            self.Signal = data
            self.FilterPeriod = FilterX
            self.FilterY = FilterY
    return Output()

def FitPolynomialToData(Dt, data, order=6, IgnoreOrder=[0, 1]):

    import numpy as np
    time = np.arange(len(data))*Dt

    def poly(x):
        function = np.zeros(len(data))
        for i in range(len(x)):
            if i not in IgnoreOrder:
                function += x[i]*time**i
        return function

    def error(x):
        return np.sum(np.abs(data - poly(x)) ** 2.)

    # z = np.polyfit(time, data, order)
    # z[-1] = 0.
    # z[-2] = 0.
    # z = z[::-1]

    # x0 = np.zeros(order)
    # res =  minimize(error, x0)
    # z = res.x

    from numpy.polynomial import polynomial as P
    z = P.polyfit(time, data, 10 ) #[2,3,4,5,6,7,8,9]) # 10) #
    # z[0] = 0
    # z[1] = 0

    z = z[::-1]
    # print(z)

    class Output:
        def __init__(self):
            self.Results = z#res
            self.FitPoly = np.polyval(z, time)#poly(z)#
    return Output()

def RemoveDriftFromAccelerogram(dt, acc):
    import scipy.integrate as integrate
    import numpy as np

    dt = dt / 100.

    vel = integrate.cumtrapz(acc, dx=dt, initial=0)
    disp = integrate.cumtrapz(vel, dx=dt, initial=0)

    O = FitPolynomialToData(dt, disp, 12)

    polyvel = np.gradient(O.FitPoly)/dt
    polyacc = np.gradient(polyvel)/dt

    coeff = O.Results[::-1]
    for i in range(len(coeff)):
        coeff[i] = coeff[i]*i*(i-1)
    coeff = coeff[2:]

    time = np.arange(len(acc)) * dt
    polyacc = np.polyval(coeff[::-1], time)
    # print coeff

    return acc - polyacc

def RemoveResidualVelocityFromAccelerogram(dt, acc):

    import numpy as np

    dt = dt / 100.

    # import scipy.integrate as integrate
    # vel = integrate.cumtrapz(acc, dx=dt, initial=0)
    # disp = integrate.cumtrapz(vel, dx=dt, initial=0)

    vel = np.cumsum(acc,) * dt
    disp = np.cumsum(vel,) * dt
    vel = np.array([0] + list(vel))
    disp = np.array([0] + list(disp))

    O = FitPolynomialToData(dt, vel, 12, IgnoreOrder=[0])

    coeff = O.Results[::-1]
    for i in range(len(coeff)):
        coeff[i] = coeff[i] * i
    coeff = coeff[1:]

    time = np.arange(len(acc)) * dt
    polyacc = np.polyval(coeff[::-1], time)

    return acc - polyacc

def FilterSeriesInTimeDomain(dt, data, cutoff_time, sigma=1, revfilter=True):
    import numpy as np
    t = np.arange(len(data))*dt
    input = data
    # from scipy.stats import norm
    # window = norm.cdf(t, loc=cutoff_time, scale=sigma)
    window = np.array(list(map(lambda x: normcdf(x, cutoff_time, sigma), t)))

    if revfilter:
        window = 1. - window
    output = input * window

    class Output:
        def __init__(self):
            self.Time = t
            self.FilteredSignal = output
            self.Signal = data
            self.Window = window
    return Output()

from math import *
def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
        t*(.09678418+t*(-.18628806+t*(.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-.82215223+
        t*.17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r

def ncdf(x):
    return 1. - 0.5*erfcc(x/(2**0.5))

def normcdf(x, mu, sigma):
    t = x-mu;
    y = 0.5*erfcc(-t/(sigma*sqrt(2.0)));
    if y>1.0:
        y = 1.0;
    return y

def normpdf(x, mu, sigma):
    u = (x-mu)/abs(sigma)
    y = (1/(sqrt(2*pi)*abs(sigma)))*exp(-u*u/2)
    return y

def normdist(x, mu, sigma, f):
    if f:
        y = normcdf(x,mu,sigma)
    else:
        y = normpdf(x,mu,sigma)
    return y