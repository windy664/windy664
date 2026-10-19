"""Refresh public profile data. Run with GH_TOKEN or an authenticated gh CLI."""
import json
import re
import runpy
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OWNER = "windy664"


def safe_link(value):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in {
        "windy664.github.io", "github.com"
    }:
        raise ValueError(f"Unexpected public URL: {value}")
    return escape(value, quote=True)


def text(value):
    return escape(" ".join(value.split()), quote=True)


def replace_section(readme, name, body):
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise ValueError(f"Missing or duplicate markers: {name}")
    return re.sub(re.escape(start) + r".*?" + re.escape(end),
                  lambda _: f"{start}\n{body}\n{end}", readme, flags=re.S)


def main():
    request = urllib.request.Request(
        "https://windy664.github.io/rss.xml", headers={"User-Agent": "Torine-Profile"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        feed = ET.fromstring(response.read())
    posts = []
    for item in feed.findall("./channel/item"):
        published = parsedate_to_datetime(item.findtext("pubDate"))
        if published <= datetime.now(timezone.utc):
            posts.append((published, item.findtext("title"), item.findtext("link")))
    posts.sort(key=lambda post: post[0], reverse=True)
    if len(posts) < 2:
        raise ValueError("Expected at least two published blog posts")

    result = subprocess.run(
        ["gh", "api", f"users/{OWNER}/repos?sort=pushed&per_page=100"],
        check=True, capture_output=True, text=True,
    )
    repos = [repo for repo in json.loads(result.stdout)
             if not repo["fork"] and not repo["archived"] and not repo["private"]
             and repo["name"] not in {OWNER, f"{OWNER}.github.io", "github-workflow-practice"}]
    repos.sort(key=lambda repo: repo["pushed_at"], reverse=True)
    repos = repos[:2]
    if len(repos) < 2:
        raise ValueError("Expected at least two public projects")

    summaries = {
        'Ru41': 'Personal automation, built with Rust.',
        'OctoDining': 'Meal planning on a budget. A work in progress.',
    }
    editorial_titles = {
        '/2026/10/14/2026-10-14-reverse-engineering-campus-card-waterfee/': 'Campus utilities, automated',
        '/2026/10/04/windyagent-from-framework-to-application/': 'WindyAgent: from framework to application?',
    }
    data = {"current_project": repos[0]['name'], 'projects': [], 'posts': []}
    for repo in repos:
        description = repo['description'] or ''
        fallback = description if description.isascii() else ''
        summary = summaries.get(repo['name'], fallback or 'An open-source project.')
        data['projects'].append({
            'name': repo['name'], 'url': repo['html_url'],
            'language': repo['language'] or 'Code', 'summary': summary,
        })
    for date, title, url in posts[:2]:
        fallback = title if title.isascii() else f'Field notes — {date:%B %d, %Y}'
        data['posts'].append({
            'title': editorial_titles.get(urlparse(url).path, fallback),
            'url': url, 'date_label': date.strftime('%b %d'),
        })
    journal = []
    for kind, label in [('project', 'Building'), ('post', 'Writing')]:
        journal.extend([f'<h4>{label}</h4>', '<p align="center">'])
        for index, item in enumerate(data[kind + 's'], 1):
            asset = f'https://raw.githubusercontent.com/{OWNER}/{OWNER}/master/assets/card-{kind}-{index}'
            alt = item['name'] + ' — ' + item['summary'] if kind == 'project' else item['title'] + ' (article in Chinese)'
            journal.append(
                f'<a href="{safe_link(item["url"])}"><picture>'
                f'<source media="(prefers-color-scheme: dark)" srcset="{asset}-dark.svg" />'
                f'<img src="{asset}-light.svg" width="410" alt="{text(alt)}" />'
                '</picture></a>'
            )
        journal.append('</p>')
    readme = (ROOT / "README.md").read_text()
    readme = replace_section(readme, "JOURNAL", '\n'.join(journal))
    (ROOT / "assets/profile-data.json").write_text(json.dumps(data, indent=2) + "\n")
    runpy.run_path(str(ROOT / "scripts/render_compact.py"))
    (ROOT / "README.md").write_text(readme)
    print("Updated two blog posts, two public projects, and both banner themes.")


if __name__ == "__main__":
    main()
