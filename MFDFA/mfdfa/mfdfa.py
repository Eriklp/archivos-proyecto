import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

#from PyQt5.QtCore import QThread


# def calc_rms(x, scale):
#     """
#     windowed Root Mean Square (RMS) with linear detrending.
#
#     Args:
#     -----
#       *x* : numpy.array
#         one dimensional data vector
#       *scale* : int
#         length of the window in which RMS will be calculaed
#     Returns:
#     --------
#       *rms* : numpy.array
#         RMS data in each window with length len(x)//scale
#     """
#     # making an array with data divided in windows
#     print("escala: "+  str(scale))
#     shape = (x.shape[0]//scale, scale)
#     X = np.lib.stride_tricks.as_strided(x,shape=shape)
#     # vector of x-axis points to regression
#     scale_ax = np.arange(scale)
#     rms = np.zeros(X.shape[0])
#     for e, xcut in enumerate(X):
#         coeff = np.polyfit(scale_ax, xcut, 1)
#         xfit = np.polyval(coeff, scale_ax)
#         # detrending and computing RMS of each window
#         rms[e] = np.sqrt(np.mean((xcut-xfit)**2))
#     return rms
#
#
# # detrended fluctuation analysis
#
# def dfa(x, scale_lim=[5,9], scale_dens=0.5, show=True):
#     """
#     Detrended Fluctuation Analysis - measures power law scaling coefficient
#     of the given signal *x*.
#     More details about the algorithm you can find e.g. here:
#     Hardstone, R. et al. Detrended fluctuation analysis: A scale-free
#     view on neuronal oscillations, (2012).
#     Args:
#     -----
#       *x* : numpy.array
#         one dimensional data vector
#       *scale_lim* = [5,9] : list of length 2
#         boundaries of the scale, where scale means windows among which RMS
#         is calculated. Numbers from list are exponents of 2 to the power
#         of X, eg. [5,9] is in fact [2**5, 2**9].
#         You can think of it that if your signal is sampled with F_s = 128 Hz,
#         then the lowest considered scale would be 2**5/128 = 32/128 = 0.25,
#         so 250 ms.
#       *scale_dens* = 0.25 : float
#         density of scale divisions, eg. for 0.25 we get 2**[5, 5.25, 5.5, ... ]
#       *show* = False
#         if True it shows matplotlib log-log plot.
#     Returns:
#     --------
#       *scales* : numpy.array
#         vector of scales (x axis)
#       *fluct* : numpy.array
#         fluctuation function values (y axis)
#       *alpha* : float
#         estimation of DFA exponent
#     """
#     # cumulative sum of data with substracted offset
#     y = np.cumsum(x - np.mean(x))
#     scales = (2**np.arange(scale_lim[0], scale_lim[1], scale_dens)).astype(np.int)
#     print(scales)
#     fluct = np.zeros(len(scales))
#     # computing RMS for each window
#     for e, sc in enumerate(scales):
#         if sc != 0:
#             print(y, sc)
#             fluct[e] = np.sqrt(np.mean(calc_rms(y, sc)**2))
#         else:
#             pass
#     # fitting a line to rms data
#     coeff = np.polyfit(np.log2(scales), np.log2(fluct), 1)
#     if show:
#         fluctfit = 2**np.polyval(coeff,np.log2(scales))
#         plt.loglog(scales, fluct, 'bo')
#         plt.loglog(scales, fluctfit, 'r', label=r'$\alpha$ = %0.2f'%coeff[0])
#         plt.title('DFA')
#         plt.xlabel(r'$\log_{10}$(time window)')
#         plt.ylabel(r'$\log_{10}$<F(t)>')
#         plt.legend()
#         plt.show()
#     return scales, fluct, coeff[0]
#     print(scales, fluct, coeff[0])
#
##intento dos de mfdfa



