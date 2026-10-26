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

## Editing the first-steps notebook

Don't edit `phlex-first-steps.ipynb` by hand. Edit the cells in `build_nb.py`, then run:

```bash
python3 build_nb.py
```

The cell IDs are fixed, so the same script gives a byte-identical notebook and the diffs stay small.

## Credits

Notebooks by Gavin S. Davies (University of Mississippi). The comics in `figures/xkcd/` are by
Randall Munroe, [xkcd.com](https://xkcd.com), under CC BY-NC 2.5.
