import re

with open('index.html', 'r') as f:
    index_content = f.read()

# Extract the full header block from index.html (from <!-- header begin --> to <!-- header close -->)
header_match = re.search(r'(        <!-- header begin -->.*?        <!-- header close -->)', index_content, re.DOTALL)
if not header_match:
    print("ERROR: Could not find header block in index.html")
    exit(1)

header_block = header_match.group(1)
print(f"Extracted header block ({len(header_block)} chars)")

with open('master.html', 'r') as f:
    master_content = f.read()

# Replace the empty navbar placeholder comments with the real header block
old_placeholder = """<!-- ============================================================ -->
<!-- PREMIUM WHITE NAVBAR                                          -->
<!-- ============================================================ -->

<!-- navbar close -->"""

new_content = master_content.replace(old_placeholder, header_block)

if new_content == master_content:
    print("ERROR: Could not find placeholder in master.html")
else:
    with open('master.html', 'w') as f:
        f.write(new_content)
    print("Successfully injected index.html header into master.html")

