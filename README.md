# MMD_Dilated

This repository implements magnetic mirror descent (MMD) with dilated entropy.
MMD converges in the last iterate linearly (i.e. exponentially fast) 
to a reduced normal-form quantal response equilibrium (QRE). 
For more details see [https://arxiv.org/abs/2206.05825](https://arxiv.org/abs/2206.05825).



## Installation
The code requires python 3.10.
- Clone the repository using the command `git clone https://github.com/ryan-dorazio/mmd-dilated.git`
- Enter the directory using `cd mmd-dilated`
- Install the package with the command `pip install .`

## Reproducing Results
The command `python scripts/main.py` reproduces the MMD dilated entropy 
results in the paper. Note that the script takes a `num_cores` argument to
run some experiments in parallel with a default value of 1.
For example the command `python scripts/main.py --cores=4` would execute the script
using 4 cores.
The results of the experiments are saved as json files in the directory `data/mmd`
with corresponding figures in `data/figures`.
The experiments for Kuhn and Dark Hex are relatively quick, Leduc and Liar's Dice
can take between 12hrs and 24hrs using 4 cores.
The number of iterations can be changed by modifying the 
experiments dict in `scripts/main.py`.

After installing, MMD can be used on any sequential two-player zero-sum 
OpenSpiel game, for example:

```python
from mmd_dilated import mmd_dilated
import pyspiel

game = pyspiel.load_game("kuhn_poker")
mmd = mmd_dilated.MMDDilatedEnt(game, alpha=0.1)

for i in range(100):
    mmd.update_sequences() # perform update
    mmd.get_policies() # extract behavioural form policies
    mmd.current_sequences() # get current sequence form policy
    mmd.get_gap() # compute saddle point gap
```

## Code Structure

MMD is implemented in [NumPy](https://numpy.org/) with [OpenSpiel](https://github.com/deepmind/open_spiel).
The source code can be found within the directory `mmd_dilated`.
There are two main files, `mmd_dilated/sequence_form_utils.py` includes various helpful sequence form 
functions, `mmd_dilated/mmd_dilated.py` implements the algorithm and main update loop.


## Citing

If you use this repository in your research, please cite the 
paper using the following BibTeX:

```
@misc{mmd_paper,
  doi = {10.48550/ARXIV.2206.05825},
  url = {https://arxiv.org/abs/2206.05825}, 
  author = {Sokota, Samuel and D'Orazio, Ryan and Kolter, J. Zico and Loizou, Nicolas and Lanctot, Marc and Mitliagkas, Ioannis and Brown, Noam and Kroer, Christian},  
  title = {A Unified Approach to Reinforcement Learning, Quantal Response Equilibria, and Two-Player Zero-Sum Games},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```
