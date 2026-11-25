#!/usr/bin/env python3
"""Validate generated pages, navigation anchors, local images, and downloads."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT if '--github-root' in sys.argv else ROOT / 'dist'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.refs, self.h1, self.titles = path, set(), [], 0, 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {self.path}: {a["id"]}'
            self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.titles += 1
        if tag == 'img': assert a.get('alt'), f'Missing image alt text in {self.path}'
        if tag == 'button': assert a.get('type') == 'button'
        if tag == 'a' and a.get('target') == '_blank': assert 'noopener' in a.get('rel', '')
        for name in ('href', 'src'):
            if a.get(name): self.refs.append(a[name])


def main():
    files = sorted(OUT.glob('**/*.html'))
    # Exclude an old dist/ copy if checking a root-exported GitHub checkout.
    if OUT == ROOT: files = [p for p in files if 'dist' not in p.relative_to(OUT).parts]
    pages = {p.resolve(): Page(p) for p in files}
    checked = 0
    for p, page in pages.items():
        assert page.h1 == 1 and page.titles == 1, f'Expected one title and one h1 in {p}'
        for ref in page.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc: continue
            path = (OUT / unquote(u.path).lstrip('/')) if u.path.startswith('/') else (p.parent / unquote(u.path))
            if not u.path: path = p
            if path.is_dir(): path = path / 'index.html'
            path = path.resolve()
            assert path.is_relative_to(OUT.resolve()), f'Link escapes website: {p}: {ref}'
            assert path.exists(), f'Missing local link: {p}: {ref}'
            if u.fragment and path in pages: assert unquote(u.fragment) in pages[path].ids, f'Missing anchor: {p}: {ref}'
            checked += 1
    data = json.loads((ROOT / 'content/portfolio.json').read_text())
    assert len(data['research']) == 2 and len(data['projects']) == 6
    paper = data['research'][0]
    assert paper['status'] == 'Under Review' and paper['venue'] == 'CVPR' and paper['year'] == 2027
    assert paper['abstract_only'] and paper['abstract']
    paper_links = {
        'arXiv': 'https://arxiv.org/abs/2611.32025',
        'PDF': 'https://arxiv.org/pdf/2611.32025',
    }
    assert {link['label']: link['url'] for link in paper['links']} == paper_links
    assert not paper['public_method']
    home = (OUT / 'index.html').read_text()
    publication = home.split('id="publication-gaussian-slam"', 1)[1].split('</article>', 1)[0]
    assert '<summary>Abs' in publication and '<details class="publication-abstract">' in publication
    for url in paper_links.values():
        assert f'href="{url}"' in publication, f'Missing publication link: {url}'
    paper_page = (OUT / 'projects/gaussian-slam/index.html').read_text()
    assert 'id="abstract"' in paper_page and 'id="methodology"' not in paper_page
    for url in paper_links.values():
        assert f'href="{url}"' in paper_page, f'Missing paper-page link: {url}'
    assert all('SNU AI Challenge' != a['event'] for a in data['awards'])
    assert (OUT / '.nojekyll').exists()
    assert len(pages) == 10, f'Expected 10 HTML pages including 404, got {len(pages)}'
    print(f'PASS: {len(pages)} HTML pages, {checked} local resources/anchors, research status and honors')


if __name__ == '__main__':
    main()
