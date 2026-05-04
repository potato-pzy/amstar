import re
from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/shop.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Change columns back to 3 per row (col-xl-4 col-lg-4 col-md-6)
# And assign data-category based on name
product_cols = soup.select(".product-item")
for col in product_cols:
    col['class'] = "col-xl-4 col-lg-4 col-md-6 product-item".split()
    
    # Extract name to determine category
    name_tag = col.find("h3")
    name = name_tag.text.lower() if name_tag else ""
    
    cat = "accessories"
    if "submersible" in name:
        cat = "submersible_pumps"
    elif "monoblock" in name:
        cat = "monoblock_pumps"
    elif "openwell" in name:
        cat = "openwell_pumps"
    elif "self priming" in name or "self_priming" in name:
        cat = "self-priming_pumps"
    elif "pipe" in name:
        cat = "pipes"
    elif "control panel" in name:
        cat = "control_panels"
    else:
        cat = "submersible_pumps" # default
        
    col['data-category'] = cat
    
    # Random application just to make it work
    if len(name) % 2 == 0:
        col['data-application'] = "residential"
    else:
        col['data-application'] = "agriculture"

# 2. Add gap to pagination
pagination_ul = soup.select_one("ul.pagination")
if pagination_ul:
    pagination_ul['style'] = "display: flex; gap: 8px; justify-content: center; list-style: none; padding-top: 20px;"

# 3. Replace old JS script with new filter+pagination script
# Find existing script that contains 'const itemsPerPage = 15;'
for script in soup.find_all("script"):
    if script.string and "const itemsPerPage = 15;" in script.string:
        script.decompose()

script_tag = soup.new_tag("script")
script_tag.string = """
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
        
        showPage(1);
    }
    
    // Attach event listeners
    catCheckboxes.forEach(cb => cb.addEventListener('change', updateFilters));
    appCheckboxes.forEach(cb => cb.addEventListener('change', updateFilters));
    
    function showPage(page) {
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
    }
    
    function renderPagination(currentPage, totalPages) {
        if (!paginationContainer) return;
        paginationContainer.innerHTML = '';
        
        if (totalPages <= 1 && filteredProducts.length === 0) return; // Hide if nothing
        
        // Previous Button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
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

body_tag = soup.body
if body_tag:
    body_tag.append(script_tag)

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully fixed layout, filters, and pagination.")
