# Dong Hwi Kim — academic portfolio

Seoul National University undergraduate, double majoring in Mechanical Engineering and Electrical and Computer Engineering.

## Update the site

1. Edit `content/portfolio.json`.
2. Run `python3 scripts/build.py --public --github-root`.
3. Run `python3 scripts/check.py --github-root`.
4. Commit the generated HTML and the updated content together.

The static site has no build dependencies beyond Python 3. The classic academic layout uses Lato in `style.css`; remote-image fallbacks are handled by `site.js`.

The ongoing research entries can be updated with results, paper links, and publication details as work progresses. Their current status labels do not imply acceptance or publication.

Each detail page has an at-a-glance overview, a responsive workflow figure, engineering decisions, and expandable implementation notes. Update these through `content/portfolio.json`; the editorial rationale and future figure guidance are in `content/editorial-notes.md`.

## Images and provenance

See `content/image-sources.json` for official pages, image URLs, and selection decisions. Source links are also shown next to official competition images. Remote photographs fall back to a local project image if unavailable. Original Zephyr Analytics slides were supplied by the user. The course figures and Automated Filming Device imagery are team project materials. The SLAM and scene-ordering diagrams are conceptual explanations.

Project materials retain their respective ownership. The classic academic layout is inspired by Jon Barron (https://jonbarron.info/), with custom responsive styling and project detail pages.

GitHub Pages serves the `main` branch at https://martian35.github.io/.
