import os
import utils
from absl import app
from absl import flags
from multiprocessing import Pool
from functools import partial

FLAGS = flags.FLAGS

flags.DEFINE_integer("cores", 1, "Number of cores to use")

experiments = [{'game':'kuhn',
                'inverse_alphas': [2, 5, 10, 20],
                'iterations': [20000]*4,
                'load_qre': True,
                'compute_gap':True
                },
               {'game': 'dark_hex',
                'inverse_alphas': [2, 5, 10, 20],
                'iterations': [20000]*4,
                'load_qre': True,
                'compute_gap':True
                 },
                {'game': 'leduc',
                 'inverse_alphas': [2, 5, 10, 20],
                 'iterations': [30000]*4,
                 'load_qre': False,
                 'compute_gap': True
                 },
                {'game': 'liars_dice',
                 'inverse_alphas': [2, 5, 10, 20],
                 'iterations': [30000]*4,
                 'load_qre': False,
                 'compute_gap': True
                 },
               ]


def construct_command(game, inverse_alpha, iterations, load_qre, compute_gap):
    return "python scripts/run_experiment.py --game={} ".format(game) +\
           "--inverse_alpha={} ".format(inverse_alpha) +\
           "--iterations={0:d} ".format(iterations) +\
           "--load_qre={} ".format(load_qre) + \
           "--compute_gap={} ".format(compute_gap)

def run_experiment(game, load_qre, compute_gap, inverse_alpha, iterations):

    if not os.path.exists(utils.construct_data_filename(game, inverse_alpha)):
        command = construct_command(game, inverse_alpha, iterations,
                                    load_qre, compute_gap)
        print(command, flush=True)
        os.system(command)
    return utils.load_results(game, inverse_alpha)


def main(argv):

    for experiment in experiments:
        game = experiment['game']
        f = partial(run_experiment, game, experiment['load_qre'], experiment['compute_gap'])

        with Pool(FLAGS.cores) as p:
            data_list = p.starmap(f, zip(experiment['inverse_alphas'], experiment['iterations']))

        if experiment['load_qre']:
            utils.construct_divergence_plot(data_list, game)

        if experiment['compute_gap']:
            utils.construct_gap_plot(data_list, game)

if __name__ == "__main__":
  app.run(main)