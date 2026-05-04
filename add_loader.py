from bs4 import BeautifulSoup

def add_loader(file_path):
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 1. Add loader HTML at the top of body
    body = soup.find("body")
    if body:
        # Check if loader already exists
        if not soup.find(id="de-loader"):
            loader_html = BeautifulSoup('<!-- page preloader begin -->\n<div id="de-loader"></div>\n<!-- page preloader close -->', "html.parser")
            body.insert(0, loader_html)

    # 2. Ensure CSS is present in head for immediate effect (optional but good for speed)
    # The style.css should handle it, but we can add a small block to keep it hidden until JS runs
    # (Actually the loader is usually visible by default and removed by JS)
    
    with open(file_path, "w") as f:
        f.write(str(soup))

add_loader("/home/potato/Documents/unwanted/Optilux HTML/shop.html")
add_loader("/home/potato/Documents/unwanted/Optilux HTML/products.html")
print("Successfully added page loader to all pages.")
