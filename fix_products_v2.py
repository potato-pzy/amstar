from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/products.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Fix double navbar - remove all nav tags and we will insert one clean one
for nav in soup.find_all("nav"):
    nav.decompose()

# 2. Insert clean navbar and hero section at the top of body
body = soup.find("body")

# Standard Navbar
navbar_html = """
<nav id="main-nav" style="position: fixed; top: 40px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 1300px; background-color: #ffffff; display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; z-index: 1000; transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); border-radius: 4px;">
    <a href="master.html" style="display: flex; align-items: center; text-decoration: none;">
        <img src="images /Footer/Asset 2.svg" alt="Amstar Pumps" style="height: 55px; width: auto;">
    </a>
    <div style="display: flex; align-items: center; gap: 50px;">
        <div class="nav-links" style="display: flex; align-items: center; gap: 30px;">
            <a href="master.html" style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;" onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Home</a>
            <a href="shop.html" style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;" onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Products</a>
            <a href="#" style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;" onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Latest</a>
        </div>
        <a href="contact.html" style="background-color: #003366; color: #ffffff; padding: 12px 28px; border-radius: 0; font-weight: 400; transition: background-color 0.3s ease; text-decoration: none; font-size: 14.5px;" onmouseover="this.style.backgroundColor='#004fb1'" onmouseout="this.style.backgroundColor='#003366'">Book a Call</a>
    </div>
</nav>
"""

# Restored Hero Header
hero_html = """
<section id="subheader" style="background: url('images/background/subheader.webp') top / cover; padding: 180px 0 80px 0; margin-bottom: 50px;">
    <div class="container">
        <h1 class="hero-title" style="color: #ffffff; font-size: 48px; font-weight: 400; margin: 0;">Submersible System</h1>
    </div>
</section>
"""

# Re-inserting elements in order
loader = soup.find(id="de-loader")
insertion_point = 0
if loader:
    insertion_point = body.contents.index(loader) + 1

body.insert(insertion_point, BeautifulSoup(navbar_html, "html.parser"))
body.insert(insertion_point + 1, BeautifulSoup(hero_html, "html.parser"))

# 3. Restore default content in the product detail section
title_h1 = soup.find("h1", class_="product-title")
if title_h1:
    title_h1.string = '4" Submersible Motor'

main_img = soup.find("img", class_="product-image")
if main_img:
    main_img['src'] = 'images /product /Asset 2@3x-100.jpg.jpeg'
    main_img['alt'] = '4" Submersible Motor'

# 4. Clean up transition CSS (make sure things are visible by default but transitionable)
style_tags = soup.find_all("style")
for style in style_tags:
    if ".product-title, .product-image, .hero-title" in style.string:
        # Keep the transition but don't force opacity 0 here if we want immediate visibility of default
        # Actually, let's just make the JS reveal them.
        pass

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully restored hero section, fixed double navbar, and set default product content.")
