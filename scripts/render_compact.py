"""Render a restrained editorial masthead in both GitHub themes."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parents[1] / 'assets'
data_path = OUT / 'profile-data.json'
data = json.loads(data_path.read_text()) if data_path.exists() else {}
project = data.get('current_project', 'something new')

for theme, ink, muted, line, accent in [
    ('light', '#22211f', '#74716c', '#dedbd6', '#b24c32'),
    ('dark', '#edeae4', '#a09c95', '#373735', '#ec9d7e'),
]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="186" viewBox="0 0 840 186" role="img" aria-labelledby="title desc">
<title id="title">Torine — a personal index of code and curiosity.</title>
<desc id="desc">Java / JVM, Minecraft and AI agents. Currently building {escape(project)}.</desc>
<style>@media(max-width:500px){{.small-print{{display:none}}.name{{font-size:140px}}.quote{{font-size:28px}}}}</style>
<g font-family="Arial,Helvetica,sans-serif">
  <path d="M0 1H840" stroke="{ink}" stroke-width="2"/>
  <text class="small-print" x="0" y="25" fill="{muted}" font-size="11" letter-spacing="2.2">CODE / SYSTEMS / CURIOSITY</text>
  <text class="small-print" x="840" y="25" text-anchor="end" fill="{accent}" font-size="11" letter-spacing="1.5">THE PERSONAL INDEX</text>
  <text class="name" x="-4" y="130" fill="{ink}" font-family="Georgia,Times New Roman,serif" font-size="112" letter-spacing="-5">Torine<tspan fill="{accent}">.</tspan></text>
  <path d="M548 58V135" stroke="{line}"/>
  <text class="quote" x="574" y="78" fill="{ink}" font-family="Georgia,Times New Roman,serif" font-size="22" font-style="italic">Java at heart.</text>
  <text class="quote" x="574" y="108" fill="{ink}" font-family="Georgia,Times New Roman,serif" font-size="22" font-style="italic">Curious by nature.</text>
  <text class="small-print" x="574" y="134" fill="{muted}" font-size="11">NOW / {escape(project[:28])}</text>
  <g class="small-print">
  <text x="0" y="169" fill="{muted}" font-size="12" letter-spacing="1">JAVA / JVM</text>
  <text x="137" y="169" fill="{accent}" font-size="12">/</text>
  <text x="161" y="169" fill="{muted}" font-size="12" letter-spacing="1">MINECRAFT</text>
  <text x="288" y="169" fill="{accent}" font-size="12">/</text>
  <text x="312" y="169" fill="{muted}" font-size="12" letter-spacing="1">AI AGENTS</text>
  </g>
  <path d="M0 185H840" stroke="{line}"/>
</g>
</svg>
'''
    (OUT / f'compact-header-{theme}.svg').write_text(svg)
