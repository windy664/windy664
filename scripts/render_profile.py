"""Regenerate the self-contained profile artwork: python3 scripts/render_profile.py."""
from html import escape
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)
def text(x,y,value,size=16,color='#aab4d0',weight=400,mono=False,extra=''):
    font='Consolas,monospace' if mono else 'Inter,Segoe UI,Arial,sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'
def svg(name,w,h,title,body):
    defs='''<defs><linearGradient id="spectrum" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5ee7f7"/><stop offset=".36" stop-color="#9c83ff"/><stop offset=".7" stop-color="#fb77b6"/><stop offset="1" stop-color="#ffc778"/></linearGradient><radialGradient id="violet"><stop stop-color="#7951e8" stop-opacity=".36"/><stop offset="1" stop-color="#7951e8" stop-opacity="0"/></radialGradient><radialGradient id="cyan"><stop stop-color="#27cecb" stop-opacity=".2"/><stop offset="1" stop-color="#27cecb" stop-opacity="0"/></radialGradient><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#929acb" stroke-opacity=".07"/></pattern></defs>'''
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>{defs}<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="#0c1020" stroke="#2a304b"/>{body}</svg>\n')
hero='<rect x="1" y="1" width="978" height="398" rx="24" fill="url(#grid)"/><ellipse cx="780" cy="130" rx="320" ry="270" fill="url(#violet)"/><ellipse cx="160" cy="380" rx="300" ry="220" fill="url(#cyan)"/>'
hero+=text(44,47,'W / 664',15,'#eef2ff',700,True)
hero+='<circle cx="749" cy="42" r="4" fill="#77efd0"/>'+text(762,47,'ALWAYS EXPLORING',12,'#77efd0',mono=True)
hero+=text(44,107,'HELLO, WORLD.  /  你好，世界。',13,'#b3a2ff',mono=True)
hero+=text(40,205,'windy664',94,'url(#spectrum)',800,extra='letter-spacing="-5"')
hero+=text(46,250,'Code with logic. Create with color.',25,'#f0f2ff',600)
hero+=text(46,283,'用代码构建世界，让灵感自由生长。',17,'#aeb9d7')
for x,label,color in [(44,'JAVA / JVM','#ffc778'),(184,'MINECRAFT','#77efd0'),(324,'AI AGENTS','#c0a1ff')]:
    hero+=f'<rect x="{x}" y="323" width="128" height="32" rx="16" fill="{color}" fill-opacity=".09" stroke="{color}" stroke-opacity=".35"/>'+text(x+64,344,label,11,color,600,True,'text-anchor="middle"')
hero+='''<g transform="translate(768 213)"><circle r="111" fill="none" stroke="#a68cff" stroke-opacity=".16"/><circle r="87" fill="none" stroke="#a68cff" stroke-opacity=".2" stroke-dasharray="3 9"/><ellipse rx="132" ry="48" transform="rotate(-32)" fill="none" stroke="url(#spectrum)" stroke-width="1.5"/><ellipse rx="132" ry="48" transform="rotate(42)" fill="none" stroke="url(#spectrum)" stroke-opacity=".45"/><path d="M0 -70 61 -35 61 35 0 70 -61 35 -61 -35Z" fill="#a487ff" fill-opacity=".1" stroke="url(#spectrum)" stroke-width="2"/><path d="M-61 -35 0 0 61 -35M0 0V70M0 -70V0L-61 35M0 0 61 35" fill="none" stroke="url(#spectrum)" stroke-opacity=".5"/><circle r="8" fill="#dbbfff"/><g><circle cx="-112" cy="0" r="5" fill="#62e8ef"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/></g><g><circle cx="87" cy="0" r="4" fill="#ff91c5"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/></g></g><path d="M44 385H936" stroke="url(#spectrum)" stroke-width="2" stroke-opacity=".6"/>'''
svg('hero.svg',980,400,'windy664 — Java, Minecraft & AI agents. Code with logic. Create with color.',hero)
stack=text(32,40,'MY TOOLBOX',13,'#c4b5fd',700,True)+text(948,40,'BUILD / CONNECT / CREATE',11,'#8995b8',mono=True,extra='text-anchor="end"')
for row,items in enumerate([[('Java','#ffbe7b'),('Kotlin','#c6a0ff'),('Python','#ffe28a'),('Rust','#f7a58c'),('Maven','#ff8fac')],[('MySQL','#7dcfff'),('Redis','#ff8797'),('Docker','#70c5ff'),('Git','#ffa38a'),('Arduino','#69e0d1')]]):
    for col,(label,color) in enumerate(items):
        x,y=32+col*185,62+row*57
        stack+=f'<rect x="{x}" y="{y}" width="173" height="43" rx="12" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".22"/><circle cx="{x+19}" cy="{y+22}" r="4" fill="{color}"/>'+text(x+34,y+27,label,15,color,600)
