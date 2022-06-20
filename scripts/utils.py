"""
This file includes utility functions to:
- convert spiel normal form policies to spiel TabularPolicy objects.
- save/load data from experiments to json files
- generate divergence and gap plots

"""
from open_spiel.python import policy
import os
import pygambit
import pyspiel
import json
import matplotlib.pyplot as plt

DATA_DIR = "data/"
GAMBIT_SOL_DIR = "gambit/sf_qres/"
GAMBIT_GAME_DIR = 'gambit/gambit_games/'
MMD_RESULTS_DIR = 'mmd/'
FIGURE_DIR = 'figures/'

game_data = {'leduc': {'qre_file_string': 'leduc_poker',
                       'spiel_string': 'leduc_poker',
                       'gambit_game_file_string': '',
                        'figure_name': 'Leduc Poker'
                       },
              'liars_dice': {'qre_file_string': 'liars_dice',
                             'spiel_string': 'liars_dice(dice_sides=4)',
                             'gambit_game_file_string': '',
                             'figure_name': 'Liar\'s Dice'
                            },
             'dark_hex': {'qre_file_string': 'dark_hex',
                          'spiel_string': 'dark_hex(board_size=2,gameversion=adh)',
                          'gambit_game_file_string': 'dark_hex(num_rows=2,num_cols=2,gameversion=adh)',
                          'figure_name': 'Dark Hex'
                          },
             'kuhn': {'qre_file_string': 'kuhn_poker',
                      'spiel_string': 'kuhn_poker',
                      'gambit_game_file_string': 'kuhn_poker',
                      'figure_name': 'Kuhn Poker'
                      }
             }

def get_data_from_gambit_file_name(file):
    """ Get game name and alpha parameter from filename.
    Args:
        file: name of file to parse.

    Returns: Tuple of string and float.
    """
    for game in game_data.keys():
        game_name = game_data[game]['qre_file_string']
        if game_name in file:
            inverse_alpha = float(file.split(game_name)[-1].split('_')[0])
            return game_name, 1/inverse_alpha

def construct_gambit_file_string(game_key, inverse_alpha):
    game_name = game_data[game_key]['qre_file_string']
    return game_name + str(inverse_alpha) + "_sf.csv"


def load_policy_from_nf_gambit_file(game_key, inverse_alpha):
    """ Loads Gambit normal-form solution as spiel TabularPolicy.

    Args:
        game_key: key to lookup game_data dict.
        inverse_alpha: int corresponding to qre solution parameter.

    Returns:
        TabularPolicy object that is realization equivalent to the
        Gambit normal-form solution.
    """
    filename = construct_gambit_file_string(game_key, inverse_alpha)
    nf_strat = load_nf_strat(filename)
    return nf_to_spiel_policy(game_key, nf_strat)

def load_nf_strat(fn):
    """ Load normal-form solution from filename.

    Args:
        fn: filename string.

    Returns:
        List of floats.
    """
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_DIR, GAMBIT_SOL_DIR, fn)
    with open(filename, 'r') as f:
        last_line = f.readlines()[-1]
        return [float(x) for x in last_line.split(",")[1:]]

def nf_to_spiel_policy(game_key, nf_strat):
    """ Convert normal-form Gambit strategy to spiel TabularPolicy.

    Args:
        game_key: key to lookup game_data dict.
        nf_strat: List of floats, taken from last line of Gambit file.

    Returns:
        TabularPolicy object.
    """

    game_string = game_data[game_key]['gambit_game_file_string']
    game_string = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_DIR, GAMBIT_GAME_DIR, game_string + ".efg")
    gambit_game = pygambit.Game.read_game(game_string)
    p = gambit_game.mixed_strategy_profile()

    for i, strat in enumerate(gambit_game.strategies):
        p[strat] = nf_strat[i]
    behavior_strat = list(p.as_behavior())

    game = pyspiel.load_game(game_data[game_key]['spiel_string'])
    tab_pol = policy.TabularPolicy(game)
    idx = 0
    for i, legal in enumerate(tab_pol.legal_actions_mask):
        for k, b in enumerate(legal):
            if b:
                tab_pol.action_probability_array[i, k] = behavior_strat[idx]
                idx += 1
    return tab_pol

def construct_figure_filename(game_key, type='divergence'):
    game_string = game_data[game_key]['qre_file_string']
    if type == 'divergence':
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_DIR, FIGURE_DIR,
                                game_string + "_divergence.pdf")
        return filename

    elif type == 'gap':
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_DIR, FIGURE_DIR,
                                game_string + "_gap.pdf")
        return filename

def construct_divergence_plot(data_list, game_key):

    plt.yscale('log')
    plt.ylim(bottom=1e-6)
    plt.title(game_data[game_key]['figure_name'] + " | Divergence to NF QRE")
    plt.xlabel("Iterations")
    for data in data_list:
        alpha = data['alpha']
        plt.plot(data['divergences'], label=r"$\alpha={:10.2f}$".format(alpha))
    plt.legend()
    file_name = construct_figure_filename(game_key)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    plt.savefig(file_name)
    plt.close()

def construct_gap_plot(data_list, game_key):

    plt.yscale('log')
    plt.ylim(bottom=1e-10)
    plt.title(game_data[game_key]['figure_name'] + " | Saddle Point Gap")
    plt.xlabel("Iterations")
    for data in data_list:
        alpha = data['alpha']
        plt.plot(data['gap'], label=r"$\alpha={:10.2f}$".format(alpha))
    plt.legend()
    file_name = construct_figure_filename(game_key, type='gap')
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    plt.savefig(file_name)
    plt.close()


def construct_data_filename(game_key, inverse_alpha):
    game_string = game_data[game_key]['qre_file_string']
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATA_DIR, MMD_RESULTS_DIR,
                            game_string + "%" + str(inverse_alpha) + ".json")
    return filename

def save_results(data, game_key, inverse_alpha):
    """ Save experiment results to json file.

    Args:
        data: dict generated from experiment.
        game_key: key to lookup game_data dict.
        inverse_alpha: int corresponding to qre solution parameter.
    """
    file_name = construct_data_filename(game_key, inverse_alpha)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    json.dump(data, open(file_name, 'w'))

def load_results(game_key, inverse_alpha):
    return json.load(open(construct_data_filename(game_key, inverse_alpha)))

