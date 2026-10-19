"""Generate animated, self-contained SVG artwork for the GitHub profile."""
from pathlib import Path
from html import escape
import json
import textwrap

OUT = Path(__file__).resolve().parents[1] / 'assets'
data = json.loads((OUT / 'profile-data.json').read_text())
PALETTES = {
    'light': {'bg': '#f7f9ff', 'ink': '#17213e', 'muted': '#52617c', 'line': '#dce2ef', 'purple': '#7251bf', 'teal': '#087f83', 'pink': '#bd427a', 'orange': '#a95921'},
    'dark': {'bg': '#10182b', 'ink': '#f1f4ff', 'muted': '#b3c1da', 'line': '#2b3956', 'purple': '#b79aff', 'teal': '#67e3db', 'pink': '#ff9aca', 'orange': '#ffc28c'},
}
MOTION = '''<style>
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(-24px,12px)}}
@keyframes rise{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes breathe{0%,100%{opacity:.45}50%{opacity:1}}
@keyframes flow{to{stroke-dashoffset:-360}}
@keyframes hue{0%,100%{stop-color:#a88bff}50%{stop-color:#ff86be}}
.drift{animation:drift 10s ease-in-out infinite}.rise{animation:rise 6s ease-in-out infinite}
.pulse{animation:breathe 3s ease-in-out infinite}.flow{animation:flow 16s linear infinite}
.color{animation:hue 9s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>'''


def text(x, y, value, size, color, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def save(name, theme, width, height, title, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{MOTION}{body}</svg>\n'
    (OUT / f'{name}-{theme}.svg').write_text(svg)


def header(theme, p):
    project = data.get('current_project', 'something new')[:28]
    body = f'''<defs>
<linearGradient id="spectrum"><stop stop-color="#42cec8"/><stop offset=".48" stop-color="#a88bff" class="color"/><stop offset="1" stop-color="#ff86be"/></linearGradient>
<radialGradient id="violet"><stop stop-color="#9a6bff" stop-opacity=".3"/><stop offset="1" stop-color="#9a6bff" stop-opacity="0"/></radialGradient>
<radialGradient id="mint"><stop stop-color="#35d8c4" stop-opacity=".22"/><stop offset="1" stop-color="#35d8c4" stop-opacity="0"/></radialGradient>
<clipPath id="panel"><rect x=".5" y=".5" width="839" height="203" rx="18"/></clipPath>
</defs>
<style>@media(max-width:500px){{.eyebrow,.status,.fine-print{{display:none}}.name{{font-size:96px}}.tagline{{font-size:24px}}.art{{opacity:.6}}}}</style>
<g clip-path="url(#panel)">
<rect x=".5" y=".5" width="839" height="203" rx="18" fill="{p['bg']}" stroke="{p['line']}"/>
<g class="drift"><ellipse cx="680" cy="48" rx="290" ry="220" fill="url(#violet)"/><ellipse cx="70" cy="204" rx="280" ry="180" fill="url(#mint)"/></g>
<path d="M28 1H812" stroke="url(#spectrum)" stroke-width="3"/>
'''
    body += text(28, 30, 'DEVELOPER / CREATOR / CURIOUS HUMAN', 10, p['muted'], 600, 'class="eyebrow" letter-spacing="1.8"')
    body += text(25, 112, 'Torine.', 82, p['ink'], 700, 'class="name" letter-spacing="-4"')
    body += text(30, 145, 'Code with logic. Create with color.', 18, p['muted'], 400, 'class="tagline"')
    body += f'<g class="status"><circle cx="34" cy="179" r="3.5" fill="{p["teal"]}" class="pulse"/>'
    body += text(46, 183, f'BUILDING / {project}', 11, p['teal'], 600) + '</g>'
    # The line grid and floating glass tiles echo code, pixels and creative tools.
    body += f'''<g class="art" transform="translate(664 104)">
<path d="M-145 42 0 106 145 42 0-22Z M-105 60 40-4 M-60 80 85 16 M-40-4 105 60 M-85 16 60 80" fill="none" stroke="{p['purple']}" stroke-opacity=".16"/>
<g class="rise"><path d="m-74 8 74-40 74 40-74 40Z" fill="{p['teal']}" fill-opacity=".12" stroke="{p['teal']}" stroke-opacity=".45"/></g>
<g class="rise" style="animation-delay:-2s"><path d="m-74-18 74-40 74 40-74 40Z" fill="{p['purple']}" fill-opacity=".12" stroke="{p['purple']}" stroke-opacity=".65"/>
<path d="m-26-22-13 7 13 7m52-14 13 7-13 7m-17-20-18 26" fill="none" stroke="{p['purple']}" stroke-width="2.4" stroke-linecap="round"/></g>
<g class="rise" style="animation-delay:-4s"><rect x="91" y="-40" width="22" height="22" rx="5" fill="{p['pink']}" fill-opacity=".2" stroke="{p['pink']}" stroke-opacity=".6"/><rect x="-118" y="-60" width="12" height="12" rx="3" fill="{p['teal']}" fill-opacity=".6"/></g>
<circle cx="-102" cy="28" r="3" fill="{p['orange']}" class="pulse"/>
<path d="M100 53h10m-5-5v10M-118-12h8m-4-4v8" stroke="{p['pink']}" stroke-opacity=".6"/>
</g>
<path d="M28 203H812" stroke="url(#spectrum)" stroke-width="1.5" stroke-dasharray="90 270" class="flow"/>
</g>'''
    save('compact-header', theme, 840, 204, 'Torine — Code with logic. Create with color. Building ' + project, body)


def card(theme, p, kind, index, item):
    color = p[('teal', 'purple')[index] if kind == 'project' else ('pink', 'orange')[index]]
    body = f'''<defs><linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{color}" stop-opacity=".11"/><stop offset="1" stop-color="{color}" stop-opacity=".02"/></linearGradient></defs>
<rect x=".5" y=".5" width="409" height="117" rx="12" fill="{p['bg']}" stroke="{p['line']}"/>
<rect x="1" y="1" width="408" height="116" rx="12" fill="url(#wash)"/>
<path d="M20 1H112" stroke="{color}" stroke-width="2"/>
'''
    label = item['language'].upper() + ' / PROJECT' if kind == 'project' else 'FIELD NOTES / ' + item['date_label'].upper()
    body += text(20, 23, label, 9, color, 700, 'letter-spacing="1.3"')
    if kind == 'project':
        name = item['name'] if len(item['name']) < 24 else item['name'][:22] + '…'
        body += text(18, 58, name, 27, p['ink'], 650)
        for row, line in enumerate(textwrap.wrap(item['summary'], 48)[:2]):
            body += text(20, 82 + row * 18, line, 13, p['muted'])
    else:
        lines = textwrap.wrap(item['title'], 31)[:2]
        for row, line in enumerate(lines):
            body += text(19, 53 + row * 25, line, 20, p['ink'], 600)
        body += text(20, 102, 'Read the story · Chinese', 11, p['muted'])
    body += f'<path d="M374 29h12v12m0-12-13 13" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    save(f'card-{kind}-{index + 1}', theme, 410, 118, item.get('name', item.get('title', '')), body)


for theme, palette in PALETTES.items():
    header(theme, palette)
    for kind in ('project', 'post'):
        for i, item in enumerate(data[kind + 's']):
            card(theme, palette, kind, i, item)
