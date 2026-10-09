#!/usr/bin/env python3
"""Generate the canonical page/image sitemap; preserve known modification dates."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://finiteck.com/'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
IMAGE = 'http://www.google.com/schemas/sitemap-image/1.1'
ET.register_namespace('', NS)
ET.register_namespace('image', IMAGE)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonical = None
        self.noindex = False
        self.images = []
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.noindex = 'noindex' in attrs.get('content', '')
        if tag == 'img' and attrs.get('alt') and attrs.get('src'):
            self.images.append(attrs['src'])
        if attrs.get('data-image'):
            self.images.append(attrs['data-image'])


previous = ET.parse(ROOT / 'sitemap.xml').getroot()
dates = {item.findtext(f'{{{NS}}}loc'): item.findtext(f'{{{NS}}}lastmod')
         for item in previous}
root = ET.Element(f'{{{NS}}}urlset')
seen = set()
image_count = 0
for path in sorted(ROOT.rglob('*.html')):
    if '.git' in path.parts:
        continue
    page = Page(path.read_text())
    if not page.canonical or page.noindex or page.canonical in seen:
        continue
    expected = BASE + str(path.relative_to(ROOT)).removesuffix('index.html')
    if page.canonical != expected:
        continue  # Verification files and redirects are not canonical content.
    seen.add(page.canonical)
    entry = ET.SubElement(root, f'{{{NS}}}url')
    ET.SubElement(entry, f'{{{NS}}}loc').text = page.canonical
    if dates.get(page.canonical):
        ET.SubElement(entry, f'{{{NS}}}lastmod').text = dates[page.canonical]
    for image in sorted(set(urljoin(page.canonical, src) for src in page.images)):
        if urlsplit(image).hostname != 'finiteck.com':
            raise ValueError(f'Image must be hosted on the verified domain: {image}')
        if urlsplit(image).path.endswith('.svg'):
            continue  # App Store badges are navigation, not editorial images.
        item = ET.SubElement(entry, f'{{{IMAGE}}}image')
        ET.SubElement(item, f'{{{IMAGE}}}loc').text = image
        image_count += 1

ET.indent(root, space='  ')
ET.ElementTree(root).write(ROOT / 'sitemap.xml', encoding='UTF-8', xml_declaration=True)
print(f'Sitemap: {len(seen)} canonical pages, {image_count} image references.')
