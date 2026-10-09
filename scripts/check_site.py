#!/usr/bin/env python3
"""Validate static navigation, headings, JSON-LD, image labels and the sitemap."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.urls, self.images, self.structured = [], [], [], []
        self.h1 = self.main = 0
        self.lang = self.title = self.description = self.canonical = False
        self.meta = {}
        self.json_buffer = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.lang = bool(attrs.get('lang'))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'main':
            self.main += 1
        if tag == 'title':
            self.title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = bool(attrs.get('content'))
        if tag == 'meta':
            self.meta[attrs.get('name') or attrs.get('property')] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'img':
            self.images.append(attrs)
        for attribute in ('src', 'href', 'data-image'):
            if attrs.get(attribute):
                self.urls.append(attrs[attribute])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.json_buffer = ''

    def handle_data(self, value):
        if self.json_buffer is not None:
            self.json_buffer += value

    def handle_endtag(self, tag):
        if tag == 'script' and self.json_buffer is not None:
            self.structured.append(self.json_buffer)
            self.json_buffer = None

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

pages = {}
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts or path.name.startswith('google') or path.name.endswith('.html.html'):
        continue
    pages[path.resolve()] = Document(path.read_text())

errors = []
for path, doc in pages.items():
    name = str(path.relative_to(ROOT))
    def fail(message):
        errors.append(f'{name}: {message}')
    for condition, message in [
        (doc.h1 == 1, f'expected one h1, found {doc.h1}'),
        (doc.main == 1, f'expected one main, found {doc.main}'),
        (doc.lang, 'missing document language'),
        (doc.title, 'missing title'),
        (doc.description, 'missing description'),
        (doc.canonical or name == '404.html', 'missing canonical URL'),
        ('main-content' in doc.ids, 'missing skip-link destination'),
    ]:
        if not condition:
            fail(message)
    for key, count in Counter(doc.ids).items():
        if count > 1:
            fail(f'duplicate id {key}')
    for img in doc.images:
        if 'alt' not in img:
            fail(f'image without alt attribute: {img.get("src")}')
        if not img.get('src', '').endswith('.svg') and not (img.get('width') and img.get('height')):
            fail(f'image without intrinsic dimensions: {img.get("src")}')
    if name != '404.html':
        expected = 'https://finiteck.com/' + name.removesuffix('index.html')
        if doc.canonical != expected:
            fail(f'canonical URL differs from published path: {doc.canonical}')
        for key in ('og:title', 'og:description', 'og:image', 'og:image:alt', 'twitter:card', 'twitter:image'):
            if not doc.meta.get(key):
                fail(f'missing {key}')
        if doc.meta.get('og:url') != doc.canonical:
            fail('Open Graph URL differs from canonical URL')
        if 'noindex' in doc.meta.get('robots', ''):
            fail('content page unexpectedly has noindex')
        for key in ('og:image', 'twitter:image'):
            image = urlsplit(doc.meta.get(key, ''))
            if image.hostname != 'finiteck.com' or not (ROOT / image.path.lstrip('/')).is_file():
                fail(f'missing or externally hosted social image: {key}')
    for value in doc.structured:
        try:
            json.loads(value)
        except ValueError as exc:
            fail(f'invalid JSON-LD: {exc}')
    for url in doc.urls:
        target = urlsplit(url)
        if target.scheme or target.netloc:
            continue
        if not target.path:
            destination = path
        elif target.path.startswith('/'):
            destination = ROOT / unquote(target.path).lstrip('/')
        else:
            destination = path.parent / unquote(target.path)
        if destination.is_dir():
            destination /= 'index.html'
        destination = destination.resolve()
        if not destination.is_file():
            fail(f'missing local destination {url}')
        elif target.fragment and destination in pages and unquote(target.fragment) not in pages[destination].ids:
            fail(f'missing anchor {url}')

sitemap = ET.parse(ROOT / 'sitemap.xml')
sitemap_urls = []
for loc in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
    sitemap_urls.append(loc.text)
    destination = ROOT / urlsplit(loc.text).path.lstrip('/')
    if destination.is_dir():
        destination /= 'index.html'
    if not destination.exists():
        errors.append(f'sitemap.xml: missing {loc.text}')
expected_urls = {doc.canonical for doc in pages.values() if doc.canonical and 'noindex' not in doc.meta.get('robots', '')}
if len(sitemap_urls) != len(set(sitemap_urls)) or set(sitemap_urls) != expected_urls:
    errors.append('sitemap.xml: canonical page coverage is incomplete or duplicated')
for loc in sitemap.findall('.//{http://www.google.com/schemas/sitemap-image/1.1}loc'):
    target = urlsplit(loc.text)
    if target.hostname != 'finiteck.com' or not (ROOT / target.path.lstrip('/')).is_file():
        errors.append(f'sitemap.xml: missing or externally hosted image {loc.text}')
if 'Sitemap: https://finiteck.com/sitemap.xml' not in (ROOT / 'robots.txt').read_text():
    errors.append('robots.txt: missing sitemap declaration')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(pages)} pages; internal URLs, anchors, headings, metadata, image labels, JSON-LD and sitemap.')
