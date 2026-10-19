"""Render the blue-and-white profile chosen from preview A.

The avatar is stored locally so every SVG is self-contained and reproducible.
Original avatar: https://avatars.githubusercontent.com/u/81475218?v=4
"""
from pathlib import Path
from html import escape
import base64
import json
import textwrap

OUT = Path(__file__).resolve().parents[1] / 'assets'
DATA = json.loads((OUT / 'profile-data.json').read_text())
AVATAR = 'data:image/png;base64,' + base64.b64encode((OUT / 'torine-avatar.png').read_bytes()).decode()


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
    header = f'''<defs><clipPath id="photo"><path d="M605 0H840V210H550Z"/></clipPath></defs>
<rect width="840" height="210" fill="{background}"/>
<image href="{AVATAR}" x="544" y="-28" width="296" height="296" clip-path="url(#photo)"/>
<path d="M548 210 603 0" stroke="{blue}" stroke-opacity=".25" stroke-width="2"/>
<style>
@keyframes breeze{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(8px)}}}}
.breeze{{animation:breeze 6s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
@media(max-width:500px){{.small{{display:none}}.name{{font-size:108px}}.caption{{font-size:24px}}}}
</style>'''
    header += text(28, 31, 'TORINE / WINDY664', 11, blue, 600, extra='class="small" letter-spacing="2"')
    header += text(24, 119, 'Torine', 88, ink, 400, 'Georgia,Times New Roman,serif', 'class="name"')
    header += text(29, 158, 'Java, Minecraft & things I make for myself.', 17, muted, extra='class="caption"')
    current = ' + '.join(textwrap.shorten(item['name'], width=22, placeholder='…') for item in DATA['projects'])
    header += text(29, 190, 'Currently: ' + current, 11, blue, extra='class="small"')
    header += f'<g transform="translate(473 51)"><g class="breeze"><path d="M0 3q9-9 18 0 9-9 18 0" fill="none" stroke="{blue}" stroke-width="1.8" stroke-linecap="round"/></g></g>'
    save(f'compact-header-{theme}.svg', 840, 210, 'Torine / windy664 — ' + current, header)

    for kind in ('projects', 'posts'):
        for index, item in enumerate(DATA[kind]):
            is_project = kind == 'projects'
            title = item['name'] if is_project else item['title']
            body = f'<path d="M0 1H398" stroke="{blue}" stroke-opacity=".4"/>'
            label = item['language'] if is_project else item['date_label'] + ' / BLOG · ZH'
            body += text(0, 22, label.upper(), 10, muted, 500, extra='letter-spacing="1.3"')
            title_lines = [textwrap.shorten(title, width=24, placeholder='…')] if is_project else textwrap.wrap(title, 32, max_lines=2, placeholder='…')
            for row, line in enumerate(title_lines):
                body += text(0, 53 + row * 23, line, 27 if is_project else 19, ink, 600)
            if is_project:
                for row, line in enumerate(textwrap.wrap(item['summary'], 48, max_lines=2, placeholder='…')):
                    body += text(0, 79 + row * 17, line, 13, muted)
            body += text(386, 52, '↗', 22, blue)
            save(f'profile-{kind}-{index}-{theme}.svg', 410, 106, title, body)
