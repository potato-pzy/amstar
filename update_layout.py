import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

override_css = """
    <style>
        /* 120% Zoom Layout Override */
        @media (min-width: 1200px) {
            .container, .container-lg, .container-md, .container-sm, .container-xl, .container-xxl {
                max-width: 1368px !important;
            }
        }
        @media (min-width: 1400px) {
            .container, .container-lg, .container-md, .container-sm, .container-xl, .container-xxl {
                max-width: 1584px !important;
            }
        }
    </style>
"""

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Increase max-width for pm-nav-inner
    content = content.replace('max-width: 1200px;', 'max-width: 1440px;')
    
    # Increase max-width for main-nav (inline styles)
    content = content.replace('max-width: 1300px;', 'max-width: 1560px;')
    
    # Also in master.html line 790: <div class="container relative z-2" style="max-width: 1400px;">
    content = content.replace('max-width: 1400px;', 'max-width: 1680px;')
    
    # Inject the override CSS right before </head> if not already there
    if '/* 120% Zoom Layout Override */' not in content:
        head_end = content.find('</head>')
        if head_end != -1:
            content = content[:head_end] + override_css + content[head_end:]

    with open(file, 'w') as f:
        f.write(content)

print("Updated all HTML files for wider layout.")
