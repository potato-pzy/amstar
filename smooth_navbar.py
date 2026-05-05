import re

files = [
    'blog-1.html', 'blog-2.html', 'blog-3.html',
    'blog.html', 'blog-single.html', 'contact.html',
    'master.html', 'products.html', 'shop.html'
]

# New smooth navbar: 
#  - Longer, butter-smooth CSS transition (0.5s with ease-in-out)
#  - Scroll threshold of 60px before hiding (prevents jitter on small scrolls)
#  - Clean morphing from pill → full-width
#  - Smooth fade + slide on hide

new_nav_transition = 'transition: top 0.45s cubic-bezier(0.4, 0, 0.2, 1), left 0.45s cubic-bezier(0.4, 0, 0.2, 1), width 0.45s cubic-bezier(0.4, 0, 0.2, 1), max-width 0.45s cubic-bezier(0.4, 0, 0.2, 1), border-radius 0.45s cubic-bezier(0.4, 0, 0.2, 1), padding 0.45s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.45s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.45s cubic-bezier(0.4, 0, 0.2, 1);'

new_script = """<script>
    // Smooth navbar scroll behavior
    (function () {
        var navbar = document.getElementById("main-nav");
        if (!navbar) return;

        var lastScrollY = 0;
        var ticking = false;
        var isFullWidth = false;

        function setNavbarStyle(scrollY, direction) {
            if (scrollY < 60) {
                // Top of page: floating pill
                isFullWidth = false;
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
                // Expand to full-width only once
                if (!isFullWidth) {
                    isFullWidth = true;
                    navbar.style.left = "0";
                    navbar.style.transform = "none";
                    navbar.style.width = "100%";
                    navbar.style.maxWidth = "100%";
                    navbar.style.borderRadius = "0";
                    navbar.style.padding = "12px 5%";
                    navbar.style.boxShadow = "0 4px 20px rgba(0,0,0,0.12)";
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

old_script_pattern = r'<script>\s*//\s*(?:Smooth )?[Nn]avbar scroll behavior.*?\}\)\(\);\s*</script>'

for fname in files:
    try:
        with open(fname, 'r') as f:
            content = f.read()

        # 1. Replace the transition property in the nav inline style
        content = re.sub(
            r"transition:\s*all\s*0\.4s\s*cubic-bezier\(0\.25,\s*0\.8,\s*0\.25,\s*1\);",
            new_nav_transition,
            content
        )

        # 2. Replace the navbar scroll script
        new_content, n = re.subn(old_script_pattern, new_script, content, flags=re.DOTALL)
        if n == 0:
            print(f"  WARNING: Could not find/replace script in {fname}")
        
        with open(fname, 'w') as f:
            f.write(new_content)

        print(f"Updated {fname} (script replacements: {n})")

    except FileNotFoundError:
        print(f"SKIP: {fname} not found")
