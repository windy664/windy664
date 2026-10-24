"""Render the blue-and-white profile with a quiet sky illustration."""
from pathlib import Path
from html import escape
import json
import textwrap

OUT = Path(__file__).resolve().parents[1] / 'assets'
DATA = json.loads((OUT / 'profile-data.json').read_text())


def text(x, y, value, size, color, weight=400, family='Arial,Helvetica,sans-serif', extra=''):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def save(name, width, height, title, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n'
    (OUT / name).write_text(svg)


for theme in ('light', 'dark'):
    dark = theme == 'dark'
    ink = '#e6f0f8' if dark else '#1e3d50'
    muted = '#b1c5d2' if dark else '#5a7483'
    blue = '#86c8e9' if dark else '#287fa9'
    background = '#132635' if dark else '#eef7fc'
    sky = '#1b3849' if dark else '#deeff8'
    cloud = '#294b5d' if dark else '#f5fbff'
    header = f'''<defs><clipPath id="sky"><path d="M605 0H840V210H550Z"/></clipPath></defs>
<rect width="840" height="210" fill="{background}"/>
<g clip-path="url(#sky)">
<rect x="550" width="290" height="210" fill="{sky}"/>
<path d="M642 76c2-12 15-18 26-13 2-21 32-29 44-10 14-8 30 1 30 14 13-3 23 1 27 9Z" fill="{cloud}"/>
<path d="M758 34c3-13 18-18 29-11 2-18 25-24 36-11 11-6 23-1 26 10l12 12Z" fill="{cloud}" opacity=".65"/>
<g fill="none" stroke="{blue}" stroke-linecap="round">
<path d="M566 175C657 126 714 206 852 137" stroke-opacity=".18"/>
<path d="M556 190C648 141 726 221 852 157" stroke-opacity=".12"/>
<path d="M576 159C665 113 713 190 850 119" stroke-opacity=".1"/>
<path d="M708 108q6-6 12 0 6-6 12 0" stroke-width="1.4" stroke-opacity=".6"/>
<path d="M750 94q4-4 8 0 4-4 8 0" stroke-width="1.2" stroke-opacity=".4"/>
</g>
</g>
<style>
@keyframes breeze{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(8px)}}}}
.breeze{{animation:breeze 6s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
@media(max-width:500px){{.small{{display:none}}.name{{font-size:108px}}.caption{{font-size:24px}}}}
</style>'''
    header += text(28, 31, 'TORINE / WINDY664', 11, blue, 600, extra='class="small" letter-spacing="2"')
    header += text(24, 119, 'Torine', 88, ink, 400, 'Georgia,Times New Roman,serif', 'class="name"')
    header += text(29, 158, 'Minecraft plugins, small tools, photos & videos.', 17, muted, extra='class="caption"')
    current = ' + '.join(textwrap.shorten(item['name'], width=22, placeholder='…') for item in DATA['projects'])
    header += text(29, 190, 'Currently: ' + current, 11, blue, extra='class="small"')
    header += f'<g transform="translate(473 51)"><g class="breeze"><path d="M0 3q9-9 18 0 9-9 18 0" fill="none" stroke="{blue}" stroke-width="1.8" stroke-linecap="round"/></g></g>'
    save(f'compact-header-{theme}.svg', 840, 210, 'Torine / windy664 — ' + current, header)

    links = {
        'blog': ('Blog', 88, '<path d="M5 3h12a2 2 0 0 1 2 2v16H6a3 3 0 0 1-3-3V5a2 2 0 0 1 2-2Zm-2 15a3 3 0 0 1 3-3h13M7 7h8M7 10h6"/>'),
        'code': ('Code', 92, '<path d="m7 6-6 6 6 6m10-12 6 6-6 6M14 3l-4 18"/>'),
        'rss': ('RSS', 76, '<circle cx="4" cy="20" r="1"/><path d="M3 11a10 10 0 0 1 10 10M3 3a18 18 0 0 1 18 18"/>'),
    }
    for key, (label, width, icon) in links.items():
        body = f'<g transform="translate(1 6) scale(.67)" fill="none" stroke="{blue}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
        body += text(25, 19, label, 14, ink)
        save(f'profile-link-{key}-{theme}.svg', width, 28, label, body)

    for kind in ('projects', 'posts'):
        for index, item in enumerate(DATA[kind]):
            is_project = kind == 'projects'
            title = item['name'] if is_project else item['title']
            body = f'<path d="M0 1H398" stroke="{blue}" stroke-opacity=".4"/>'
            label = item['language'] if is_project else item['date_label'] + ' / BLOG · ' + item['source_language'].upper()
            body += text(0, 22, label.upper(), 10, muted, 500, extra='letter-spacing="1.3"')
            title_lines = [textwrap.shorten(title, width=24, placeholder='…')] if is_project else textwrap.wrap(title, 32, max_lines=2, placeholder='…')
            for row, line in enumerate(title_lines):
                body += text(0, 53 + row * 23, line, 27 if is_project else 19, ink, 600)
            if is_project:
                for row, line in enumerate(textwrap.wrap(item['summary'], 48, max_lines=2, placeholder='…')):
                    body += text(0, 79 + row * 17, line, 13, muted)
            body += text(386, 52, '↗', 22, blue)
            save(f'profile-{kind}-{index}-{theme}.svg', 410, 106, title, body)
