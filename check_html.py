#!/usr/bin/env python3
import re, os

html_path = '/mnt/c/Users/USER/Downloads/learning_verilog_and_sv/overagain/hash_pareto/notebook/hashpareto.html'
with open(html_path, 'r') as f:
    content = f.read()

imgs = re.findall(r'<img[^>]+>', content)
print(f'Total img tags: {len(imgs)}')
for i, img in enumerate(imgs[:5]):
    src_match = re.search(r'src="([^"]+)"', img)
    if src_match:
        src = src_match.group(1)
        print(f'Image {i+1} src: {src[:120]}')
    else:
        print(f'Image {i+1}: no src attribute')

# Check for data: URIs
data_uris = re.findall(r'src="data:[^"]+"', imgts) if 'imgts' in dir() else []
print(f'\nChecking for data: URIs...')
for img in imgs:
    if 'data:' in img.get('src', ''):
        print('Found data URI')
        break
else:
    print('No data URIs found in img src')