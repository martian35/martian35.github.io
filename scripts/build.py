#!/usr/bin/env python3
"""Build the portfolio with Python's standard library; no web framework required."""
import html
import hashlib
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
PROFILE_IMAGE = 'portrait-original.jpg' if not OPTIONS.public or PUBLICATION.get('profile_photo', False) else 'profile-mark.svg'
ORIGIN = 'https://martian35.github.io'
STYLE_PATH = ROOT / 'style.css' if OPTIONS.github_root else ROOT / 'dist/style.css'
STYLE_REVISION = hashlib.sha256(STYLE_PATH.read_bytes()).hexdigest()[:12]


def esc(value):
    return html.escape(str(value), quote=True)


def anchor(label, url, cls=''):
    external = url.startswith(('https://', 'http://'))
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a href="{esc(url)}" class="{esc(cls)}"{attrs}>{esc(label)}</a>'


def head(title, description, path='', prefix=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#ffffff"><link rel="canonical" href="{ORIGIN}/{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{ORIGIN}/{path}"><meta property="og:image" content="{ORIGIN}/assets/{PROFILE_IMAGE}"><meta name="twitter:card" content="summary">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css?v={STYLE_REVISION}">
<script src="{prefix}site.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>'''


def header(prefix=''):
    home = prefix or './'
    return f'<header class="site-header"><a href="{home}">Dong Hwi Kim</a><nav aria-label="Main navigation"><a href="{home}#research">Research</a> / <a href="{home}#projects">Projects</a> / <a href="{home}#experience">Experience</a></nav></header>'


def footer(prefix=''):
    return f'<footer class="site-footer"><p>Layout inspired by {anchor("Jon Barron", "https://jonbarron.info/")}.</p><p>Updated {esc(PERSON["updated"])}</p></footer></body></html>'


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
    thumbnail = item.get('thumbnail_url') or 'assets/' + item.get('thumbnail', item['image'])
    fallback = f' data-fallback="assets/{esc(item["image"])}" data-fallback-alt="{esc(item["image_alt"])}"' if item.get('thumbnail_url') else ''
    badge = item['status'] if research else item['badge']
    role = '<p class="work-role"><strong>My role:</strong> '+esc(item['card_role'])+'</p>' if item.get('card_role') else ''
    credit = '<p class="thumbnail-credit">'+anchor(item['thumbnail_source_label'],item['thumbnail_source_url'])+'</p>' if item.get('thumbnail_source_url') else ''
    return f'''<article class="work-row">
<div class="work-media"><a class="work-image {esc(item['id'])}" href="projects/{item['id']}/" tabindex="-1" aria-hidden="true"><img src="{esc(thumbnail)}" alt="{esc(item.get('thumbnail_alt',item['image_alt']))}" width="160" height="120" loading="lazy" referrerpolicy="no-referrer"{fallback}></a>{credit}</div>
<div class="work-copy"><p class="work-category">{esc(item['category'])}</p><h3><a href="projects/{item['id']}/">{esc(item['title'])}</a></h3>
<p class="work-meta">{esc(item['eyebrow'])} · {esc(item['date'])} · <em>{esc(badge)}</em></p>
<p class="work-description">{esc(item['summary'])}</p>{role}{item_links(item)}</div></article>'''


def profile_portrait():
    if PROFILE_IMAGE == 'portrait-original.jpg':
        # Keep the framing in the HTML as well as CSS so stale styles cannot
        # expose the uncropped photograph while the new stylesheet loads.
        frame_style = 'position:relative;width:var(--portrait-size,210px);max-width:100%;height:auto;aspect-ratio:1/1;border-radius:50%;overflow:hidden;flex:none'
        image_style = 'position:absolute;width:600%;height:800%;max-width:none;left:-280.555556%;top:-408.333333%;object-fit:fill;border-radius:0'
        return f'<figure class="portrait original-photo" style="{frame_style}"><img src="assets/{PROFILE_IMAGE}" width="1080" height="1440" alt="Dong Hwi Kim" fetchpriority="high" style="{image_style}"></figure>'
    return f'<figure class="portrait"><img src="assets/{PROFILE_IMAGE}" width="210" height="210" alt="Dong Hwi Kim" fetchpriority="high"></figure>'


def home():
    p = PERSON
    bio = esc(p['bio'])
    for label, url in [('RPM Robotics Lab', 'https://rpm.snu.ac.kr/'), ('AIDAS Lab', 'https://aidas.snu.ac.kr/')]:
        bio = bio.replace(label, anchor(label, url))
    body = head('Dong Hwi Kim | Robotics & 3D Vision', p['intro'])
    body += f'''<main id="main" class="home-main">
<section class="intro" aria-labelledby="name"><div class="intro-copy">
<h1 id="name">Dong Hwi Kim</h1>
<p class="academic-program"><strong>SEOUL NATIONAL UNIVERSITY</strong><br>Mechanical Engineering<br>Electrical and Computer Engineering</p>
<p>{esc(p['intro'])}</p><p>{bio}</p>
<p class="profile-links">{anchor('Email', 'mailto:'+p['email'])} / {anchor('GitHub',p['github'])} / {anchor('LinkedIn',p['linkedin'])}</p>
</div>{profile_portrait()}</section>
<section class="research-approach" aria-labelledby="approach-title"><h2 id="approach-title">How I approach research</h2>{''.join('<p>'+esc(t)+'</p>' for t in p.get('approach', []))}</section>
<section id="research" class="section" aria-labelledby="research-title"><h2 id="research-title">Research</h2>
<p class="section-intro">{esc(DATA.get('research_intro', 'Ongoing projects in 3D mapping and visual data augmentation for robot learning.'))}</p>
<div class="work-list">{''.join(row(x,True) for x in DATA['research'])}</div></section>
<section id="projects" class="section" aria-labelledby="projects-title"><h2 id="projects-title">Selected Projects</h2>
<p class="section-intro">{esc(DATA.get('projects_intro', 'Engineering and machine learning projects, with implementation details, design decisions, and results on each project page.'))}</p>
<div class="work-list">{''.join(row(x) for x in DATA['projects'])}</div></section>
<section id="experience" class="section" aria-labelledby="experience-title"><h2 id="experience-title">Experience &amp; Education</h2><div class="timeline">'''
    for x in DATA['experience']:
        org = anchor(x['organization'], x['url']) if x.get('url') else esc(x['organization'])
        body += f'<article class="timeline-row"><p class="timeline-date">{esc(x["date"])}</p><div><h3>{esc(x["title"])}</h3><p>{org}</p><p class="muted">{esc(x["detail"])}</p></div></article>'
    body += '<article class="timeline-row"><p class="timeline-date">Education</p><div><h3>Seoul National University</h3><p>Mechanical Engineering<br>Electrical and Computer Engineering</p></div></article></div></section>'
    body += '<section id="honors" class="section" aria-labelledby="honors-title"><h2 id="honors-title">Selected Honors</h2>'
    for label, group in [('Engineering competitions', [a for a in DATA['awards'] if not a['type'].startswith('Military')]), ('Military recognition', [a for a in DATA['awards'] if a['type'].startswith('Military')])]:
        if not group: continue
        body += f'<h3 class="honors-heading">{esc(label)}</h3><ul class="honors-list">'
        for a in group:
            body += f'<li><span class="honor-year">{esc(a["year"])}</span> <strong>{esc(a["title"])}</strong> — {esc(a["event"])}</li>'
        body += '</ul>'
    body += '</section>'
    if DATA.get('service'):
        body += f'''<section id="military" class="section military-section" aria-labelledby="military-title"><h2 id="military-title">Military Service &amp; Recognition</h2><p>{esc(DATA['service']['summary'])}</p><figure class="military-photo"><a href="assets/service-honors.jpg" target="_blank" rel="noopener noreferrer"><img src="assets/service-honors.jpg" alt="Joint Service Achievement Medal certificate, ROK Army commendations, and military challenge coins" width="1800" height="1013" loading="lazy"></a><figcaption>Decorations, commendations and challenge coins. {anchor('View full-size photograph','assets/service-honors.jpg')}</figcaption></figure></section>'''
    return body + '</main>' + footer()


def project_figure(g):
    src = g.get('url') or '../../assets/' + g['image']
    source = ' ' + anchor(g.get('source_label', 'Source'), g['source_url']) if g.get('source_url') else ''
    dimensions = f' width="{int(g["width"])}" height="{int(g["height"])}"' if g.get('width') and g.get('height') else ''
    fallback = f' data-fallback="../../assets/{esc(g["fallback"])}" data-fallback-alt="{esc(g["alt"])}"' if g.get('fallback') else ''
    return f'''<figure class="project-figure {esc(g.get('layout',''))}"><a href="{esc(src)}" target="_blank" rel="noopener noreferrer" aria-label="{esc('Open full-size figure: '+g['alt'])}"><img src="{esc(src)}" alt="{esc(g['alt'])}"{dimensions} loading="lazy" referrerpolicy="no-referrer"{fallback}></a><figcaption>{esc(g['caption'])}{source} {anchor('Open full-size figure',src)}</figcaption></figure>'''


def project_section(s, index=None):
    section_id = f' id="decision-{index}"' if index is not None else ''
    out = f'<section{section_id}><h2>{esc(s["heading"])}</h2><p>{esc(s["body"])}</p>'
    if s.get('figure'):
        out += project_figure(s['figure'])
    if s.get('sources'):
        out += '<p class="credit">Sources: ' + ' · '.join(anchor(r['label'], r['url']) for r in s['sources']) + '</p>'
    return out + '</section>'


def project(item, research=False):
    title = item['title']
    body = head(title+' | Dong Hwi Kim',item['summary'],f'projects/{item["id"]}/','../../')+header('../../')
    badge = item['status'] if research else item['badge']
    body += f'''<main id="main" class="detail-main"><a class="back-link" href="../../#{'research' if research else 'projects'}">← Back to {'research' if research else 'projects'}</a>
<header class="project-heading"><p class="work-category">{esc(item['category'])}</p><h1>{esc(title)}</h1><p class="overline">{esc(item['eyebrow'])} · {esc(item['date'])}</p><span class="{'status' if research else 'badge'}">{esc(badge)}</span><p class="project-deck">{esc(item['summary'])}</p>{tags(item)}{item_links(item,True)}</header>'''
    if item.get('at_glance'):
        body += '<section class="project-glance" aria-labelledby="glance-title"><h2 id="glance-title">At a glance</h2><dl>'
        for fact in item['at_glance']:
            body += f'<div><dt>{esc(fact["label"])}</dt><dd>{esc(fact["text"])}</dd></div>'
        body += '</dl></section>'
    body += '<nav class="detail-contents" aria-label="On this page"><a href="#how-it-works">How it works</a> / <a href="#engineering">Engineering decisions</a> / <a href="#implementation">Implementation &amp; evidence</a></nav>'
    hero = item.get('hero_image', item['image'])
    hero_alt = item.get('hero_alt', item['image_alt'])
    dims = f'width="{item.get("hero_width",1100)}" height="{item.get("hero_height",640)}"'
    body += f'<figure class="project-hero {esc(item["id"])}"><a href="../../assets/{esc(hero)}" target="_blank" rel="noopener noreferrer" aria-label="{esc("Open full-size figure: "+hero_alt)}"><img src="../../assets/{esc(hero)}" alt="{esc(hero_alt)}" {dims} fetchpriority="high"></a>'
    if item.get('hero_caption'):
        body += '<figcaption>'+esc(item['hero_caption'])+' '+anchor('Open full-size figure','../../assets/'+hero)+'</figcaption>'
    elif item.get('illustrative'):
        body += '<figcaption>Research concept illustration.</figcaption>'
    body += '</figure>'
    if item.get('flow'):
        body += f'<section id="how-it-works" class="workflow-section" aria-labelledby="workflow-title"><h2 id="workflow-title">{esc(item["flow_title"])}</h2><figure class="workflow"><ol class="process-flow">'
        for i, stage in enumerate(item['flow'],1):
            body += f'<li><span class="step-index" aria-hidden="true">{i:02d}</span><h3>{esc(stage["title"])}</h3><p>{esc(stage["body"])}</p></li>'
        body += '</ol><figcaption>'+esc(item['flow_caption'])+'</figcaption></figure></section>'
    if item.get('metrics'):
        body += '<dl class="metrics">'+''.join(f'<div><dt>{esc(m["label"])}</dt><dd>{esc(m["value"])}</dd></div>' for m in item['metrics'])+'</dl>'
    if item.get('role') and not item.get('at_glance'):
        body += f'<aside class="contribution"><span class="tiny-label">My role</span><p>{esc(item["role"])}</p></aside>'
    body += '<div class="project-body"><h2 id="engineering" class="section-marker">Engineering decisions</h2>'
    for i, s in enumerate(item['sections'],1):
        body += project_section(s,i)
    if item.get('connection'):
        body += '<aside class="research-connection"><h2>How this connects to my current research</h2><p>'+esc(item['connection'])+'</p>'
        related = {x['id']: x for x in DATA['research'] + DATA['projects']}
        body += '<p class="related-links">' + ' / '.join(anchor(related[k]['title'], '../'+k+'/') for k in item.get('related', [])) + '</p></aside>'
    if item.get('technical_notes'):
        body += '<details class="implementation" id="implementation"><summary>'+esc(item.get('technical_notes_title','Implementation notes & source evidence'))+'</summary><div class="implementation-body">'
        for s in item['technical_notes']:
            body += project_section(s)
        body += '</div></details>'
    if item.get('gallery'):
        body += '<section class="gallery"><h2>Inside the project</h2>'
        for g in item['gallery']:
            body += project_figure(g)
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
