import re

with open('master.html', 'r') as f:
    master_content = f.read()

# Extract navbar from master
nav_match = re.search(r'<nav id="main-nav".*?</nav>', master_content, re.DOTALL)
if nav_match:
    nav_html = nav_match.group(0)
else:
    print("Could not find nav in master.html")
    exit(1)

with open('products.html', 'r') as f:
    prod_content = f.read()

# Find the end of product-page-loader
loader_end = prod_content.find('</div>\n\n\n\n\n\n<!-- ============================================================ -->\n<!-- PREMIUM WHITE NAVBAR                                          -->')

if loader_end != -1:
    # Let's replace that messy gap with the correct structure
    replacement = f'</div>\n\n{nav_html}\n\n<div id="product-page-content">\n\n<!-- ============================================================ -->\n<!-- PREMIUM WHITE NAVBAR                                          -->'
    prod_content = prod_content.replace('</div>\n\n\n\n\n\n<!-- ============================================================ -->\n<!-- PREMIUM WHITE NAVBAR                                          -->', replacement)
    
    with open('products.html', 'w') as f:
        f.write(prod_content)
    print("Successfully restored navbar and product-page-content div")
else:
    # Try more robust regex
    match = re.search(r'</div>\s*<!-- ===+ -->\s*<!-- PREMIUM WHITE NAVBAR', prod_content)
    if match:
        replacement = f'</div>\n\n{nav_html}\n\n<div id="product-page-content">\n\n<!-- ============================================================ -->\n<!-- PREMIUM WHITE NAVBAR'
        prod_content = prod_content[:match.start()] + replacement + prod_content[match.end():]
        with open('products.html', 'w') as f:
            f.write(prod_content)
        print("Successfully restored navbar and product-page-content div (Regex)")
    else:
        print("Could not find insertion point")
