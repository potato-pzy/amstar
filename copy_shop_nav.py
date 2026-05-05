import re

with open('shop.html', 'r') as f:
    shop_content = f.read()

# Extract navbar from shop.html
# Need to capture the <nav> and everything in it
nav_match = re.search(r'<nav id="main-nav".*?</nav>', shop_content, re.DOTALL)
if nav_match:
    nav_html = nav_match.group(0)
else:
    # shop.html might not have id="main-nav"? Wait, I checked it earlier and it did.
    # Let's search for just <nav
    nav_match = re.search(r'<nav.*?</nav>', shop_content, re.DOTALL)
    if nav_match:
        nav_html = nav_match.group(0)
    else:
        print("Could not find nav in shop.html")
        exit(1)

with open('products.html', 'r') as f:
    prod_content = f.read()

# Make sure we remove any existing nav just in case
prod_content = re.sub(r'<nav.*?</nav>', '', prod_content, flags=re.DOTALL)

# Insert after <div id="product-page-loader">...</div>
# Let's just find the end of the loader block or insert before <div id="product-page-content">
insertion_point = prod_content.find('<div id="product-page-content">')
if insertion_point != -1:
    prod_content = prod_content[:insertion_point] + nav_html + '\n\n' + prod_content[insertion_point:]
    with open('products.html', 'w') as f:
        f.write(prod_content)
    print("Navbar from shop.html placed into products.html successfully")
else:
    print("Could not find <div id=\"product-page-content\"> in products.html")
