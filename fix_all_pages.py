import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

# Remove duplicate jQuery and OwlCarousel from ALL pages so we don't have this issue again
JQUERY_RE = re.compile(r'<script src="https://code.jquery.com/jquery-3\.6\.0\.min\.js"></script>', re.IGNORECASE)
OWL_RE = re.compile(r'<script src="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2\.3\.4/owl\.carousel\.min\.js"></script>', re.IGNORECASE)

for fname in files:
    with open(fname, 'r') as f:
        content = f.read()

    new_content = JQUERY_RE.sub('', content)
    new_content = OWL_RE.sub('', new_content)

    if new_content != content:
        with open(fname, 'w') as f:
            f.write(new_content)
        print(f"Removed duplicate scripts from: {fname}")

PYEOF
python3 fix_all_pages.py
