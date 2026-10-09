"""Regenerate the self-contained profile artwork: python3 scripts/render_profile.py."""
from html import escape
from pathlib import Path
import re
OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)
def text(x,y,value,size=16,color='#aab4d0',weight=400,mono=False,extra=''):
    font='Consolas,monospace' if mono else 'Inter,Segoe UI,Arial,sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def motion(name, w, h, body):
    """Animate decorative layers inside GitHub-compatible, self-contained SVGs."""
    style = '''<style>
    @keyframes breathe { 0%,100% { opacity:.35 } 50% { opacity:1 } }
    @keyframes drift { 0%,100% { transform:translate(0,0) } 50% { transform:translate(-32px,14px) } }
    @keyframes orbit { to { transform:rotate(360deg) } }
    @keyframes borderflow { to { stroke-dashoffset:-1000 } }
    @keyframes scan { 0%,15% { transform:translateX(-110%) } 75%,100% { transform:translateX(110%) } }
    @keyframes arrow { 0%,100% { transform:translate(0,0) } 50% { transform:translate(3px,-3px) } }
    @keyframes spectrum { 0%,100% { stop-color:#5ee7f7 } 33% { stop-color:#b392ff } 66% { stop-color:#ff8abc } }
    .pulse { animation:breathe 4s ease-in-out infinite }
    .drift { animation:drift 12s ease-in-out infinite }
    .orbit { animation:orbit 24s linear infinite }
    .reverse { animation-direction:reverse; animation-duration:18s }
    .flow { animation:borderflow 16s linear infinite }
    .scan { animation:scan 9s ease-in-out infinite; transform-box:view-box }
    .arrow { animation:arrow 3s ease-in-out infinite }
    #spectrum stop { animation:spectrum 12s ease-in-out infinite }
    #spectrum stop:nth-child(2) { animation-delay:-3s }
    #spectrum stop:nth-child(3) { animation-delay:-6s }
    #spectrum stop:nth-child(4) { animation-delay:-9s }
    @media (prefers-reduced-motion:reduce) { * { animation:none !important } .scan { display:none } }
    </style>'''
    # Pulse status lights and toolbox dots at different phases.
    counter = iter(range(100))
    body = re.sub(r'<circle ([^>]*r="4"[^>]*)/>',
                  lambda m: f'<circle {m[1]} class="pulse" style="animation-delay:-{next(counter)*.37}s"/>', body)
    body = body.replace('<ellipse cx=', '<ellipse class="drift" cx=')
    if name == 'hero.svg':
        # CSS keeps the orbit animation responsive to reduced-motion preferences.
        body = body.replace('<g><circle cx="-112"', '<g class="orbit"><circle cx="-112"')
        body = body.replace('<g><circle cx="87"', '<g class="orbit reverse"><circle cx="87"')
        body = re.sub(r'<animateTransform[^>]*/>', '', body)
        body += '<rect x="154" y="96" width="7" height="14" rx="1" fill="#b3a2ff" class="pulse"/>'
        # Sparse stars occupy the orbital area, leaving the copy untouched.
        for i, (x, y) in enumerate([(575,70),(635,309),(906,104),(932,276),(555,350),(863,346),(698,83)]):
            body += f'<circle cx="{x}" cy="{y}" r="1.8" fill="#bcbdff" class="pulse" style="animation-delay:-{i*.6}s"/>'
    if name.startswith('about'):
        body = re.sub(r'<rect ([^>]*width="3"[^>]*)/>', r'<rect \1 class="pulse"/>', body)
        # A small signal meter in the header adds movement without moving text.
        for i in range(9):
            height = [5,10,17,11,21,14,8,16,6][i]
            body += f'<rect x="{w-85+i*5}" y="{43-height}" width="2" height="{height}" rx="1" fill="#a997ff" class="pulse" style="animation-delay:-{i*.32}s"/>'
    if name.startswith('nav-'):
        body = body.replace('text-anchor="end"', 'text-anchor="end" class="arrow"')
    # The low-opacity beam passes behind the content; it never covers the text.
    beam = f'''<defs><linearGradient id="beam"><stop stop-color="#8ce8ff" stop-opacity="0"/><stop offset=".5" stop-color="#a393ff" stop-opacity=".09"/><stop offset="1" stop-color="#ff9dce" stop-opacity="0"/></linearGradient></defs><g class="scan"><path d="M0 0H{w*.16}L{w*.3} {h}H{w*.14}Z" fill="url(#beam)"/></g>'''
    # A moving highlight traces the existing panel edge.
    edge = f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="23" fill="none" stroke="url(#spectrum)" stroke-width="1.3" stroke-opacity=".55" stroke-dasharray="90 410" class="flow"/>'
    return style + beam + body + edge


