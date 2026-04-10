#!/usr/bin/env python3
"""
Scans the Astro blog repo and regenerates data.js with latest post data.
Run this whenever you want to refresh the tracker with new/updated posts.

Usage: python3 update-data.py
"""
import os, re, json

REPO_PATH = os.path.join(os.path.dirname(__file__), '..', 'vantagecircle-astro')
POSTS_DIR = os.path.join(REPO_PATH, 'content', 'en', 'posts')
OUTPUT = os.path.join(os.path.dirname(__file__), 'data.js')

posts = []
for fname in sorted(os.listdir(POSTS_DIR)):
    if not fname.endswith('.md'):
        continue
    with open(os.path.join(POSTS_DIR, fname), 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        continue
    fm = m.group(1)
    title_m = re.search(r'^title:\s*"(.+?)"', fm, re.M)
    slug_m = re.search(r'^slug:\s*"(.+?)"', fm, re.M)
    date_m = re.search(r'^date:\s*(\S+)', fm, re.M)
    updated_m = re.search(r'^updated:\s*(\S+)', fm, re.M)
    author_m = re.search(r'^author:\s*(.+)', fm, re.M)
    tags_section = re.search(r'^tags:\s*\n((?:\s+-\s+.+\n)*)', fm, re.M)

    title = title_m.group(1) if title_m else ''
    slug = slug_m.group(1) if slug_m else fname.replace('.md', '')
    date = date_m.group(1) if date_m else ''
    updated = updated_m.group(1) if updated_m else ''

    tags = []
    if tags_section:
        tags = [t.strip().lstrip('- ') for t in tags_section.group(1).strip().split('\n') if t.strip()]

    author_raw = author_m.group(1).strip() if author_m else ''
    if author_raw.startswith('['):
        authors = [a.strip().strip('"').strip("'") for a in author_raw.strip('[]').split(',')]
    else:
        authors = [author_raw.strip('"').strip("'")]

    posts.append({'t': title, 's': slug, 'd': date, 'u': updated, 'a': authors, 'tg': tags})

js = 'const EMBEDDED_DATA = ' + json.dumps(posts, ensure_ascii=True) + ';'
with open(OUTPUT, 'w') as f:
    f.write(js)

print(f'Updated data.js with {len(posts)} posts')
