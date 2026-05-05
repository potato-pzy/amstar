import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Update "Latest" link to point to blog.html
    # We look for <a href="#" ...>Latest</a> or <a href="#" ...>\s*Latest\s*</a>
    # We can just replace href="#" with href="blog.html" only where the inner text is Latest
    
    def replace_latest_href(match):
        a_tag = match.group(0)
        # Only replace href="#" if it contains #
        a_tag = re.sub(r'href="#"', 'href="blog.html"', a_tag)
        return a_tag
        
    content = re.sub(r'<a[^>]*>\s*Latest\s*</a>', replace_latest_href, content, flags=re.IGNORECASE)

    # In shop.html, fix the smooth scroll issue by making it instant or scrolling to main
    if file == 'shop.html':
        content = content.replace("window.scrollTo({ top: 0, behavior: 'smooth' });", "window.scrollTo(0, 0);")

    with open(file, 'w') as f:
        f.write(content)

print("Updated Latest link and shop.html scroll.")
