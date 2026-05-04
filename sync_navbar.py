import re
from bs4 import BeautifulSoup

def update_navbar_behavior(file_path):
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 1. Update CSS
    style_tag = soup.find('style')
    if not style_tag:
        style_tag = soup.new_tag("style")
        soup.head.append(style_tag)
    
    navbar_css = """
        /* Navbar Overrides for Animation */
        #main-nav {
            position: fixed;
            top: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 1300px;
            background-color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            z-index: 1000;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
        }

        @media (max-width: 991px) {
            #main-nav {
                width: 95% !important;
                padding: 15px 20px !important;
                top: 20px !important;
            }
        }
    """
    # Replace old navbar css if exists, otherwise append
    if style_tag.string:
        # Try to find and replace existing #main-nav block
        new_css = re.sub(r'#main-nav\s*\{[^}]*\}', navbar_css.strip(), style_tag.string)
        if new_css == style_tag.string: # not found
             style_tag.string += navbar_css
        else:
             style_tag.string = new_css
    else:
        style_tag.string = navbar_css

    # 2. Update Script
    # Remove any existing scroll script to avoid conflicts
    for script in soup.find_all("script"):
        if script.string and "window.addEventListener(\"scroll\"" in script.string and "setNavbarStyle" in script.string:
            script.decompose()
        elif script.string and "const navbar = document.getElementById(\"main-nav\");" in script.string:
            script.decompose()

    scroll_script = """
        (function () {
            const navbar = document.getElementById("main-nav");
            if (!navbar) return;

            let lastScrollY = 0;
            let ticking = false;

            function setNavbarStyle(scrollY, direction) {
                if (scrollY < 5) {
                    // Top of page: floating pill
                    navbar.style.top = "40px";
                    navbar.style.left = "50%";
                    navbar.style.transform = "translateX(-50%)";
                    navbar.style.width = "90%";
                    navbar.style.maxWidth = "1300px";
                    navbar.style.borderRadius = "4px";
                    navbar.style.padding = "15px 40px";
                    navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,0.08)";
                    navbar.style.opacity = "1";
                    navbar.style.pointerEvents = "";
                } else {
                    // Scrolled: full-width sticky
                    if (navbar.style.left !== "0px" && navbar.style.left !== "0") {
                        navbar.style.left = "0";
                        navbar.style.transform = "none";
                        navbar.style.width = "100%";
                        navbar.style.maxWidth = "100%";
                        navbar.style.borderRadius = "0";
                        navbar.style.padding = "12px 5%";
                        navbar.style.boxShadow = "0 4px 15px rgba(0,0,0,0.1)";
                    }
                    if (direction === "down") {
                        navbar.style.top = "-90px";
                        navbar.style.opacity = "0";
                        navbar.style.pointerEvents = "none";
                    } else {
                        navbar.style.top = "0";
                        navbar.style.opacity = "1";
                        navbar.style.pointerEvents = "";
                    }
                }
            }

            window.addEventListener("scroll", function () {
                const currentScrollY = window.scrollY || window.pageYOffset;
                const direction = currentScrollY > lastScrollY ? "down" : "up";
                if (!ticking) {
                    window.requestAnimationFrame(function () {
                        setNavbarStyle(currentScrollY, direction);
                        lastScrollY = currentScrollY;
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });

            setNavbarStyle(0, "up");
        })();
    """
    new_script_tag = soup.new_tag("script")
    new_script_tag.string = scroll_script
    soup.body.append(new_script_tag)

    with open(file_path, "w") as f:
        f.write(str(soup))

update_navbar_behavior("/home/potato/Documents/unwanted/Optilux HTML/shop.html")
update_navbar_behavior("/home/potato/Documents/unwanted/Optilux HTML/products.html")
print("Successfully synced navbar animation from master.html to other pages.")
