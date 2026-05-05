import re

# Read shop.html
with open('shop.html', 'r') as f:
    shop_content = f.read()

# Extract footer from shop.html
footer_match = re.search(r'<footer id="main-footer".*?</footer[^>]*>\n *<!-- footer close -->', shop_content, re.DOTALL)
if not footer_match:
    print("Could not find footer in shop.html")
    exit(1)

shop_footer = footer_match.group(0)

# Read products.html
with open('products.html', 'r') as f:
    products_content = f.read()

# Replace footer in products.html
new_products_content = re.sub(r'<footer.*?</footer>\s*<!-- footer close -->', shop_footer, products_content, flags=re.DOTALL)

with open('products.html', 'w') as f:
    f.write(new_products_content)

print("Replaced footer in products.html")
