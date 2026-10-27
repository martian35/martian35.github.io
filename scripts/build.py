#!/usr/bin/env python3
"""Build the portfolio with Python's standard library; no web framework required."""
import html
import json
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARGS = argparse.ArgumentParser(description=__doc__)
ARGS.add_argument('--github-root', action='store_true')
ARGS.add_argument('--public', action='store_true', help='Export according to the publication options in the content file')
ARGS.add_argument('--include-service-experience', action='store_true', help='Include military employment text when explicitly authorized')
ARGS.add_argument('--output', type=Path)
OPTIONS = ARGS.parse_args()
OUT = OPTIONS.output or (ROOT if OPTIONS.github_root else ROOT / 'dist')
DATA = json.loads((ROOT / 'content/portfolio.json').read_text())
PUBLICATION = DATA.get('publication', {})
if OPTIONS.public:
    if not PUBLICATION.get('service_recognition', False):
        DATA.pop('service', None)
    if not (OPTIONS.include_service_experience or PUBLICATION.get('service_experience', False)):
        DATA['experience'] = [x for x in DATA['experience'] if x['title'] != 'Interpreter']
    if not PUBLICATION.get('project_documents', False):
        for item in DATA['research'] + DATA['projects']:
            item['links'] = [x for x in item.get('links', []) if not x['url'].startswith('documents/')]
            for section in item.get('sections', []):
                section['body'] = section['body'].replace(' The original report and presentation are available above.', '')
PERSON = DATA['person']
PROFILE_IMAGE = 'portrait.jpg' if not OPTIONS.public or PUBLICATION.get('profile_photo', False) else 'profile-mark.svg'
ORIGIN = 'https://martian35.github.io'


def esc(value):
    return html.escape(str(value), quote=True)


def anchor(label, url, cls=''):
    external = url.startswith(('https://', 'http://'))
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a href="{esc(url)}" class="{esc(cls)}"{attrs}>{esc(label)}<span aria-hidden="true"> {"↗" if external else "→"}</span></a>'


