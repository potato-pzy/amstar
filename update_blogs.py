import re

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Read master.html parts
    with open('master.html', 'r') as f:
        master_content = f.read()

    # Extract style block
    style_match = re.search(r'<style>.*?</style>', master_content, re.DOTALL)
    style_block = style_match.group(0) if style_match else ""

    # Extract font link
    font_match = re.search(r'<link href="https://fonts.googleapis.com/css2\?family=Alan\+Sans[^>]+>', master_content)
    font_link = font_match.group(0) if font_match else ""

    # Extract navbar
    nav_match = re.search(r'<nav id="main-nav".*?</nav>\n *<!-- navbar close -->', master_content, re.DOTALL)
    nav_block = nav_match.group(0) if nav_match else ""

    # Extract footer
    # Find from <footer id="main-footer" to <!-- footer close -->
    with open('shop.html', 'r') as f:
        shop_content = f.read()
    footer_match = re.search(r'<footer id="main-footer".*?</footer[^>]*>\n *<!-- footer close -->', shop_content, re.DOTALL)
    footer_block = footer_match.group(0) if footer_match else ""

    # 1. Update title
    content = re.sub(r'<title>.*?</title>', '<title>Amstar Pumps - Blog</title>', content)

    # 2. Add style and fonts to head
    if style_block and font_link:
        head_end = content.find('</head>')
        if head_end != -1:
            content = content[:head_end] + style_block + '\n' + font_link + '\n' + content[head_end:]

    # 3. Replace header with new navbar
    # Note: original uses <header class="transparent... > ... </header>
    content = re.sub(r'<header class="transparent.*?</header>\n *<!-- header close -->', nav_block, content, flags=re.DOTALL)

    # 4. Replace footer
    # Note: original uses <footer class="section-dark"> ... </footer>
    content = re.sub(r'<footer class="section-dark".*?</footer[^>]*>\n *<!-- footer close -->', footer_block, content, flags=re.DOTALL)

    # 5. Remove rounded classes to enforce 0px radius
    content = content.replace('rounded-1', '')
    content = content.replace('rounded-2', '')

    with open(filepath, 'w') as f:
        f.write(content)

update_file('blog.html')
update_file('blog-single.html')
print("Successfully updated blog.html and blog-single.html")
