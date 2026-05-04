import re
from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/products.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find the specific script tag that has `function requestQuote()`
for script in soup.find_all("script"):
    if script.string and "function requestQuote()" in script.string:
        # Replace the hardcoded requestQuote function to be dynamic
        script.string = script.string.replace(
            """const message = `You have successfully requested a quote for the <strong>4" Submersible Motor</strong>.<br><br><strong>Variant:</strong> ${selectedVariant} HP<br><strong>Cycle:</strong> ${selectedCycle}`;""",
            """const productName = document.querySelector('.product-title').innerText;
            const message = `You have successfully requested a quote for the <strong>${productName}</strong>.<br><br><strong>Variant:</strong> ${selectedVariant} HP<br><strong>Cycle:</strong> ${selectedCycle}`;"""
        )
        
        # Add the dynamic URL parsing code to the beginning of the script
        dynamic_js = """
        // Dynamic Product Loader
        document.addEventListener("DOMContentLoaded", function() {
            const params = new URLSearchParams(window.location.search);
            const name = params.get('name');
            const img = params.get('img');
            
            if (name && img) {
                // Update Image
                const mainImage = document.querySelector('.product-image');
                if (mainImage) mainImage.src = img;
                
                // Update Titles
                const productTitle = document.querySelector('.product-title');
                if (productTitle) productTitle.innerText = name;
                
                const heroTitle = document.querySelector('.hero-title');
                if (heroTitle) heroTitle.innerText = name;
                
                const pageTitle = document.querySelector('title');
                if (pageTitle) pageTitle.innerText = name + " - Product Details";
            }
        });
        """
        script.string = dynamic_js + script.string

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully updated products.html for dynamic loading")
