import re

with open('products.html', 'r') as f:
    content = f.read()

# Remove the navbar entirely
content = re.sub(r'<nav id="main-nav".*?</nav>', '', content, flags=re.DOTALL)

with open('products.html', 'w') as f:
    f.write(content)

print("Navbar removed from products.html")
