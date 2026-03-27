# Advanced Statistical Computing with Python

A Python port of Roger Peng's [Advanced Statistical Computing](https://bookdown.org/rdpeng/advstatcomp/), originally written in R. All examples are implemented using NumPy, SciPy, and Matplotlib.

## Setup

```bash
pip install -r requirements.txt
```

## Building the site

```bash
# Execute all notebooks and build the site → site/
python build.py

# Execute notebooks and serve locally with hot-reload (for development)
python build.py --serve

# Skip notebook execution, just rebuild the mkdocs site
python build.py --site

# Re-execute a single notebook (faster iteration when editing one chapter)
python build.py --chapter ch07_background

# Run with more parallel workers (default is 4)
python build.py -j 8
```

## Deploying to GitHub Pages

Once the repo has a GitHub remote, deploy to the `gh-pages` branch with:

```bash
python build.py --deploy
```

This runs `mkdocs gh-deploy --force` which builds the site and pushes it to `gh-pages` automatically.

## Project structure

```
notebooks/          # Source notebooks (edit these)
plotting.py         # Shared matplotlib styling
data/               # Data files used by the notebooks
docs/               # Static site assets (index, CSS, JS)
mkdocs.yml          # Site configuration
build.py            # Build script
```

The build script executes notebooks from `notebooks/advstatcomp/` and writes the results to `docs/chapters/`, which is gitignored. Only source files are tracked in version control.