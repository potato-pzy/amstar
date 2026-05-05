import re
import os

files = ['master.html', 'shop.html', 'products.html', 'blog.html', 
         'blog-1.html', 'blog-2.html', 'blog-3.html', 'contact.html']

# The new unified navbar scroll animation script
# Matches index.html behaviour: slides UP on scroll-down, reappears on scroll-up
NAVBAR_SCRIPT = """<script>
// Unified navbar scroll animation (matches index.html behaviour)
(function () {
    var navbar = document.getElementById('main-nav');
    if (!navbar) return;

    var lastScrollY = 0;
    var ticking = false;
    var SCROLL_THRESHOLD = 80; // px before hiding starts

    function updateNavbar() {
        var currentScrollY = window.scrollY || window.pageYOffset;

        if (currentScrollY <= 5) {
            // At top: floating pill
            navbar.style.top = '40px';
            navbar.style.left = '50%';
            navbar.style.transform = 'translateX(-50%)';
            navbar.style.width = '90%';
            navbar.style.maxWidth = '1560px';
            navbar.style.borderRadius = '4px';
            navbar.style.padding = '15px 40px';
            navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.08)';
            navbar.style.opacity = '1';
            navbar.style.pointerEvents = '';
        } else if (currentScrollY > lastScrollY && currentScrollY > SCROLL_THRESHOLD) {
            // Scrolling DOWN past threshold: slide navbar out of view (top)
            navbar.style.top = '-90px';
            navbar.style.left = '0';
            navbar.style.transform = 'none';
            navbar.style.width = '100%';
            navbar.style.maxWidth = '100%';
            navbar.style.borderRadius = '0';
            navbar.style.padding = '12px 5%';
            navbar.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
            navbar.style.opacity = '0';
            navbar.style.pointerEvents = 'none';
        } else if (currentScrollY < lastScrollY) {
            // Scrolling UP: snap to full-width sticky and show
            navbar.style.top = '0';
            navbar.style.left = '0';
            navbar.style.transform = 'none';
            navbar.style.width = '100%';
            navbar.style.maxWidth = '100%';
            navbar.style.borderRadius = '0';
            navbar.style.padding = '12px 5%';
            navbar.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
            navbar.style.opacity = '1';
            navbar.style.pointerEvents = '';
        }

        lastScrollY = currentScrollY;
        ticking = false;
    }

    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }, { passive: true });

    updateNavbar();
})();
</script>"""

# Regex to match any existing navbar scroll script block
OLD_SCRIPT_RE = re.compile(
    r'<script>\s*(?://[^\n]*\n)?\s*\(function\s*\(\s*\)\s*\{[^}]*navbar\s*=\s*document\.getElementById\(["\']main-nav["\']\).*?\}\)\(\);\s*</script>',
    re.DOTALL | re.IGNORECASE
)

for fname in files:
    if not os.path.exists(fname):
        print(f"SKIP (not found): {fname}")
        continue

    with open(fname, 'r') as f:
        content = f.read()

    if 'id="main-nav"' not in content and "id='main-nav'" not in content:
        print(f"SKIP (no main-nav): {fname}")
        continue

    # Remove ALL old navbar animation scripts
    new_content, count = OLD_SCRIPT_RE.subn('', content)
    
    # Inject the new script before </body>
    body_end = new_content.rfind('</body>')
    if body_end != -1:
        new_content = new_content[:body_end] + NAVBAR_SCRIPT + '\n' + new_content[body_end:]

    with open(fname, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {fname}: removed {count} old script(s), injected new animation")

