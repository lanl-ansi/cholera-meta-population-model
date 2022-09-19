
import numpy as np

from scipy.integrate import odeint

from tools import meta_population_siarw

t_max = 2300


def meta_population_solution(t, asym, beta, gamma, phi, t_0, init, Ns, M_c, travel_matrix, init_n=4):
    """
    Solves the meta-population ODEs and returns the values for specified times.
    :param t: times at which to find the ODE solution (numpy.array)
    :param asym: fraction of asymptomatic cases (float)
    :param beta: transmission rate/s (float/numpy.array)
    :param gamma: recovery rate (float)
    :param phi: seasonality phase (float)
    :param t_0: seasonality parameter (float)
    :param init: number of initial cases (float/numpy.array)
    :param Ns: populations of the cities (numpy.array)
    :param M_c: number of analysed cities (int)
    :param travel_matrix: travelling rates (numpy.array)
    :param init_n: number of cities with initial cases (int)
    :return: solution of the ODE equations for the meta-population model (numpy.array)
    """
    y0 = np.zeros(M_c * 5)
    y0[np.arange(0, M_c * 5, 5)] = Ns
    y0[0 + 5 * np.arange(init_n)] = y0[0 + 5 * np.arange(init_n)] - init
    y0[2 + 5 * np.arange(init_n)] = init

    p = {'asym': asym, 'beta': beta, 'gamma': gamma, 'phi': phi,
         't_0': t_0, 'Ns': Ns, 'M_c': M_c, 'travel_matrix': travel_matrix}

    return odeint(meta_population_siarw, y0, t, args=(p,), mxstep=10000, rtol=1e-11, atol=1e-11)


def meta_population_cumulative(t, asym, beta, gamma, phi, t_0, init, shift, Ns, M_c, travel_matrix,
                               init_n=4, active_sampling=14):
    """
    Computes the cumulative (over last 14 days or until previous observation) values of all
    meta-population ODEs variables and for all cities at the specified days. First axis of
    the returned array represent time, while the second represents variables (varibales of
    the first city, then second city and so on).
    :param t: times at which to find the ODE solution (numpy.array)
    :param asym: fraction of asymptomatic cases (float)
    :param beta: transmission rate/s (float/numpy.array)
    :param gamma: recovery rate (float)
    :param phi: seasonality phase (float)
    :param t_0: seasonality parameter (float)
    :param init: number of initial cases (float/numpy.array)
    :param shift: difference in days between first day and the first cases day (int)
    :param Ns: populations of the cities (numpy.array)
    :param M_c: number of analysed cities (int)
    :param travel_matrix: travelling rates (numpy.array)
    :param init_n: number of cities with initial cases (int)
    :param active_sampling: number of past days a single sampling includes (int)
    :return: cumulative values for different variables at different times (numpy.array)
    """
    y0 = np.zeros(M_c * 5)
    y0[np.arange(0, M_c * 5, 5)] = Ns
    y0[0 + 5 * np.arange(init_n)] = y0[0 + 5 * np.arange(init_n)] - init
    y0[2 + 5 * np.arange(init_n)] = init

    p = {'asym': asym, 'beta': beta, 'gamma': gamma, 'phi': phi,
         't_0': t_0, 'Ns': Ns, 'M_c': M_c, 'travel_matrix': travel_matrix}

    tau = np.concatenate(([shift], t))
    tau[tau <= shift] = shift
    tau = np.concatenate(([shift], np.max([t - active_sampling, tau[:-1]], axis=0), t))
    order = np.argsort(tau)

    output = odeint(meta_population_siarw, y0, tau[order], args=(p,), mxstep=10000, rtol=1e-11, atol=1e-11)

    reverse = np.argsort(order)
    return (output[reverse[int(1 + tau.shape[0] / 2):], :] -
            output[reverse[1:int(1 + tau.shape[0] / 2)], :])


def meta_population_sample(sampling, asym, beta, gamma, phi, t_0, init, shift, Ns, M_c, travel_matrix,
                           init_n=4, active_sampling=14):
    """
    Computes all the samples according to the sampling structure, which specifies times for different
    cities. The result is a single vector of number of cases.
    :param sampling: sampling structure (dict)
    :param asym: fraction of asymptomatic cases (float)
    :param beta: transmission rate/s (float/numpy.array)
    :param gamma: recovery rate (float)
    :param phi: seasonality phase (float)
    :param t_0: seasonality parameter (float)
    :param init: number of initial cases (float/numpy.array)
    :param shift: difference in days between first day and the first cases day (int)
    :param Ns: populations of the cities (numpy.array)
    :param M_c: number of analysed cities (int)
    :param travel_matrix: travelling rates (numpy.array)
    :param init_n: number of cities with initial cases (int)
    :param active_sampling: number of past days a single sampling includes (int)
    :return: one dimensional array of all samples (numpy.array)
    """
    t = np.arange(shift, t_max)
    output = meta_population_solution(t, asym, beta, gamma, phi, t_0, init, Ns, M_c, travel_matrix, init_n)

    res = []
    for j, city in enumerate(sampling.keys()):
        pre_sampling = sampling[city][:-1]
        pre_sampling = np.insert(pre_sampling, 0, shift)
        pre_sampling[pre_sampling < shift] = shift
        pre_sampling = np.max([sampling[city] - active_sampling, pre_sampling], axis=0)
        res.append(output[sampling[city], 4 + 5 * j] - output[pre_sampling, 4 + 5 * j])

    return np.concatenate(res)
