#!/usr/bin/env python3
"""Export the public portfolio without private photographs or attached PDFs."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path)
parser.add_argument('--include-service-experience', action='store_true')
args = parser.parse_args()
target = args.destination.resolve()
if target == ROOT or ROOT in target.parents:
    raise SystemExit('Choose an export destination outside the source checkout.')
if target.exists() and any(target.iterdir()):
    raise SystemExit('Choose a new, empty export destination.')
target.mkdir(parents=True, exist_ok=True)
command = [sys.executable, str(ROOT/'scripts/build.py'), '--public', '--output', str(target)]
if args.include_service_experience:
    command += ['--include-service-experience']
subprocess.run(command, check=True)
for name in ['style.css', 'site.js']:
    shutil.copy2(ROOT/'dist'/name, target/name)
(target/'assets').mkdir(exist_ok=True)
for asset in (ROOT/'dist/assets').iterdir():
    if asset.is_file() and asset.name not in {'portrait.jpg', 'service-honors.jpg'}:
        shutil.copy2(asset, target/'assets'/asset.name)
shutil.copytree(ROOT/'scripts', target/'scripts', ignore=shutil.ignore_patterns('__pycache__'))
for name in ['image-sources.json']:
    if (ROOT/'content'/name).exists():
        shutil.copy2(ROOT/'content'/name, target/'content'/name)
(target/'README.md').write_text('''# Dong Hwi Kim — academic portfolio

Seoul National University undergraduate, double majoring in Mechanical Engineering and Electrical and Computer Engineering.

## Update the site

1. Edit `content/portfolio.json`.
2. Run `python3 scripts/build.py --public --github-root`.
3. Run `python3 scripts/check.py --github-root`.
4. Commit the generated HTML and the updated content together.

The static site has no build dependencies beyond Python 3. CSS is in `style.css` and the project filter and image fallback are in `site.js`.

The ongoing research entries can be updated with results, paper links, and publication details as work progresses. Their current status labels do not imply acceptance or publication.

## Images and provenance

See `content/image-sources.json` for official pages, image URLs, and selection decisions. Source links are also shown next to official competition images. Remote photographs fall back to a local project image if unavailable. Original Zephyr Analytics slides were supplied by the user. The course figures and Automated Filming Device imagery are team project materials. The SLAM and scene-ordering diagrams are conceptual explanations.

Project materials retain their respective ownership. The original HTML/CSS layout draws on the supplied academic portfolio references.

GitHub Pages serves the `main` branch at https://martian35.github.io/.
''')
(target/'.gitignore').write_text('__pycache__/\n*.pyc\n.DS_Store\n')
subprocess.run([sys.executable, str(target/'scripts/check.py'), '--github-root'], check=True)
print(f'Public export: {target}')