# import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval
def MFDFA(timeseries: np.ndarray, lag: np.ndarray=None, order: int=1,
          q: np.ndarray=2, modified: bool=False) -> np.ndarray:
    """
    Multi-Fractal Detrended Fluctuation Analysis of timeseries. MFDFA generates
    a fluctuation function F²(q,s), with s the segment size and q the q-powers,
    Take a timeseries Xₜ, find the integral Yₜ = cumsum(Xₜ), and segment the
    timeseries into Nₛ segments of size s.
                                        ₛ
                          Fᵥ²(s) = ¹/ₛ∑[Yᵥᵢ - yᵥᵢ]²
                                        ⁱ
    with yᵥᵢ the polynomial fittings of order m. Having obtained the variances
    of each (detrended) segment, average over s and increase s, to obtain the
    fluctuation function Fₚ²(s) depending on the segment lenght.
                       F²(q,s) = {1/Nₛ∑[Fᵥ²(s)]^q/2}^1/q,
                                     ᵛ
    The fluctuation function F²(q,s) can now be plotted in a log-log scale, the
    slope of the fluctuation function F²(q,s) vs the s-segment size is the
    self-similarity scaling h(q)
                                  F²(q,s) ~ sʰ.
    If H ≈ 0 in a monofractal series, use a second integration step by setting
    'modified' = True.
    Parameters
    ----------
    timeseries: np.ndarray
        A 1-dimensional timeseries (N, 1). The timeseries of length N.
    lag: np.ndarray of ints
        An array with the window sizes to calculate (ints). Notice
        min(lag) > order + 1 because to fit a polynomial of order m one needs at
        least m points. The results are meaningless for 'order = m' and for
        lag > size of data / 4 since there is low statistics with < 4 windows
        to divide the timeseries.
    order: int
        The order of the polynomials to approximate. 'order = 1' is the DFA1,
        which is a least-square fit of the data with a first order polynomial (a
        line), 'order = 2' is a second-order polynomial, etc..
    q: np.ndarray
        Fractal exponent to calculate. Array in [-10,10]. The values = 0 will be
        removed, since the code does not converge there. q = 2 is the standard
        Detrended Fluctuation Analysis as is set a default.
    modified: bool
        For data with the Hurst exponent ≈ 0, i.e., strongly anticorrelated, a
        standard MFDFA will result in inacurate results, thus a further
        integration of the timeseries yields a modified scaling coefficient.
    Returns
    -------
    lag: np.ndarray of ints
        Array of lags, realigned, preserving only different lags and with
        entries > order + 1
    f: np.ndarray
        A array of shape (size(lag),size(q)) of variances over the indicated
        lag windows and the indicated q-fractal powers.
    """

    # Force lag to be ints, ensure lag > order + 1
    lag = lag[lag > order + 1]
    lag = np.round(lag).astype(int)

    # Assert if timeseries is 1 dimensional
    if timeseries.ndim > 1:
        assert timeseries.shape[1] == 1, "Timeseries needs to be 1 dimensional"

    timeseries = timeseries.reshape(-1,1)
    # Size of array
    N = timeseries.shape[0]

    # Fractal powers as floats
    q = np.asarray_chkfinite(q, dtype = float)

    # Ensure q≈0 is removed, since it does not converge. Limit set at |q| < 0.1
    q = q[(q < -.1) + (q > .1)]

    # Reshape q to perform np.float_power
    q = q.reshape(-1, 1)
    #print("Q: ", q)
    # x-axis
    X = np.linspace(1, lag.max(), lag.max())

    # "Profile" of the series
    Y = np.cumsum(timeseries - np.mean(timeseries))

    # Cumulative "profile" for strongly anticorrelated data:
    if modified == True:
        Y = np.cumsum(Y - np.mean(Y))

    # Return f of (fractal)-variances
    f = np.empty((0, q.size))


    # Loop over elements in lag
    # Notice that given one has to slip the timeseries into diferent segments of
    # length lag(), so some elements at the end of the array might be missing.
    # The same procedure it run in reverse, were elements at the begining of the
    # series are discared instead
    for i in lag:
        # Reshape into (N/lag, lag)
        Y_ = Y[:N - N % i].reshape((N - N % i) // i, i)
        Y_r = Y[N % i:].reshape((N - N % i) // i, i)

        # Perform a polynomial fit to each segments
        p = polyfit(X[:i], Y_.T, order)
        p_r = polyfit(X[:i], Y_r.T, order)
        #print(p)
        # Subtract the trend from the fit and calculate the variance
        F = np.var(Y_ - polyval(X[:i], p), axis = 1)
        F_r = np.var(Y_r - polyval(X[:i], p_r), axis = 1)
        #print(F)
        # Caculate the Multi-Fractal Detrended Fluctuation Analysis
        f = np.append(f,
              np.float_power(
                np.mean( np.float_power(F, q / 2), axis = 1) / 2,
              1 / q.T)
              + np.float_power(
                np.mean( np.float_power(F_r, q / 2), axis = 1) / 2,
              1 / q.T),
            axis = 0)

    #coeff = np.polyfit(np.log2(Y), np.log2(F), 1)
    #plt.loglog(q, f, 'o', label='fOU: MFDFA q=2')
    #plt.show()

    print(lag, f)
    return lag, f

# class mfdfa(QThread):
#
#     timeSerie = []
#     escala = []
#
#     tipo = 1
#
#     def __init__(self, x, escala, tipo):
#         #self.timeSerie = np.abs(ss.hilbert(np.array(x)))
#         self.timeSerie = np.array(x)
#         self.escala = np.array(escala)
#         print(self.escala)
#         self.tipo = tipo
#         super().__init__()
#
#     def run(self):
#         #print(type(self.timeSerie))
#         #x = self.timeSerie
#         #print(x)
#         lag, f = MFDFA(timeseries =  self.timeSerie,  lag = np.array([5000000, 10000000, 15000000, 20000000]), order = self.tipo, q = self.escala)
#         print(lag, f)




    # if __name__=='__main__':
    #     n = 1000
    #     x = np.random.randn(n)
    #     # computing DFA of signal envelope
    #     x = np.abs(ss.hilbert(x))
    #     scales, fluct, alpha = dfa(x, show=1)
    #     print(scales)
    #     print(fluct)
    #     print("DFA exponent: {}".format(alpha))