svg('toolbox.svg',980,187,'Toolbox: Java, Kotlin, Python, Rust, Maven, MySQL, Redis, Docker, Git, Arduino',stack)
PROJECTS=[
('windyagent','01 / AUTONOMOUS OPERATIONS','WindyAgent',['让 Minecraft 服务器运维拥有自己的 Agent。','可替换 LLM，探索自主运维。'],'KOTLIN  /  LLM  /  MINECRAFT','#c1a0ff','AG'),
('windui','02 / INTERFACE ENGINEERING','WindUI',['让服务端驱动 Minecraft 的交互界面。','把 UI 能力带进方块世界。'],'JAVA  /  SDUI  /  MINECRAFT','#6ae2ef','UI'),
('ftbquests','03 / CONNECTED WORLDS','FTBQuestsSync',['跨越服务器，让任务进度保持同步。','基于 Redis 与 IO 的 FTB 任务数据同步。'],'JAVA  /  REDIS  /  DATA SYNC','#76ecc0','DB'),
('arc','04 / CODING INTELLIGENCE','ARC-Bench Agent',['从需求分解到多智能体协作与视觉验收。','探索有限 Token 预算下的编程能力。'],'PYTHON  /  AGENTS  /  AUTOMATION','#ff9dcb','AI'),
('gosim','05 / BEYOND THE HORIZON','GOSIM Survey Agent',['Rust 观测规划 × LLM 情报解析。','探索巡天调度与复杂环境中的泛化能力。'],'RUST  /  LLM  /  OBSERVATION','#ffc784','//'),
('velocity','06 / SERVER EXPERIENCE','VelocityHologram',['在代理端，为世界添上悬浮的信息。','基于 Velocity + packetevents 的悬浮字系统。'],'JAVA  /  VELOCITY  /  PACKETS','#87b5ff','VX')]
for name,eyebrow,title,lines,tags,color,icon in PROJECTS:
    body=f'<path d="M25 1H455" stroke="{color}" stroke-width="2" stroke-opacity=".75"/><circle cx="435" cy="70" r="65" fill="{color}" fill-opacity=".035"/>'
    body+=text(26,37,eyebrow,10,color,600,True)+text(26,82,title,27,'#f0f3ff',700)+text(432,82,icon,18,color,700,True,'text-anchor="middle"')
    for i,line in enumerate(lines): body+=text(26,120+i*25,line,14,'#b0bad3')
    body+='<path d="M26 171H454" stroke="#252d44"/>'+text(26,198,tags,10,color,600,True)+text(454,200,'↗',22,color,extra='text-anchor="end"')
    svg(f'project-{name}.svg',480,222,f'{title}: {" ".join(lines)}',body)
footer='<ellipse cx="490" cy="140" rx="450" ry="150" fill="url(#violet)"/><path d="M44 1H936" stroke="url(#spectrum)" stroke-width="2"/>'
footer+=text(490,55,'STAY CURIOUS. KEEP BUILDING.',25,'url(#spectrum)',800,extra='text-anchor="middle" letter-spacing="2"')
footer+=text(490,89,'下一次灵感，下一行代码，下一个世界。',16,'#b4bfdc',extra='text-anchor="middle"')
footer+=text(490,125,'WINDY664  /  CODE × CREATIVITY',10,'#8a96b6',mono=True,extra='text-anchor="middle" letter-spacing="2"')
svg('footer.svg',980,152,'Stay curious. Keep building. 下一次灵感，下一行代码，下一个世界。',footer)