def svg(name,w,h,title,body):
    body = motion(name, w, h, body)
    defs='''<defs><linearGradient id="spectrum" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5ee7f7"/><stop offset=".36" stop-color="#9c83ff"/><stop offset=".7" stop-color="#fb77b6"/><stop offset="1" stop-color="#ffc778"/></linearGradient><radialGradient id="violet"><stop stop-color="#7951e8" stop-opacity=".36"/><stop offset="1" stop-color="#7951e8" stop-opacity="0"/></radialGradient><radialGradient id="cyan"><stop stop-color="#27cecb" stop-opacity=".2"/><stop offset="1" stop-color="#27cecb" stop-opacity="0"/></radialGradient><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#929acb" stroke-opacity=".07"/></pattern></defs>'''
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{defs}<defs><clipPath id="panel"><rect width="{w}" height="{h}" rx="24"/></clipPath></defs><g clip-path="url(#panel)"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="#0c1020" stroke="#2a304b"/>{body}</g></svg>\n')
hero='<rect x="1" y="1" width="978" height="398" rx="24" fill="url(#grid)"/><ellipse cx="780" cy="130" rx="320" ry="270" fill="url(#violet)"/><ellipse cx="160" cy="380" rx="300" ry="220" fill="url(#cyan)"/>'
hero+=text(44,47,'W / 664',15,'#eef2ff',700,True)
hero+='<circle cx="749" cy="42" r="4" fill="#77efd0"/>'+text(762,47,'ALWAYS EXPLORING',12,'#77efd0',mono=True)
hero+=text(44,107,'HELLO, WORLD.',13,'#b3a2ff',mono=True)
hero+=text(40,205,'windy664',94,'url(#spectrum)',800,extra='letter-spacing="-5"')
hero+=text(46,250,'Code with logic. Create with color.',25,'#f0f2ff',600)
hero+=text(46,283,'Building systems. Exploring possibilities.',17,'#aeb9d7')
for x,label,color in [(44,'JAVA / JVM','#ffc778'),(184,'MINECRAFT','#77efd0'),(324,'AI AGENTS','#c0a1ff')]:
    hero+=f'<rect x="{x}" y="323" width="128" height="32" rx="16" fill="{color}" fill-opacity=".09" stroke="{color}" stroke-opacity=".35"/>'+text(x+64,344,label,11,color,600,True,'text-anchor="middle"')
hero+='''<g transform="translate(768 213)"><circle r="111" fill="none" stroke="#a68cff" stroke-opacity=".16"/><circle r="87" fill="none" stroke="#a68cff" stroke-opacity=".2" stroke-dasharray="3 9"/><ellipse rx="132" ry="48" transform="rotate(-32)" fill="none" stroke="url(#spectrum)" stroke-width="1.5"/><ellipse rx="132" ry="48" transform="rotate(42)" fill="none" stroke="url(#spectrum)" stroke-opacity=".45"/><path d="M0 -70 61 -35 61 35 0 70 -61 35 -61 -35Z" fill="#a487ff" fill-opacity=".1" stroke="url(#spectrum)" stroke-width="2"/><path d="M-61 -35 0 0 61 -35M0 0V70M0 -70V0L-61 35M0 0 61 35" fill="none" stroke="url(#spectrum)" stroke-opacity=".5"/><circle r="8" fill="#dbbfff"/><g><circle cx="-112" cy="0" r="5" fill="#62e8ef"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/></g><g><circle cx="87" cy="0" r="4" fill="#ff91c5"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/></g></g><path d="M44 385H936" stroke="url(#spectrum)" stroke-width="2" stroke-opacity=".6"/>'''
svg('hero.svg',980,400,'windy664 — Java, Minecraft & AI agents. Code with logic. Create with color.',hero)
stack=text(32,40,'02 / MY TOOLBOX',13,'#c4b5fd',700,True)+text(948,40,'BUILD / CONNECT / CREATE',11,'#8995b8',mono=True,extra='text-anchor="end"')
for row,items in enumerate([[('Java','#ffbe7b'),('Kotlin','#c6a0ff'),('Python','#ffe28a'),('Rust','#f7a58c'),('Maven','#ff8fac')],[('MySQL','#7dcfff'),('Redis','#ff8797'),('Docker','#70c5ff'),('Git','#ffa38a'),('Arduino','#69e0d1')]]):
    for col,(label,color) in enumerate(items):
        x,y=32+col*185,62+row*57
        stack+=f'<rect x="{x}" y="{y}" width="173" height="43" rx="12" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".22"/><circle cx="{x+19}" cy="{y+22}" r="4" fill="{color}"/>'+text(x+34,y+27,label,15,color,600)
