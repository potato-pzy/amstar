import re

with open('products.html', 'r') as f:
    content = f.read()

# Find the navbar
nav_match = re.search(r'<nav id="main-nav".*?</nav>', content, re.DOTALL)
if nav_match:
    nav_html = nav_match.group(0)
    # Remove from current location
    content = content.replace(nav_html, '')
    
    # Place it immediately after the loader, BEFORE product-page-content
    # Let's find <div id="product-page-content">
    content = content.replace('<div id="product-page-content">', '<div id="product-page-content">\n' + nav_html)
    # Wait, if we want it visible immediately, it should be OUTSIDE product-page-content!
    # The loader is `<div id="product-page-loader"> ... </div>`
    # Let's insert it before `<div id="product-page-content">`
    content = content.replace('<div id="product-page-content">\n' + nav_html, '') # revert
    content = content.replace('<div id="product-page-content">', nav_html + '\n<div id="product-page-content">')
    
    with open('products.html', 'w') as f:
        f.write(content)
    print("Moved nav outside of hidden content")
else:
    print("Nav not found")
