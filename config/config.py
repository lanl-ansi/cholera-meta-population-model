
import argparse

parser = argparse.ArgumentParser(description="Fit Arguments")

parser.add_argument('-name', type=str, action='store', default='setup',
                    dest='name', help='filename')

parser.add_argument('-start', type=str, action='store', default='1992-02-08',
                    dest='start', help='model starting date')
parser.add_argument('-end', type=str, action='store', default='1998-07-28',
                    dest='end', help='model last date')
parser.add_argument('-c', type=int, action='store', default=3,
                    dest='c', help='number of cities')

parser.add_argument('-fix_asym', type=float, action='store', default=0.1,
                    dest='fix_asym', help='fixed fraction of asymptomatic')

parser.add_argument('-asym', type=float, action='store', default=0.32,
                    dest='asym', help='fraction of asymptomatic')
parser.add_argument('-beta', type=float, action='store', default=1.6e-1,
                    dest='beta', help='direct infection')
parser.add_argument('-sin_0', type=float, action='store', default=11,
                    dest='sin_0', help='minimum beta shift')
parser.add_argument('-init', type=float, action='store', default=10,
                    dest='init', help='initial number of asymptomatic')
parser.add_argument('-phi', type=float, action='store', default=5.8,
                    dest='phi', help='phase of the seasonality')

parser.add_argument('-inits', type=float, action='store', nargs='+',
                    default=[7.0, 7.0, 7.0, 7.0],
                    dest='inits', help='initial cases in different cities')
parser.add_argument('-betas', type=float, action='store', nargs='+',
                    default=[1.6e-1, 1.6e-1, 1.6e-1, 1.6e-1, 1.6e-1, 1.6e-1, 1.6e-1, 1.6e-1],
                    dest='betas', help='direct infection in different cities')
parser.add_argument('-betas2', type=float, action='store', nargs='+',
                    default=[1.57e-1, 1.55e-1],
                    dest='betas2', help='direct infection in different city sizes')

parser.add_argument('-gamma', type=float, action='store', default=1.0 / 7.0,
                    dest='gamma', help='recovery rate')
parser.add_argument('-shift', type=float, action='store', default=0.0,
                    dest='shift', help='position in respect to first sample')

parser.add_argument('-travel', type=float, action='store', default=1.0,
                    dest='travel_norm', help='normalisation constant for travel')
parser.add_argument('-sampling', type=int, action='store', default=14,
                    dest='active_sampling', help='sampling horizon')
parser.add_argument('-min_init', type=float, action='store', default=4.0,
                    dest='min_init', help='minimal number of initial cases')

parser.add_argument('-noise', type=float, action='store', default=0.0,
                    dest='noise', help='noise for synthetic experiments')

parser.add_argument('-m', type=int, action='store', default=100,
                    dest='m', help='number of different initial conditions')
parser.add_argument('-r', type=int, action='store', default=1,
                    dest='r', help='number of sample repeats')

parser.add_argument('--asym', action='store_const', default=False, const=True, dest='fit_asym',
                    help='whether to fit asymptomatic')
parser.add_argument('--beta', action='store_const', default=False, const=True, dest='fit_beta',
                    help='whether to fit beta')
parser.add_argument('--sin_0', action='store_const', default=False, const=True, dest='fit_sin_0',
                    help='whether to fit sin_0')
parser.add_argument('--init', action='store_const', default=False, const=True, dest='fit_init',
                    help='whether to fit init')
parser.add_argument('--phi', action='store_const', default=False, const=True, dest='fit_phi',
                    help='whether to fit phi')
parser.add_argument('--shift', action='store_const', default=False, const=True, dest='fit_shift',
                    help='whether to fit shift')

parser.add_argument('--negative_cases', action='store_const', default=False, const=True, dest='negative_cases',
                    help='whether negative case counts are possible (for synthetic experiments)')
parser.add_argument('--neglect_zeros', action='store_const', default=False, const=True, dest='neglect_zeros',
                    help='whether non-positive case counts should be neglected (for synthetic experiments)')

args = parser.parse_args()


def get_arguments():
    return args
