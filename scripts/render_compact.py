"""A small pixel masthead and 88x31 buttons for Torine's personal homepage."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / 'assets'
LETTERS = {
    'T': ['11111','00100','00100','00100','00100','00100','00100'],
    'O': ['01110','10001','10001','10001','10001','10001','01110'],
    'R': ['11110','10001','10001','11110','10100','10010','10001'],
    'I': ['11111','00100','00100','00100','00100','00100','11111'],
    'N': ['10001','11001','11001','10101','10011','10011','10001'],
    'E': ['11111','10000','10000','11110','10000','10000','11111'],
}
COLORS = ['#89d9ff', '#ffc28b', '#b4eba1', '#e1b0ff', '#ff9ead', '#ffdf82']


def svg(name, width, height, title, body):
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{body}</svg>\n')


body = '''<style>
@keyframes twinkle{0%,70%,100%{opacity:.35}75%,95%{opacity:1}}
@keyframes cursor{0%,45%{opacity:1}46%,100%{opacity:0}}
.star{animation:twinkle 5s steps(1,end) infinite}.cursor{animation:cursor 1.4s steps(1,end) infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
@media(max-width:500px){.small{display:none}.wordmark{transform:translate(28px,48px) scale(1.2)}.caption{font-size:23px}}
</style>
<rect width="840" height="170" fill="#151c32"/>
<path d="M1 169V1H839" fill="none" stroke="#60739a" stroke-width="2"/>
<path d="M839 1V169H1" fill="none" stroke="#080e1d" stroke-width="2"/>
'''
for index, (x,y) in enumerate([(448,23),(530,67),(796,35),(614,27),(756,139),(467,123),(575,146),(814,104),(392,149),(683,24)]):
    color = COLORS[index % len(COLORS)]
    body += f'<path class="star" style="animation-delay:-{index*.6}s" d="M{x-3} {y}h7M{x} {y-3}v7" stroke="{color}" stroke-width="1"/>'
body += '<text class="small" x="28" y="29" font-family="Courier New,monospace" font-size="12" fill="#b2bfd8">windy664.github.io / personal homepage</text>'
body += '<g class="wordmark" transform="translate(28 48)">'
for letter_index, letter in enumerate('TORINE'):
    for row, pixels in enumerate(LETTERS[letter]):
        for col, value in enumerate(pixels):
            if value == '1':
                body += f'<rect x="{letter_index*54+col*8}" y="{row*8}" width="7" height="7" fill="{COLORS[letter_index]}"/>'
body += '</g><text class="caption" x="28" y="141" font-family="Courier New,monospace" font-size="16" fill="#dce4f3">Java / Minecraft / Rust</text>'
# A tiny CRT, drawn with flat pixels; the only moving part is its terminal cursor.
body += '''<g transform="translate(634 47)" shape-rendering="crispEdges">
<path d="M8 0h102v4h5v70H4V4h4Z" fill="#bdc6cd"/>
<path d="M8 4h102v3H8Z" fill="#edf1f2"/>
<path d="M8 8h98v55H8Z" fill="#566074"/>
<path d="M12 12h90v47H12Z" fill="#142c2a"/>
<path d="m21 23 8 6-8 6" fill="none" stroke="#9be0ae" stroke-width="3"/>
<rect class="cursor" x="39" y="33" width="10" height="3" fill="#9be0ae"/>
<rect x="93" y="67" width="5" height="3" fill="#8fca75"/>
<path d="M43 74h34v12H43Z" fill="#909ba6"/>
<path d="M26 86h68v8H26Z" fill="#c1c9cf"/>
<path d="M0 102h119l8 12H-9Z" fill="#a1adba"/>
<path d="M7 105h103M3 109h111" stroke="#59697c" stroke-width="2"/>
</g>'''
for theme in ('light','dark'):
    svg(f'compact-header-{theme}.svg',840,170,'Torine / windy664 — Java, Minecraft and Rust',body)

for name, label, color in [('blog','MY BLOG','#345caf'),('code','MY CODE','#237665'),('rss','RSS FEED','#a95530')]:
    button = f'''<style>@keyframes nudge{{0%,65%,100%{{transform:translateX(0)}}70%,90%{{transform:translateX(2px)}}}}.arrow{{animation:nudge 4s steps(1,end) infinite}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect width="88" height="31" fill="{color}"/>
<path d="M1 30V1H87" fill="none" stroke="#dce3ec" stroke-width="2"/>
<path d="M87 1V30H1" fill="none" stroke="#182433" stroke-width="2"/>
<text x="7" y="19" fill="#ffffff" font-family="Verdana,Arial,sans-serif" font-size="9" font-weight="700">{label}</text>
<path class="arrow" d="m74 11 4 4-4 4" fill="none" stroke="#ffffff" stroke-width="2"/>'''
    svg(f'nav-retro-{name}.svg',88,31,label,button)
