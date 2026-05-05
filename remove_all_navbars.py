import re
import os

files = [f for f in os.listdir('.') if f.endswith('.html')]

# Remove <nav id="main-nav">...</nav>
NAV_RE = re.compile(r'<nav id="main-nav".*?</nav>', re.DOTALL)

# Remove the injected navbar scroll script
SCRIPT_RE = re.compile(r'<script>\s*//\s*Unified navbar scroll animation.*?\}\)\(\);\s*</script>', re.DOTALL)

for fname in files:
    with open(fname, 'r') as f:
        content = f.read()

    new_content = NAV_RE.sub('', content)
    new_content = SCRIPT_RE.sub('', new_content)

    if new_content != content:
        with open(fname, 'w') as f:
            f.write(new_content)
        print(f"Cleaned: {fname}")
    else:
        print(f"No changes: {fname}")