svg('toolbox.svg',980,187,'Toolbox: Java, Kotlin, Python, Rust, Maven, MySQL, Redis, Docker, Git, Arduino',stack)
footer='<ellipse cx="490" cy="140" rx="450" ry="150" fill="url(#violet)"/><path d="M44 1H936" stroke="url(#spectrum)" stroke-width="2"/>'
footer+=text(490,55,'STAY CURIOUS. KEEP BUILDING.',25,'url(#spectrum)',800,extra='text-anchor="middle" letter-spacing="2"')
footer+=text(490,89,'One more idea. One more line. A whole new world.',16,'#b4bfdc',extra='text-anchor="middle"')
footer+=text(490,125,'WINDY664  /  CODE × CREATIVITY',10,'#8a96b6',mono=True,extra='text-anchor="middle" letter-spacing="2"')
svg('footer.svg',980,152,'Stay curious. Keep building. One more idea. One more line. A whole new world.',footer)

# Keep every section in the same visual system; provide readable narrow layouts.
about = text(40, 43, '01 / BEHIND THE CODE', 13, '#c4b5fd', 700, True)
about += text(40, 91, 'Java at heart. Curious by nature.', 30, '#eef2ff', 700)
for y, label, detail, color in [
    (143, 'BUILD', 'Minecraft plugins, backend systems, and cross-server data sync.', '#75e4ed'),
    (207, 'EXPLORE', 'AI agents and automation for coding and server operations.', '#c4a4ff'),
    (271, 'CREATE', 'Photography, video editing, and design beyond the terminal.', '#ff9bc9'),
]:
    about += f'<rect x="40" y="{y-15}" width="3" height="41" rx="1.5" fill="{color}"/>'
    about += text(57, y, label, 11, color, 700, True)
    about += text(57, y+26, detail, 19, '#b4bfdc')
svg('about.svg', 980, 330, 'Java at heart. Curious by nature. Building backend systems, exploring AI agents, and creating through photography and design.', about)
mobile = text(28, 40, '01 / BEHIND THE CODE', 12, '#c4b5fd', 700, True)
mobile += text(28, 87, 'Java at heart.', 30, '#eef2ff', 700)
mobile += text(28, 124, 'Curious by nature.', 30, '#eef2ff', 700)
for y, label, lines, color in [
    (176, 'BUILD', ['Minecraft plugins, backend systems,', 'and cross-server data sync.'], '#75e4ed'),
    (270, 'EXPLORE', ['AI agents and automation for coding', 'and server operations.'], '#c4a4ff'),
    (364, 'CREATE', ['Photography, video editing, and design', 'beyond the terminal.'], '#ff9bc9'),
]:
    mobile += f'<rect x="28" y="{y-14}" width="3" height="64" rx="1.5" fill="{color}"/>'
    mobile += text(44, y, label, 11, color, 700, True)
    for i, line in enumerate(lines): mobile += text(44, y+26+i*24, line, 18, '#b4bfdc')
svg('about-mobile.svg', 480, 446, 'Java at heart. Curious by nature. Backend systems, AI agents, photography, video editing, and design.', mobile)
mobile_stack = text(28, 40, '02 / MY TOOLBOX', 13, '#c4b5fd', 700, True)
items=[('Java','#ffbe7b'),('Kotlin','#c6a0ff'),('Python','#ffe28a'),('Rust','#f7a58c'),('Maven','#ff8fac'),('MySQL','#7dcfff'),('Redis','#ff8797'),('Docker','#70c5ff'),('Git','#ffa38a'),('Arduino','#69e0d1')]
for i, (label, color) in enumerate(items):
    x, y = 28+(i%2)*218, 62+(i//2)*55
    mobile_stack += f'<rect x="{x}" y="{y}" width="206" height="43" rx="12" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".22"/><circle cx="{x+19}" cy="{y+22}" r="4" fill="{color}"/>' + text(x+34, y+28, label, 17, color, 600)
svg('toolbox-mobile.svg',480,350,'Java, Kotlin, Python, Rust, Maven, MySQL, Redis, Docker, Git, Arduino',mobile_stack)
for name, label, color in [('blog','BLOG','#c4a4ff'),('repositories','REPOSITORIES','#75e4ed'),('inspiration','INSPIRATION','#ff9bc9')]:
    button=text(24, 38, label, 14, color, 700, True)+text(285,38,'↗',20,color,extra='text-anchor="end"')
    svg(f'nav-{name}.svg',310,64,label,button)
