
import numpy as np


def seasonal_function(t, phi, t_0):
    """
    Evaluates the seasonality function according to given parameters.
    :param t: times at which to evaluate the seasonal sinus (numpy.array)
    :param phi: seasonality phase (float)
    :param t_0: seasonality parameter changing the minimum value (float)
    :return: values of sinus representing the seasonality (numpy.array)
    """
    year_days_number = 365.0
    return (np.sin(2.0 * np.pi * t / year_days_number + np.pi + phi) + 1.0 + t_0) / (2.0 + t_0)


def dS(S, I, A, beta):
    """
    Computes the susceptible differential.
    :param S: number of susceptible (float)
    :param I: number of infected with symptoms (float)
    :param A: number of asymptomatic (float)
    :param beta: direct transmission (float)
    :return: susceptible differential (float)
    """
    return -beta * (I + A) * S


def dI(S, I, A, asym, beta, gamma):
    """
    Computes the infected differential.
    :param S: number of susceptible (float)
    :param I: number of infected with symptoms (float)
    :param A: number of asymptomatic (float)
    :param asym: fraction of asymptomatic (float)
    :param beta: direct transmission (float)
    :param gamma: recovery rate (float)
    :return: infected differential (float)
    """
    return (1.0 - asym) * S * beta * (I + A) - gamma * I


def dA(S, I, A, asym, beta, gamma):
    """
    Computes the asymptomatic differential.
    :param S: number of susceptible (float)
    :param I: number of infected with symptoms (float)
    :param A: number of asymptomatic (float)
    :param asym: fraction of asymptomatic (float)
    :param beta: direct transmission (float)
    :param gamma: recovery rate (float)
    :return: asymptomatic differential (float)
    """
    return asym * S * beta * (I + A) - gamma * A


def dR(I, A, gamma):
    """
    Computes the recovered differential.
    :param I: number of infected with symptoms (float)
    :param A: number of asymptomatic (float)
    :param gamma: recovery rate (float)
    :return: recovered differential (float)
    """
    return gamma * (I + A)


def dG(S, I, A, asym, beta):
    """
    Computes the cumulative infected differential.
    :param S: number of susceptible (float)
    :param I: number of infected with symptoms (float)
    :param A: number of asymptomatic (float)
    :param asym: fraction of asymptomatic (float)
    :param beta: direct transmission (float)
    :return: cumulative infected differential (float)
    """
    return (1.0 - asym) * S * beta * (I + A)


def meta_population_siarw(y, t, p):
    """
    Computes the meta-population ODEs variables differentials for
    the current state and time.
    :param y: current values of the meta-population ODEs variables (numpy.array)
    :param t: current time (float)
    :param p: parameters (dict)
    :return: variables differentials (numpy.array)
    """
    beta = p['beta'] * seasonal_function(t, p['phi'], p['t_0']) / p['Ns']

    S_ids = np.arange(0, p['M_c'] * 5, 5)
    I_ids = np.arange(1, p['M_c'] * 5, 5)
    A_ids = np.arange(2, p['M_c'] * 5, 5)
    R_ids = np.arange(3, p['M_c'] * 5, 5)
    G_ids = np.arange(4, p['M_c'] * 5, 5)

    travel_ratios = y[A_ids] / (y[S_ids] + y[A_ids] + y[R_ids])
    travel_component = (p['travel_matrix'].dot(travel_ratios) -
                        p['travel_matrix'].sum(1) * travel_ratios)

    dy = np.zeros(y.shape)
    dy[S_ids] = dS(y[S_ids], y[I_ids], y[A_ids],
                   beta) - travel_component
    dy[I_ids] = dI(y[S_ids], y[I_ids], y[A_ids],  # compartments
                   p['asym'], beta, p['gamma'])  # parameters
    dy[A_ids] = dA(y[S_ids], y[I_ids], y[A_ids],
                   p['asym'], beta, p['gamma']) + travel_component
    dy[R_ids] = dR(y[I_ids], y[A_ids],
                   p['gamma'])
    dy[G_ids] = dG(y[S_ids], y[I_ids], y[A_ids],
                   p['asym'], beta)

    return dy
