import re
from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/shop.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# Fix categorization default
product_cols = soup.select(".product-item")
for col in product_cols:
    name_tag = col.find("h3")
    name = name_tag.text.lower() if name_tag else ""
    
    if "submersible" in name:
        cat = "submersible_pumps"
    elif "monoblock" in name:
        cat = "monoblock_pumps"
    elif "openwell" in name:
        cat = "openwell_pumps"
    elif "self priming" in name or "self-priming" in name or "self_priming" in name:
        cat = "self-priming_pumps"
    elif "pipe" in name:
        cat = "pipes"
    elif "control panel" in name:
        cat = "control_panels"
    else:
        cat = "other_pumps" # Don't default to submersible
        
    col['data-category'] = cat

# Make sure "Other Pumps" exists as a filter if not present
# Actually, I'll just change the default to not be submersible. If it's not checked, it won't show, but "All" (no checkboxes) will show everything.

# Find existing script and replace it
for script in soup.find_all("script"):
    if script.string and "const itemsPerPage = 15;" in script.string:
        script.string = """
document.addEventListener("DOMContentLoaded", function() {
    const itemsPerPage = 15;
    const allProducts = Array.from(document.querySelectorAll('.product-item'));
    const paginationContainer = document.getElementById('dynamic-pagination');
    let filteredProducts = [...allProducts];
    
    // Checkboxes
    const catCheckboxes = document.querySelectorAll('input[id^="cat_"]');
    const appCheckboxes = document.querySelectorAll('input[id^="app_"]');
    
    function updateFilters() {
        const activeCats = Array.from(catCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
        const activeApps = Array.from(appCheckboxes).filter(cb => cb.checked).map(cb => cb.value);
        
        filteredProducts = allProducts.filter(item => {
            const itemCat = item.getAttribute('data-category');
            const itemApp = item.getAttribute('data-application');
            
            const catMatch = activeCats.length === 0 || activeCats.includes(itemCat);
            const appMatch = activeApps.length === 0 || activeApps.includes(itemApp);
            
            return catMatch && appMatch;
        });
        
        showPage(1, false);
    }
    
    // Attach event listeners
    catCheckboxes.forEach(cb => cb.addEventListener('change', updateFilters));
    appCheckboxes.forEach(cb => cb.addEventListener('change', updateFilters));
    
    function showPage(page, scroll = true) {
        // Hide all original products
        allProducts.forEach(item => item.style.display = 'none');
        
        const totalPages = Math.ceil(filteredProducts.length / itemsPerPage) || 1;
        // Enforce bounds
        page = Math.max(1, Math.min(page, totalPages));
        
        // Calculate start and end
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        
        // Show current page items
        for(let i = start; i < end && i < filteredProducts.length; i++) {
            filteredProducts[i].style.display = 'block';
        }
        
        renderPagination(page, totalPages);
        
        // Scroll to top of the page smoothly
        if(scroll) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    function renderPagination(currentPage, totalPages) {
        if (!paginationContainer) return;
        paginationContainer.innerHTML = '';
        
        if (totalPages <= 1 && filteredProducts.length === 0) return; // Hide if nothing
        
        // Previous Button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        prevLi.style.margin = '0 10px';
        const prevA = document.createElement('a');
        prevA.className = 'page-link';
        prevA.href = 'javascript:void(0)';
        prevA.innerText = 'Prev';
        prevA.style.padding = '8px 16px';
        prevA.style.borderRadius = '0';
        if (currentPage > 1) {
            prevA.onclick = (e) => { e.preventDefault(); showPage(currentPage - 1); };
        }
        prevLi.appendChild(prevA);
        paginationContainer.appendChild(prevLi);
        
        // Page Numbers
        for(let i = 1; i <= totalPages; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === currentPage ? 'active' : ''}`;
            li.style.margin = '0 5px';
            const a = document.createElement('a');
            a.className = 'page-link';
            a.href = 'javascript:void(0)';
            a.innerText = i;
            a.style.padding = '8px 16px';
            a.style.borderRadius = '0';
            a.onclick = (e) => { e.preventDefault(); showPage(i); };
            li.appendChild(a);
            paginationContainer.appendChild(li);
        }
        
        // Next Button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.style.margin = '0 10px';
        const nextA = document.createElement('a');
        nextA.className = 'page-link';
        nextA.href = 'javascript:void(0)';
        nextA.innerText = 'Next';
        nextA.style.padding = '8px 16px';
        nextA.style.borderRadius = '0';
        if (currentPage < totalPages) {
            nextA.onclick = (e) => { e.preventDefault(); showPage(currentPage + 1); };
        }
        nextLi.appendChild(nextA);
        paginationContainer.appendChild(nextLi);
    }
    
    // Initialize
    updateFilters();
});
"""

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully fixed scroll, spacing, and filters.")
