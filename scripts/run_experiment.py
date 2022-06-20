from mmd_dilated import sequence_form_utils, mmd_dilated
import pyspiel
import utils
from absl import app
from absl import flags
from tqdm import tqdm

FLAGS = flags.FLAGS

flags.DEFINE_integer("iterations", 100, "Number of iterations")
flags.DEFINE_string("game", "kuhn", "Name of the game")
flags.DEFINE_integer("inverse_alpha", 2, "Inverse of alpha regularization parameter")
flags.DEFINE_bool("load_qre", True, "Load gambit QRE solution, if false then divergence will not be computed")
flags.DEFINE_bool("compute_gap", True, "Compute gap if true")
flags.register_validator('game',
                         lambda game: game in utils.game_data.keys(),
                         message='game not supported')

def main(argv):

    spiel_string = utils.game_data[FLAGS.game]['spiel_string']

    game = pyspiel.load_game(spiel_string)
    alpha = 1 / float(FLAGS.inverse_alpha)
    mmd = mmd_dilated.MMDDilatedEnt(game, alpha)

    if FLAGS.load_qre:
        qre_solution = utils.load_policy_from_nf_gambit_file(FLAGS.game, FLAGS.inverse_alpha)
        seq_solutions = sequence_form_utils.policy_to_sequence(game, qre_solution, mmd.infoset_actions_to_seq)
        solution = mmd_dilated.MMDDilatedEnt(game, alpha)
        solution.sequences = seq_solutions

    data = {
        'inverse_alpha': FLAGS.inverse_alpha,
        'alpha': alpha,
        'solutions': [list(seq_solutions[0]), list(seq_solutions[1])] if FLAGS.load_qre else None,
        'divergences': [],
        'gap': []
    }

    for i in tqdm(range(FLAGS.iterations)):
        mmd.update_sequences()
        if FLAGS.load_qre:
            data['divergences'].append(mmd_dilated.dilated_dgf_divergence(solution, mmd))
        if FLAGS.compute_gap:
            data['gap'].append(mmd.get_gap())
    utils.save_results(data, FLAGS.game, FLAGS.inverse_alpha)



if __name__ == "__main__":
  app.run(main)