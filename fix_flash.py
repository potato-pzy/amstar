from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/products.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# Add a style to hide elements initially if there are URL params
style_tag = soup.new_tag("style")
style_tag.string = """
    .product-title, .product-image, .hero-title {
        transition: opacity 0.2s ease-in;
    }
    .loading-dynamic {
        opacity: 0 !important;
    }
"""
soup.head.append(style_tag)

# Add an inline script at the top of body to add the loading class if params exist
inline_script = soup.new_tag("script")
inline_script.string = """
    (function() {
        const params = new URLSearchParams(window.location.search);
        if (params.has('name') || params.has('img')) {
            document.documentElement.classList.add('is-loading-product');
            document.write('<style>.product-title, .product-image, .hero-title { opacity: 0; }</style>');
        }
    })();
"""
soup.body.insert(0, inline_script)

# Update the existing dynamic loader script to reveal the elements
for script in soup.find_all("script"):
    if script.string and "const params = new URLSearchParams(window.location.search);" in script.string:
        # Find the end of the if (name && img) block or just add to the end of the function
        new_logic = script.string.replace(
            "if (pageTitle) pageTitle.innerText = name + \" - Product Details\";",
            "if (pageTitle) pageTitle.innerText = name + \" - Product Details\";\n                document.querySelectorAll('.product-title, .product-image, .hero-title').forEach(el => el.style.opacity = '1');"
        )
        # Also handle the case where params DON'T exist (default content should be visible)
        new_logic = new_logic.replace(
            "updateFilters();", # Wait, updateFilters was in shop.html. products.html has different logic.
            "// ... existing init ..."
        )
        # Let's just append a "reveal" at the end of DOMContentLoaded
        if "document.addEventListener(\"DOMContentLoaded\"" in new_logic:
             new_logic = new_logic.replace(
                 "updateFilters();", "" # cleanup from previous messy logic if any
             )
             # Ensure that even if params are missing, we show the content
             new_logic += "\n        if (!window.location.search.includes('name')) { document.querySelectorAll('.product-title, .product-image, .hero-title').forEach(el => el.style.opacity = '1'); }"
        
        script.string = new_logic

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully fixed the flash of original content")
