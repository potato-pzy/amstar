import os
import re
from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/shop.html"
images_dir = "/home/potato/Documents/unwanted/Optilux HTML/drive-download-20260502T054600Z-3-001"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find the product container. It's inside <div class="col-lg-9"><div class="row g-4">
product_container = soup.select_one(".col-lg-9 .row.g-4")

if product_container:
    # Clear existing products
    product_container.clear()

    # List all images
    images = sorted(os.listdir(images_dir))
    
    for img in images:
        if not img.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
            
        # Extract name: remove extension
        name = os.path.splitext(img)[0]
        # remove trailing numbers in parenthesis like (1) or _
        name = re.sub(r'\(\d+\)$', '', name)
        name = name.replace('_', '"') # Some filenames might have _ instead of "
        
        # relative path for image
        img_path = f"drive-download-20260502T054600Z-3-001/{img}"
        
        # Create new product HTML
        product_html = f"""
        <!-- product item begin -->
        <div class="col-xl-4 col-lg-4 col-md-6">
            <div class="de__pcard text-center">
                <div class="atr__images" style="height: 250px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 20px;">
                    <a href="shop-product-single.html">
                        <img class="atr__image-main" src="{img_path}" style="max-height: 200px; width: auto; object-fit: contain;">
                    </a>
                    <div class="atr__extra-menu">
                        <a class="atr__quick-view" href="shop-product-single.html"><i class="icon_zoom-in_alt"></i></a>
                        <div class="atr__add-cart"><i class="icon_cart_alt"></i></div>
                    </div>
                </div>
                <h3 style="font-size: 16px; margin-top: 15px; margin-bottom: 15px;">{name}</h3>
                <a href="shop-product-single.html" class="btn-main w-100" style="padding: 10px; display: block; color: white;">View Details</a>
            </div>
        </div>
        <!-- product item end -->
        """
        
        # Append to container
        new_product = BeautifulSoup(product_html, "html.parser")
        product_container.append(new_product)

# Fix navbar CSS
style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    if css:
        # Replace main-nav css
        css = re.sub(r'#main-nav\s*\{[^}]*\}', 
"""#main-nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 5%;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }""", css)
        css = re.sub(r'@media[^{]*\{[^#]*#main-nav\s*\{[^}]*\}[^\}]*\}', 
"""@media (max-width: 991px) {
            #main-nav {
                padding: 15px 20px !important;
            }
        }""", css)
        style_tag.string.replace_with(css)

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully updated shop.html")
