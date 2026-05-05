import re

# Read shop.html to extract the good footer
with open('shop.html', 'r') as f:
    shop_content = f.read()

# Extract from <footer id="main-footer" to <!-- footer close -->
footer_match = re.search(r'<footer id="main-footer".*?</footer[^>]*>\n *<!-- footer close -->', shop_content, re.DOTALL)
if not footer_match:
    print("Could not find footer in shop.html")
    exit(1)
good_footer = footer_match.group(0)

# Read products.html
with open('products.html', 'r') as f:
    products_content = f.read()

# Replace the footer in products.html
new_products_content = re.sub(r'<footer id="main-footer".*?</footer[^>]*>\n *<!-- footer close -->', good_footer, products_content, flags=re.DOTALL)

with open('products.html', 'w') as f:
    f.write(new_products_content)

print("Successfully replaced products.html footer with shop.html footer")