def head(title, description, path='', prefix=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#faf9f6"><link rel="canonical" href="{ORIGIN}/{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{ORIGIN}/{path}"><meta property="og:image" content="{ORIGIN}/assets/{PROFILE_IMAGE}"><meta name="twitter:card" content="summary">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css">
<script src="{prefix}site.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>'''


def header(prefix=''):
    home = prefix or './'
    return f'''<header class="site-header"><div class="nav-wrap">
<a class="wordmark" href="{home}" aria-label="Dong Hwi Kim, home">DHK<span>.</span></a>
<nav aria-label="Main navigation"><a href="{home}#research">Research</a><a href="{home}#projects">Projects</a><a href="{home}#experience">Experience</a><a href="mailto:{esc(PERSON['email'])}">Contact <span aria-hidden="true">↗</span></a></nav>
</div></header>'''


def footer(prefix=''):
    return f'''<footer class="site-footer"><div><a href="{prefix or './'}">Dong Hwi Kim</a><span>Seoul National University</span></div>
<div><span>Updated {esc(PERSON['updated'])}</span>{anchor('GitHub', PERSON['github'])}</div></footer></body></html>'''


def tags(item):
    return '<ul class="tags" aria-label="Topics">' + ''.join(f'<li>{esc(t)}</li>' for t in item.get('tags', [])) + '</ul>'


def item_links(item, detail=False):
    links = [anchor('Details', f'projects/{item["id"]}/')] if not detail else []
    for link in item.get('links', []):
        url = link['url']
        if detail and not url.startswith(('https://', 'http://')):
            url = '../../' + url
        links.append(anchor(link['label'], url))
    return '<div class="item-links">' + ''.join(links) + '</div>'


def row(item, research=False):
    badge = item['status'] if research else item['badge']
    cl = 'status' if research else ('badge subdued' if item['category']=='Coursework' or item['id']=='scene-reordering' else 'badge')
    label = f'<span class="{cl}">{esc(badge)}</span>'
    thumbnail = item.get('thumbnail_url') or 'assets/' + item.get('thumbnail', item['image'])
    fallback = f' data-fallback="assets/{esc(item["image"])}" data-fallback-alt="{esc(item["image_alt"])}"' if item.get('thumbnail_url') else ''
    credit = '<p class="thumbnail-credit">'+anchor(item['thumbnail_source_label'],item['thumbnail_source_url'])+'</p>' if item.get('thumbnail_source_url') else ''
    return f'''<article class="work-row{' research-row' if research else ''}"{' data-category="'+esc(item['category'])+'"' if not research else ''}>
<div class="work-media"><a class="work-image {esc(item['id'])}{' official-photo' if item.get('thumbnail_url') else ''}" href="projects/{item['id']}/" tabindex="-1" aria-hidden="true"><img src="{esc(thumbnail)}" alt="{esc(item.get('thumbnail_alt',item['image_alt']))}" width="560" height="360" loading="lazy" referrerpolicy="no-referrer"{fallback}></a>{credit}</div>
<div class="work-copy"><div class="work-meta"><span>{esc(item['eyebrow'])} · {esc(item['date'])}</span>{label}</div>
<h3><a href="projects/{item['id']}/">{esc(item['title'])}</a></h3>
<p>{esc(item['summary'])}</p>{tags(item)}{item_links(item)}</div></article>'''


def home():
    p = PERSON
    body = head('Dong Hwi Kim | Robotics & 3D Vision', p['intro']) + header()
    body += f'''<main id="main" class="home-main">
<section class="intro" aria-labelledby="name"><div class="intro-copy">
<p class="overline">Seoul National University</p>
<p class="academic-program">Mechanical Engineering<br>Electrical and Computer Engineering</p>
<h1 id="name">Dong Hwi Kim <span lang="ko">김동휘</span></h1>
<p class="intro-lead">Robotics, 3D vision,<br>and learning from the world.</p>
<p>{esc(p['intro'])}</p><p>{esc(p['bio'])}</p>
<div class="profile-links">{anchor('Email', 'mailto:'+p['email'])}{anchor('GitHub',p['github'])}{anchor('LinkedIn',p['linkedin'])}</div>
</div><figure class="portrait"><img src="assets/{PROFILE_IMAGE}" width="240" height="310" alt="{'Dong Hwi Kim monogram' if PROFILE_IMAGE == 'profile-mark.svg' else 'Dong Hwi Kim'}" fetchpriority="high"><figcaption>Based in Seoul, South Korea</figcaption></figure></section>
<div class="interest-line"><span class="tiny-label">Research interests</span><p>{' <span aria-hidden="true">/</span> '.join(esc(x) for x in p['interests'])}</p></div>
<section id="research" class="section" aria-labelledby="research-title"><div class="section-heading"><div><p class="overline">What I am working on</p><h2 id="research-title">Ongoing research</h2></div><span class="section-aside">3D representations → robot perception</span></div>
<p class="section-intro">My current research explores 3D Gaussian representations for mapping and visual data augmentation for robot learning.</p>
<div class="work-list">{''.join(row(x,True) for x in DATA['research'])}</div></section>
<section id="projects" class="section" aria-labelledby="projects-title"><div class="section-heading"><div><p class="overline">From models to working systems</p><h2 id="projects-title">Selected projects</h2></div><span class="section-aside">2024 — 2026</span></div>
<div class="filters" aria-label="Filter projects" hidden><button type="button" class="active" data-filter="All" aria-pressed="true">All <span>06</span></button><button type="button" data-filter="Robotics" aria-pressed="false">Robotics</button><button type="button" data-filter="Machine Learning" aria-pressed="false">Machine learning</button><button type="button" data-filter="Coursework" aria-pressed="false">Coursework</button></div>
<p class="sr-only" id="filter-result" role="status" aria-live="polite"></p>
<div class="work-list">{''.join(row(x) for x in DATA['projects'])}</div></section>
<section id="experience" class="section" aria-labelledby="experience-title"><div class="section-heading"><div><p class="overline">Where I have been</p><h2 id="experience-title">Experience & education</h2></div></div>
<div class="timeline">'''
    for x in DATA['experience']:
        org = anchor(x['organization'], x['url']) if x.get('url') else esc(x['organization'])
        body += f'<article class="timeline-row"><p class="timeline-date">{esc(x["date"])}</p><div><h3>{esc(x["title"])}</h3><p class="organization">{org}</p><p class="muted">{esc(x["detail"])}</p></div></article>'
    body += '''<article class="timeline-row"><p class="timeline-date">Education</p><div><h3>Seoul National University</h3><p class="organization">Undergraduate · Double major</p><p class="muted">Mechanical Engineering<br>Electrical and Computer Engineering</p></div></article></div></section>
<section id="honors" class="section" aria-labelledby="honors-title"><div class="section-heading"><div><p class="overline">Competitions & service</p><h2 id="honors-title">Selected honors</h2></div></div>'''
    for label, group in [('Engineering competitions', [a for a in DATA['awards'] if not a['type'].startswith('Military')]), ('Military recognition', [a for a in DATA['awards'] if a['type'].startswith('Military')])]:
        if not group:
            continue
        body += f'<div class="honors-group"><h3>{esc(label)}</h3><div class="honors-list">'
        for a in group:
            body += f'<div class="honor-row"><span class="honor-year">{esc(a["year"])}</span><strong>{esc(a["title"])}</strong><span>{esc(a["event"])}</span></div>'
        body += '</div></div>'
    body += '</section>'
    if DATA.get('service'):
        body += f'''<section id="military" class="section military-section" aria-labelledby="military-title"><div class="section-heading"><div><p class="overline">ROK–U.S. Combined Forces Command</p><h2 id="military-title">Military service & recognition</h2></div><span class="section-aside">September 2022 — March 2024</span></div><div class="military-overview"><p>{esc(DATA['service']['summary'])}</p><p class="military-note">Military decorations, formal commendations, and challenge coins from my service are shown below.</p></div><figure class="military-photo"><a href="assets/service-honors.jpg" target="_blank" rel="noopener noreferrer" aria-label="Open the full-size photograph of military medals and commendations"><img src="assets/service-honors.jpg" alt="Joint Service Achievement Medal certificate, ROK Army commendations, and military challenge coins" width="1800" height="1013" loading="lazy"></a><figcaption><span>Decorations, commendations & challenge coins</span>{anchor('View full-size photograph','assets/service-honors.jpg')}</figcaption></figure></section>'''
    body += f'''
<section class="contact-section" aria-labelledby="contact-title"><p class="overline">Get in touch</p><h2 id="contact-title">Let’s talk about research.</h2><p>I’m interested in robotics, 3D vision, and learning-based perception.</p>{anchor(p['email'],'mailto:'+p['email'],'contact-link')}</section></main>'''
    return body + footer()


def project(item, research=False):
    title = item['title']
    body = head(title+' | Dong Hwi Kim',item['summary'],f'projects/{item["id"]}/','../../')+header('../../')
    badge = item['status'] if research else item['badge']
    body += f'''<main id="main" class="detail-main"><a class="back-link" href="../../#{'research' if research else 'projects'}">← Back to {'research' if research else 'projects'}</a>
<header class="project-heading"><p class="overline">{esc(item['eyebrow'])} · {esc(item['date'])}</p><h1>{esc(title)}</h1><span class="{'status' if research else 'badge'}">{esc(badge)}</span><p class="project-deck">{esc(item['summary'])}</p>{tags(item)}{item_links(item,True)}</header>
<figure class="project-hero {esc(item['id'])}"><img src="../../assets/{esc(item['image'])}" alt="{esc(item['image_alt'])}" width="1100" height="640" fetchpriority="high">'''
    if item.get('illustrative'):
        body += '<figcaption>Research concept illustration.</figcaption>'
    body += '</figure>'
    if item.get('metrics'):
        body += '<dl class="metrics">'+''.join(f'<div><dt>{esc(m["label"])}</dt><dd>{esc(m["value"])}</dd></div>' for m in item['metrics'])+'</dl>'
    if item.get('role'):
        body += f'<aside class="contribution"><span class="tiny-label">My role</span><p>{esc(item["role"])}</p></aside>'
    body += '<div class="project-body">'
    for s in item['sections']:
        body += f'<section><h2>{esc(s["heading"])}</h2><p>{esc(s["body"])}</p></section>'
    if item.get('gallery'):
        body += '<section class="gallery"><h2>Inside the project</h2>'
        for g in item['gallery']:
            src = g.get('url') or '../../assets/'+g['image']
            source = ' '+anchor(g['source_label'],g['source_url']) if g.get('source_url') else ''
            fallback = f' data-fallback="../../assets/{esc(g["fallback"])}" data-fallback-alt="{esc(item["image_alt"])}"' if g.get('fallback') else ''
            body += f'<figure><img src="{esc(src)}" alt="{esc(g["alt"])}" loading="lazy" referrerpolicy="no-referrer"{fallback}><figcaption>{esc(g["caption"])}{source}</figcaption></figure>'
        body += '</section>'
    if item.get('credit'):
        body += f'<p class="credit">{esc(item["credit"])}</p>'
    body += '</div><nav class="project-bottom" aria-label="Project navigation"><a href="../../#'+('research' if research else 'projects')+'">← All '+('research' if research else 'projects')+'</a><a href="mailto:'+esc(PERSON['email'])+'">Contact me ↗</a></nav></main>'
    return body + footer('../../')


def main():
    OUT.mkdir(exist_ok=True)
    (OUT/'index.html').write_text(home())
    if OPTIONS.public:
        (OUT/'content').mkdir(exist_ok=True)
        (OUT/'content/portfolio.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
    paths = ['']
    for group in ['research','projects']:
        for item in DATA[group]:
            path = OUT/'projects'/item['id']
            path.mkdir(parents=True,exist_ok=True)
            (path/'index.html').write_text(project(item,group=='research'))
            paths.append(f'projects/{item["id"]}/')
    (OUT/'.nojekyll').write_text('')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+'/'+p+'</loc></url>' for p in paths)+'</urlset>')
    (OUT/'404.html').write_text(head('Page not found | Dong Hwi Kim','This page could not be found.',prefix='/')+header('/')+'<main id="main" class="detail-main error-page"><p class="overline">404</p><h1>Page not found.</h1><p>The page may have moved. You can find my research and projects on the homepage.</p><a href="/">← Back to home</a></main>'+footer('/'))
    print(f'Built homepage and {len(paths)-1} project pages in {OUT}')


if __name__ == '__main__':
    main()
