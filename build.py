#!/usr/bin/env python3
"""
Build script for advstatcomp-python.

Executes the source notebooks in notebooks/, copies them to
docs/chapters/, then builds (or serves/deploys) the mkdocs site.

Usage:
    python build.py              # Execute notebooks + build site  →  site/
    python build.py --serve      # Execute notebooks + serve locally (hot-reload)
    python build.py --site       # Skip execution, just rebuild the mkdocs site
    python build.py --deploy     # Execute notebooks + deploy to gh-pages branch
    python build.py --chapter ch07_background  # Only (re)execute one notebook
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT        = Path(__file__).parent
NB_SRC      = ROOT / "notebooks"                   # source notebooks
CHAPTERS    = ROOT / "docs" / "chapters"            # executed notebooks land here
TIMEOUT     = 600   # seconds per notebook


# ---------------------------------------------------------------------------
# Notebook execution
# ---------------------------------------------------------------------------

def execute_notebook(nb_path: Path, timeout: int = TIMEOUT) -> tuple[Path, bool, float, str]:
    """Execute a single notebook in-place, writing the result to docs/chapters/."""
    dest = CHAPTERS / nb_path.name
    t0 = time.time()
    try:
        from nbconvert.preprocessors import ExecutePreprocessor
        import nbformat

        with open(nb_path) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=timeout, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": str(nb_path.parent)}})

        CHAPTERS.mkdir(parents=True, exist_ok=True)
        with open(dest, "w") as f:
            nbformat.write(nb, f)

        elapsed = time.time() - t0
        return nb_path, True, elapsed, ""
    except Exception as exc:
        elapsed = time.time() - t0
        # Copy unexecuted notebook so a later --site run has something to render
        shutil.copy2(nb_path, dest)
        return nb_path, False, elapsed, str(exc)


def execute_all(chapter_filter: str | None = None, workers: int = 4) -> tuple[int, int]:
    """Execute all (or one) notebook(s) in parallel. Returns (ok, failed)."""
    notebooks = sorted(NB_SRC.glob("ch*.ipynb"))
    if chapter_filter:
        notebooks = [n for n in notebooks if chapter_filter in n.stem]
        if not notebooks:
            print(f"No notebook matching '{chapter_filter}' found.")
            sys.exit(1)

    print(f"Executing {len(notebooks)} notebook(s) with {workers} worker(s)...")
    ok = failed = 0

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(execute_notebook, nb): nb for nb in notebooks}
        for fut in as_completed(futures):
            nb_path, success, elapsed, err = fut.result()
            status = "✓" if success else "✗"
            print(f"  {status} {nb_path.name}  ({elapsed:.1f}s)")
            if not success:
                print(f"    Error: {err[:200]}")
                failed += 1
            else:
                ok += 1

    return ok, failed


# ---------------------------------------------------------------------------
# mkdocs commands
# ---------------------------------------------------------------------------

def mkdocs_build():
    result = subprocess.run(["mkdocs", "build"], cwd=ROOT)
    if result.returncode != 0:
        print("mkdocs build failed.")
        sys.exit(result.returncode)


def mkdocs_serve():
    subprocess.run(["mkdocs", "serve"], cwd=ROOT)


def mkdocs_deploy():
    """Deploy to the gh-pages branch of the GitHub remote."""
    result = subprocess.run(["mkdocs", "gh-deploy", "--force"], cwd=ROOT)
    if result.returncode != 0:
        print("mkdocs gh-deploy failed.")
        sys.exit(result.returncode)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site",    action="store_true",
                        help="Skip notebook execution; just rebuild the mkdocs site.")
    parser.add_argument("--serve",   action="store_true",
                        help="Serve the site locally after building (development mode).")
    parser.add_argument("--deploy",  action="store_true",
                        help="Deploy to GitHub Pages via mkdocs gh-deploy.")
    parser.add_argument("--chapter", metavar="NAME",
                        help="Only execute the notebook whose name contains NAME.")
    parser.add_argument("-j", "--jobs", type=int, default=4,
                        help="Parallel notebook execution workers (default: 4).")
    args = parser.parse_args()

    CHAPTERS.mkdir(parents=True, exist_ok=True)

    if not args.site:
        ok, failed = execute_all(chapter_filter=args.chapter, workers=args.jobs)
        print(f"\nExecution complete: {ok} succeeded, {failed} failed.")
        if failed:
            print(f"\n{failed} notebook(s) failed; aborting before mkdocs build.")
            sys.exit(1)

    if args.deploy:
        mkdocs_deploy()
    elif args.serve:
        mkdocs_serve()
    else:
        mkdocs_build()
        print(f"\nSite built → {ROOT / 'site'}/")
        print("To deploy to GitHub Pages: python build.py --deploy")


if __name__ == "__main__":
    main()
