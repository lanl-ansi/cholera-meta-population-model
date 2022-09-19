
import numpy as np
import pandas as pd


def load_full_dataset():
    """
    Generates a data frame with records meeting certain conditions
    (human origin, assigned timestamp and serogroup O1).
    :return: full dataset (pandas.DataFrame)
    """
    data = pd.read_csv('data/joined_metadata_with_seq_lanes_and_geo_MANUAL_EDIT.csv')

    condition = ((data['Isolate.date'].notnull()) & (data['Origin'] == 'Human') & (data['Serogroup.x'] == 'O1'))
    return data[condition]


def load_specific_city(data, city, start_date, end_date):
    """
    Loads number of cases in a given period for a specified city.
    :param data: full dataset (pandas.DataFrame)
    :param city: city name (str)
    :param start_date: starting date (str)
    :param end_date: ending date (str)
    :return: iterator and number of cases for specified city (numpy.array, numpy.array)
    """
    set_of_names = {'Tartagal': ['Tartagal, Salta'],
                    'Jujuy': ['Jujuy', 'Pericho, Jujuy'],  # I assume it's Pericho plus San Salvador de Jujuy
                    'Oran': ['Oran, Salta'],
                    'Tucuman': ['Tucuman', 'San Miguel de Tucuman'],  # I assume it's mostly San Miguel
                    'Mendoza': ['Mendoza'],
                    'Buenos Aires': ['Buenos Aires (city)', 'Avellaneda, Buenos Aires', 'La Plata, Buenos Aires'],
                    'Santa Fe': ['Santa Fe', 'Rosario, Santa Fe'],
                    'Guemes': ['General Guemes, Salta'],
                    'Salta': ['Apolinario Saravia, Salta', 'Colonia Santa Rosa, Salta', 'Embarcación, Salta',
                              'General Guemes, Salta', 'Metan, Salta', 'Tartagal, Salta', 'Oran, Salta',
                              'Pichanal, Salta', 'Rosario de la Frontera, Salta', 'Salta, Salta', 'Salta',
                              'Salvador Mazza, Salta', 'Santa Rosa, Salta']}
    names = set_of_names[city]

    start_dt = np.datetime64(start_date)
    end_dt = np.datetime64(end_date)

    city_data = data[data['Geographic.origin_NR'].isin(names)]

    x, y = np.unique(pd.to_datetime(city_data['Isolate.date'], format='%d/%m/%Y'), return_counts=True)
    y = y[(x >= start_dt) & (x <= end_dt)]
    x = x[(x >= start_dt) & (x <= end_dt)]
    x = (x - start_dt).astype('timedelta64[D]').astype('int')

    d = x.max() + 1
    z = np.zeros(d)
    z[x] = y
    x = np.arange(d)
    return x, z


def load_specific_city_dates(data, city, start_date, end_date):
    """
    Loads number of cases in a given period for a specified city (with dates).
    :param data: full dataset (pandas.DataFrame)
    :param city: city name (str)
    :param start_date: starting date (str)
    :param end_date: ending date (str)
    :return: dates and number of cases for specified city (numpy.array, numpy.array)
    """
    set_of_names = {'Tartagal': ['Tartagal, Salta'],
                    'Jujuy': ['Jujuy', 'Pericho, Jujuy'],  # I assume it's Pericho plus San Salvador de Jujuy
                    'Oran': ['Oran, Salta'],
                    'Tucuman': ['Tucuman', 'San Miguel de Tucuman'],  # I assume it's mostly San Miguel
                    'Mendoza': ['Mendoza'],
                    'Buenos Aires': ['Buenos Aires (city)', 'Avellaneda, Buenos Aires', 'La Plata, Buenos Aires'],
                    'Santa Fe': ['Santa Fe', 'Rosario, Santa Fe'],
                    'Guemes': ['General Guemes, Salta'],
                    'Salta': ['Apolinario Saravia, Salta', 'Colonia Santa Rosa, Salta', 'Embarcación, Salta',
                              'General Guemes, Salta', 'Metan, Salta', 'Tartagal, Salta', 'Oran, Salta',
                              'Pichanal, Salta', 'Rosario de la Frontera, Salta', 'Salta, Salta', 'Salta',
                              'Salvador Mazza, Salta', 'Santa Rosa, Salta']}
    names = set_of_names[city]

    start_dt = np.datetime64(start_date)
    end_dt = np.datetime64(end_date)

    city_data = data[data['Geographic.origin_NR'].isin(names)]

    x, y = np.unique(pd.to_datetime(city_data['Isolate.date'], format='%d/%m/%Y'), return_counts=True)
    y = y[(x >= start_dt) & (x <= end_dt)]
    x = x[(x >= start_dt) & (x <= end_dt)]
    return x, y


def data_travel():
    """
    Loads the travelling rates from a file.
    :return: matrix of travelling rates (numpy.array)
    """
    return np.loadtxt('data/travel.csv', delimiter=';')
