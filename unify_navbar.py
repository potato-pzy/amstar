import re
from bs4 import BeautifulSoup

def unify_navbar(file_path):
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # The exact Navbar from master.html (with my links)
    new_navbar_html = """
        <nav id="main-nav"
            style="position: fixed; top: 40px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 1300px; background-color: #ffffff; display: flex; justify-content: space-between; align-items: center; padding: 15px 40px; z-index: 1000; transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); border-radius: 4px;">
            <!-- Logo -->
            <a href="master.html" style="display: flex; align-items: center; text-decoration: none;">
                <img src="images /Footer/Asset 2.svg" alt="Amstar Pumps" style="height: 55px; width: auto;">
            </a>

            <!-- Links and Button Group -->
            <div style="display: flex; align-items: center; gap: 50px;">
                <div class="nav-links" style="display: flex; align-items: center; gap: 30px;">
                    <a href="master.html"
                        style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;"
                        onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Home</a>
                    <a href="shop.html"
                        style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;"
                        onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Products</a>
                    <a href="#"
                        style="text-decoration: none; color: #1a2b4c; font-weight: 400; font-size: 15px; transition: color 0.3s ease;"
                        onmouseover="this.style.color='#004fb1'" onmouseout="this.style.color='#1a2b4c'">Latest</a>
                </div>
                <a href="contact.html"
                    style="background-color: #003366; color: #ffffff; padding: 12px 28px; border-radius: 0; font-weight: 400; transition: background-color 0.3s ease; text-decoration: none; font-size: 14.5px;"
                    onmouseover="this.style.backgroundColor='#004fb1'"
                    onmouseout="this.style.backgroundColor='#003366'">Book a Call</a>
            </div>
        </nav>
    """
    
    # Replace existing #main-nav
    old_nav = soup.find(id="main-nav")
    if old_nav:
        new_nav_soup = BeautifulSoup(new_navbar_html, "html.parser")
        old_nav.replace_with(new_nav_soup)
    
    # Ensure the script is present and updated
    # (The script I added in the previous turn is already quite good, but let's make sure it's consistent)
    
    with open(file_path, "w") as f:
        f.write(str(soup))

unify_navbar("/home/potato/Documents/unwanted/Optilux HTML/shop.html")
unify_navbar("/home/potato/Documents/unwanted/Optilux HTML/products.html")
print("Successfully unified navbar structure across all pages.")
