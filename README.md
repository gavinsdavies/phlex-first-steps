# Phlex first steps

Two Jupyter notebooks for the hands-on Phlex sessions at the DUNE workshop at IISc Bengaluru
(October 26 to 30, 2026).

| Notebook | Time | What it covers |
|---|---|---|
| `phlex-first-steps.ipynb` | about 2 hours | Terminal, fork and clone, a CMake warm-up, building and running the Phlex examples, a first look at FORM, then a pull request and a review |
| `phlex-examples-tutorial.ipynb` | longer | The deep dive: CMake targets and plugins, unfolds, undoing mistakes with git, a Python observer, and a mock neutrino analysis with plots |

The first-steps notebook works in
[nuRiceLab/dune-tech-phlex-sandbox](https://github.com/nuRiceLab/dune-tech-phlex-sandbox), a practice
repository that includes the official
[Framework-R-D/phlex-examples](https://github.com/Framework-R-D/phlex-examples) as a submodule.
The deep dive clones phlex-examples directly.

Both expect the workshop's JupyterHub and its `phaindia` apptainer kernel, which provides Phlex.

## If you are using the DUNE Tech JupyterHub

Log in with GitHub at [![DUNE Tech JupyterHub](https://img.shields.io/badge/Log%20in-DUNE%20Tech%20JupyterHub-F37626?logo=jupyter&logoColor=white)](https://dune-tech.rice.edu/jupyterhub/), then click a button to clone this repository into your session and open the notebook:

[![Open first steps](https://img.shields.io/badge/Open-phlex--first--steps-2EA44F?logo=git&logoColor=white)](https://dune-tech.rice.edu/jupyterhub/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fgavinsdavies%2Fphlex-first-steps&branch=main&urlpath=lab%2Ftree%2Fphlex-first-steps%2Fphlex-first-steps.ipynb)
[![Open the deep dive](https://img.shields.io/badge/Open-phlex--examples--tutorial-2EA44F?logo=git&logoColor=white)](https://dune-tech.rice.edu/jupyterhub/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fgavinsdavies%2Fphlex-first-steps&branch=main&urlpath=lab%2Ftree%2Fphlex-first-steps%2Fphlex-examples-tutorial.ipynb)

Choose the **phaindia apptainer** kernel when the notebook opens. To present a notebook as slides,
press **Alt+R** (needs `jupyterlab-rise` on the hub).

## Editing the first-steps notebook

Don't edit `phlex-first-steps.ipynb` by hand. Edit the cells in `build_nb.py`, then run:

```bash
python3 build_nb.py
```

The cell IDs are fixed, so the same script gives a byte-identical notebook and the diffs stay small.

## Credits and license

Notebooks by Gavin S. Davies (University of Mississippi). The notebooks and `build_nb.py` are under
the Apache License 2.0 (see `LICENSE`), like other DUNE software. The comics in `figures/xkcd/` are
not: they are by Randall Munroe, [xkcd.com](https://xkcd.com), under CC BY-NC 2.5.
