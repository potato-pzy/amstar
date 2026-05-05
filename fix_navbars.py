import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

navbar_script = """<script>
    // Navbar scroll behavior
    (function () {
        var navbar = document.getElementById("main-nav");
        if (!navbar) return;

        var lastScrollY = 0;
        var ticking = false;

        function setNavbarStyle(scrollY, direction) {
            if (scrollY < 5) {
                // Top of page: floating pill
                navbar.style.top = "40px";
                navbar.style.left = "50%";
                navbar.style.transform = "translateX(-50%)";
                navbar.style.width = "90%";
                navbar.style.maxWidth = "1560px";
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
            var currentScrollY = window.scrollY || window.pageYOffset;
            var direction = currentScrollY > lastScrollY ? "down" : "up";
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
</script>"""

regex_pattern = r'<script>\s*(?:// Navbar scroll behavior[^\n]*\n)?\s*(?:\(|function).*?navbar\s*=\s*document\.getElementById\("main-nav"\).*?\}\)\(\);\s*</script>'

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # If the file has a main-nav, we process it
    if 'id="main-nav"' in content:
        # First, try to replace existing script
        new_content, count = re.subn(regex_pattern, navbar_script, content, flags=re.DOTALL | re.IGNORECASE)
        
        # If no replacement was made, inject it before </body>
        if count == 0:
            body_end = new_content.rfind('</body>')
            if body_end != -1:
                new_content = new_content[:body_end] + navbar_script + "\n" + new_content[body_end:]
            else:
                new_content += "\n" + navbar_script

        with open(file, 'w') as f:
            f.write(new_content)
        print(f"Updated {file} ({'Replaced existing' if count > 0 else 'Injected new'})")
