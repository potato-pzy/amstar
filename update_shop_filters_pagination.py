import re
from bs4 import BeautifulSoup

html_file = "/home/potato/Documents/unwanted/Optilux HTML/shop.html"

with open(html_file, "r") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1. Update Filters
# Find Categories and Brands
categories_header = soup.find(lambda tag: tag.name == "h4" and "Categories" in tag.text)
if categories_header:
    form = categories_header.find_next_sibling("div", class_="de_form")
    if form:
        form.clear()
        cats = ["Submersible Pumps", "Monoblock Pumps", "Openwell Pumps", "Self-Priming Pumps", "Pipes", "Control Panels"]
        for i, cat in enumerate(cats, 1):
            div = soup.new_tag("div", attrs={"class": "de_checkbox"})
            input_tag = soup.new_tag("input", attrs={"id": f"cat_{i}", "name": f"cat_{i}", "type": "checkbox", "value": cat.lower().replace(' ', '_')})
            label_tag = soup.new_tag("label", attrs={"for": f"cat_{i}"})
            label_tag.string = cat
            div.append(input_tag)
            div.append(label_tag)
            form.append(div)

brands_header = soup.find(lambda tag: tag.name == "h4" and "Brands" in tag.text)
if brands_header:
    brands_header.string = "Application"
    form = brands_header.find_next_sibling("div", class_="de_form")
    if form:
        form.clear()
        apps = ["Agriculture", "Residential", "Industrial", "Commercial"]
        for i, app in enumerate(apps, 1):
            div = soup.new_tag("div", attrs={"class": "de_checkbox"})
            input_tag = soup.new_tag("input", attrs={"id": f"app_{i}", "name": f"app_{i}", "type": "checkbox", "value": app.lower()})
            label_tag = soup.new_tag("label", attrs={"for": f"app_{i}"})
            label_tag.string = app
            div.append(input_tag)
            div.append(label_tag)
            form.append(div)

# 2. Make Products Bigger (change 3 columns to 2 columns)
# Also add a class 'product-item' to them for pagination JS
product_cols = soup.select(".col-xl-4.col-lg-4.col-md-6")
for col in product_cols:
    col['class'] = "col-xl-6 col-lg-6 col-md-6 product-item".split()

# 3. Add Pagination ID to the container
product_container = soup.select_one(".col-lg-9 .row.g-4")
if product_container:
    product_container['id'] = 'product-list-container'

# 4. Modify existing Pagination HTML
pagination_ul = soup.select_one("ul.pagination")
if pagination_ul:
    pagination_ul['id'] = 'dynamic-pagination'
    pagination_ul.clear() # clear existing static links

# 5. Add Pagination Script
script_tag = soup.new_tag("script")
script_tag.string = """
document.addEventListener("DOMContentLoaded", function() {
    const itemsPerPage = 15;
    const productItems = document.querySelectorAll('.product-item');
    const paginationContainer = document.getElementById('dynamic-pagination');
    const totalPages = Math.ceil(productItems.length / itemsPerPage);
    
    function showPage(page) {
        // Hide all
        productItems.forEach(item => item.style.display = 'none');
        
        // Calculate start and end
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        
        // Show current page items
        for(let i = start; i < end && i < productItems.length; i++) {
            productItems[i].style.display = 'block';
        }
        
        renderPagination(page);
        
        // Scroll to top of list
        document.getElementById('product-list-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    function renderPagination(currentPage) {
        if (!paginationContainer) return;
        paginationContainer.innerHTML = '';
        
        // Previous Button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        const prevA = document.createElement('a');
        prevA.className = 'page-link';
        prevA.href = 'javascript:void(0)';
        prevA.innerText = 'Previous';
        if (currentPage > 1) {
            prevA.onclick = () => showPage(currentPage - 1);
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
            a.onclick = () => showPage(i);
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
        if (currentPage < totalPages) {
            nextA.onclick = () => showPage(currentPage + 1);
        }
        nextLi.appendChild(nextA);
        paginationContainer.appendChild(nextLi);
    }
    
    // Initialize
    if (productItems.length > 0) {
        showPage(1);
    }
});
"""
body_tag = soup.body
if body_tag:
    body_tag.append(script_tag)

with open(html_file, "w") as f:
    f.write(str(soup))

print("Successfully updated filters, layout, and pagination in shop.html")
