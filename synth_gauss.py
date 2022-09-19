
import numpy as np

from scipy.optimize import minimize

from tools import (meta_population_sample, meta_population_cumulative,
                   load_full_dataset, load_specific_city, data_travel)
from config import get_arguments

# Params

args = get_arguments()

start_date = args.start
end_date = args.end
active_sampling = args.active_sampling
t_max = 2300

M_c = args.c
cities = ['Tartagal', 'Oran', 'Jujuy', 'Guemes', 'Tucuman', 'Santa Fe', 'Mendoza', 'Buenos Aires']
cities = cities[:M_c]
Ns = np.array([4.4e4, 5.1e4, 2e5, 2.3e4, 6.3e5, 4e5, 8e5, 2e6])
Ns = Ns[:M_c]

travel_matrix = data_travel() / args.travel_norm
travel_matrix = travel_matrix[:M_c, :M_c]

params = [args.asym,
          np.array([args.betas2[0], args.betas2[0], args.betas2[1]]),
          args.gamma, args.phi, args.sin_0, args.init, args.shift,
          Ns, M_c, travel_matrix]


# Functions

def objective(pars,  # asym, beta_1, beta_2, t_0, init, phi
              shift, gamma, Ns, M_c, travel_matrix, sampling, y_sample, opt_ids):
    betas = np.array([pars[1], pars[1], pars[2]])
    y_opt = meta_population_sample(sampling, pars[0], betas, gamma, pars[5], pars[3], pars[4], shift,
                                   Ns, M_c, travel_matrix, init_n=M_c, active_sampling=active_sampling)

    if args.r > 1:
        y_opt = np.repeat(y_opt, args.r)

    objs = (y_opt - y_sample)[opt_ids] ** 2.0

    return objs.sum() / objs.shape[0]


# Load Sample

data = load_full_dataset()

sampling = dict()
y_sample = []
for j, city in enumerate(cities):
    x, z = load_specific_city(data, city, start_date, end_date)
    sampling[city] = x[z > 0.0]

    y_sample.append(meta_population_cumulative(x[z > 0.0], *params,
                                               init_n=M_c, active_sampling=active_sampling)[:, 4 + 5 * j])
y_sample = np.concatenate(y_sample)

y_sample = np.repeat(y_sample, args.r)

y_sample += np.random.normal(size=y_sample.shape[0], scale=args.noise)
if not args.negative_cases:
    y_sample[y_sample < 0.0] = 0.0
if args.neglect_zeros:
    opt_ids = y_sample > 0.0
else:
    opt_ids = np.repeat(True, y_sample.shape[0])

# Minimization

# x0 = np.array([args.asym, args.beta, args.sin_0, args.init, args.phi, args.sigma])

arguments = (args.shift, args.gamma, Ns, M_c, travel_matrix, sampling, y_sample, opt_ids)
limits = [[0.0, 1.0], [0.0, None], [0.0, None], [0.0, None], [0.0, None], [0.0, 2.0 * np.pi]]

ws = []
params = [args.asym, *args.betas2, args.sin_0, args.init, args.phi, args.noise, args.shift, args.gamma]
for ii in range(args.m):
    x0 = np.array([np.random.random(), np.random.random() * 0.179 + 0.001, np.random.random() * 0.179 + 0.001,
                   np.random.random() * 20.0, np.random.random() * 20.0, np.random.random() * 2.0 * np.pi])

    res = minimize(objective, x0, args=arguments, bounds=limits)

    temp_sd = objective(res.x, *arguments)

    ws.append(list(res.x))
    ws[-1].append(temp_sd)
    ws[-1] = params + ws[-1]

ws = np.array(ws)

# Save

np.save('results/' + args.name + '.npy', ws)
