from bs4 import BeautifulSoup
import urllib.parse

html_file = "/home/potato/Documents/unwanted/Optilux HTML/shop.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

product_cols = soup.select(".product-item")
for col in product_cols:
    name_tag = col.find("h3")
    name = name_tag.text if name_tag else ""
    
    img_tag = col.find("img", class_="atr__image-main")
    img_src = img_tag['src'] if img_tag else ""
    
    # URL encode parameters
    params = urllib.parse.urlencode({'name': name, 'img': img_src})
    new_href = f"products.html?{params}"
    
    # Update links
    links = col.find_all("a")
    for link in links:
        if link.get('href') == "shop-product-single.html":
            link['href'] = new_href

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully updated shop.html links")
