# Dong Hwi Kim — academic portfolio

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
