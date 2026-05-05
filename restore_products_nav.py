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

# Make sure we don't have multiple navbars
prod_content = re.sub(r'<nav id="main-nav".*?</nav>', '', prod_content, flags=re.DOTALL)

# Insert it right before <div id="product-page-content">
prod_content = prod_content.replace('<div id="product-page-content">', nav_html + '\n\n<div id="product-page-content">')

with open('products.html', 'w') as f:
    f.write(prod_content)

print("Restored navbar to products.html")
