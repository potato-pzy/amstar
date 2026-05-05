import re
import PyPDF2

def get_pdf_text(filepath):
    reader = PyPDF2.PdfReader(filepath)
    text = ''
    for page in reader.pages:
        t = page.extract_text()
        # Replace '\n \n \n' with a unique token for paragraph
        t = t.replace('\n \n \n', '<PARA>')
        # Replace '\n \n' with space
        t = t.replace('\n \n', ' ')
        # Replace single '\n' with empty string
        t = t.replace('\n', '')
        text += t + '<PARA>'
    return text

def format_text_to_html(text):
    text = text.replace('AMST AR', 'AMSTAR')
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    
    paragraphs = text.split('<PARA>')
    html_paragraphs = []
    
    # We will ignore "Blog 1" and the main title, as they are usually the first few elements.
    # We will inject the actual title manually in the template.
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        # Ignore things that look like the main title or "Blog X" at the beginning
        # Actually, let's just let it be, but format headings.
        if p.startswith('Blog '):
            continue
            
        # If it's a short sentence and doesn't end with a punctuation, treat as heading
        if len(p) < 100 and not p.endswith('.') and not p.endswith(':') and p.istitle():
             # Exclude the exact main title from being a heading
             pass
             
        # Actually, just simple logic
        if len(p) < 100 and not p.endswith('.') and not p.endswith(',') and not p.endswith(':'):
            html_paragraphs.append(f'<h4 style="font-family: \'Alan Sans\', sans-serif; margin-top: 30px; font-weight: 600; color: #1a2b4c;">{p}</h4>')
        elif p.startswith('●'):
            html_paragraphs.append(f'<p style="font-family: \'Alan Sans\', sans-serif; margin-bottom: 10px; padding-left: 20px;">{p}</p>')
        else:
            html_paragraphs.append(f'<p style="font-family: \'Alan Sans\', sans-serif; margin-bottom: 20px; line-height: 1.8; color: #444;">{p}</p>')
            
    return '\n'.join(html_paragraphs)

with open('blog-single.html', 'r') as f:
    template = f.read()

blogs = [
    {
        'file': 'blog-1.html',
        'pdf': 'Blogs-1.pdf',
        'title': 'Our Journey Towards Carbon Neutral Manufacturing',
        'image': 'images/blog/1.webp'
    },
    {
        'file': 'blog-2.html',
        'pdf': 'Blogs-2.pdf',
        'title': 'The Evolution of Pump Efficiency',
        'image': 'images/blog/2.webp'
    },
    {
        'file': 'blog-3.html',
        'pdf': 'Blogs-3.pdf',
        'title': 'Solar Water Pumps and Sustainable Agriculture',
        'image': 'images/blog/3.webp'
    }
]

for blog in blogs:
    text = get_pdf_text(blog['pdf'])
    html_content = format_text_to_html(text)
    
    # Optional: remove the main title from the html_content to avoid duplication
    title_pattern = blog['title']
    html_content = html_content.replace(f'<h4 style="font-family: \'Alan Sans\', sans-serif; margin-top: 30px; font-weight: 600; color: #1a2b4c;">{title_pattern}</h4>', '')
    
    # Create the new block
    new_block = f"""<div class="row gx-5 justify-content-center">
                        <div class="col-lg-10">
                            <div class="blog-read">
                                <img src="{blog['image']}" class="w-100 mb-5" alt="{blog['title']}" style="border-radius: 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                                {html_content}
                            </div>
                        </div>
                    </div>"""
    
    # Replace the <div class="row gx-5"> block inside the main section
    page_content = re.sub(r'<div class="row gx-5">.*?</div>\s*</div>\s*</section>', new_block + '\n                </div>\n            </section>', template, flags=re.DOTALL)
    
    # Replace the title and breadcrumb
    page_content = re.sub(r'<h1 class="split">.*?</h1>', f'<h1 class="split" style="font-family: \'Alan Sans\', sans-serif;">{blog["title"]}</h1>', page_content)
    page_content = re.sub(r'<li class="active">.*?</li>', f'<li class="active">{blog["title"]}</li>', page_content)
    page_content = re.sub(r'<li><a href="index\.html">Home</a></li>', '<li><a href="master.html">Home</a></li>', page_content)
    
    # Remove the Clear Vision Starts Here section if it's there
    page_content = re.sub(r'<section class="bg-color relative text-light pt-50 pb-50">.*?</section>\s*</div>\s*<!-- content close -->', '</div>\n        <!-- content close -->', page_content, flags=re.DOTALL)
    
    # Write to file
    with open(blog['file'], 'w') as f:
        f.write(page_content)

print("Generated all 3 blog files successfully.")
