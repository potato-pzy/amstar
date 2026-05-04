from bs4 import BeautifulSoup
import urllib.parse

def update_page(file_path, is_products_page=False):
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Navbar updates
    # Home -> master.html
    # Products -> shop.html
    nav = soup.find("nav")
    if nav:
        for a in nav.find_all("a"):
            if a.text.strip().lower() == "home":
                a['href'] = "master.html"
            elif a.text.strip().lower() == "products":
                a['href'] = "shop.html"

    if is_products_page:
        # Remove hardcoded image and title to prevent flash
        title_h1 = soup.find("h1", class_="product-title")
        if title_h1:
            title_h1.string = "" # Clear it
        
        main_img = soup.find("img", class_="product-image")
        if main_img:
            main_img['src'] = "" # Clear it
            main_img['alt'] = ""
            
        hero_title = soup.find("h1", class_="hero-title")
        if hero_title:
            hero_title.string = "Product Details" # Generic starting title

        # Update the script to be even faster and handle the empty state
        for script in soup.find_all("script"):
            if script.string and "const params = new URLSearchParams(window.location.search);" in script.string:
                script.string = """
(function() {
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name');
    const img = params.get('img');
    
    function updateDOM() {
        if (name && img) {
            const mainImage = document.querySelector('.product-image');
            if (mainImage) mainImage.src = img;
            
            const productTitle = document.querySelector('.product-title');
            if (productTitle) productTitle.innerText = name;
            
            const heroTitle = document.querySelector('.hero-title');
            if (heroTitle) heroTitle.innerText = name;
            
            const pageTitle = document.querySelector('title');
            if (pageTitle) pageTitle.innerText = name + " - Product Details";
            
            document.querySelectorAll('.product-title, .product-image, .hero-title').forEach(el => el.style.opacity = '1');
        } else {
            // Default content if no params
            const productTitle = document.querySelector('.product-title');
            if (productTitle && !productTitle.innerText) productTitle.innerText = '4" Submersible Motor';
            
            const mainImage = document.querySelector('.product-image');
            if (mainImage && !mainImage.getAttribute('src')) mainImage.src = 'images /product /Asset 2@3x-100.jpg.jpeg';
            
            document.querySelectorAll('.product-title, .product-image, .hero-title').forEach(el => el.style.opacity = '1');
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateDOM);
    } else {
        updateDOM();
    }
})();
"""
    
    with open(file_path, "w") as f:
        f.write(str(soup))

update_page("/home/potato/Documents/unwanted/Optilux HTML/products.html", is_products_page=True)
update_page("/home/potato/Documents/unwanted/Optilux HTML/shop.html")
print("Successfully updated navbar links and fixed the placeholder flash.")
