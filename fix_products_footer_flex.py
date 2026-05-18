import re

flex_footer = """<!-- ============================================================ -->
<!-- CUSTOM FOOTER (FLEXBOX)                                       -->
<!-- ============================================================ -->
<footer id="main-footer" style="background-color: #004fb1; padding: 80px 0 30px 0; color: #ffffff; font-family: 'Alan Sans', sans-serif; overflow: hidden;">
    <div style="max-width: 1560px; margin: 0 auto; padding: 0 15px; width: 100%;">
        <div style="display: flex; flex-wrap: wrap; margin: 0 -15px;">
            
            <!-- Branding and Certifications -->
            <div style="flex: 0 0 auto; width: 41.66666667%; padding: 0 15px; margin-bottom: 3rem;">
                <div style="margin-bottom: 30px;">
                    <img alt="Amstar Pumps" src="images /Footer/Asset 2.svg" style="height: 100px; width: auto;"/>
                </div>
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img alt="Certifications" src="images /Footer/Certification logos.png" style="height: 45px; width: auto;"/>
                </div>
            </div>

            <!-- Links Col 1 -->
            <div style="flex: 0 0 auto; width: 16.66666667%; padding: 0 15px; margin-bottom: 1.5rem;">
                <ul style="list-style: none; padding: 0; margin: 0; line-height: 2.5; font-size: 16px;">
                    <li><a href="about.html" style="color: #ffffff; text-decoration: none;">About</a></li>
                    <li><a href="shop.html" style="color: #ffffff; text-decoration: none;">Products</a></li>
                    <li><a href="gallery.html" style="color: #ffffff; text-decoration: none;">Gallery</a></li>
                    <li><a href="blog.html" style="color: #ffffff; text-decoration: none;">Blogs</a></li>
                </ul>
            </div>

            <!-- Links Col 2 -->
            <div style="flex: 0 0 auto; width: 16.66666667%; padding: 0 15px; margin-bottom: 1.5rem;">
                <ul style="list-style: none; padding: 0; margin: 0; line-height: 2.5; font-size: 16px;">
                    <li><a href="contact.html" style="color: #ffffff; text-decoration: none;">Contact Us</a></li>
                    <li><a href="about.html#profile" style="color: #ffffff; text-decoration: none;">Company Profile</a></li>
                </ul>
            </div>

            <!-- Contact Details -->
            <div style="flex: 0 0 auto; width: 25%; padding: 0 15px;">
                <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                    <img alt="Location" src="images /Footer/Location icon.svg" style="width: 18px; height: 18px; flex-shrink: 0; margin-top: 4px; filter: brightness(0) invert(1);"/>
                    <p style="margin: 0; font-size: 14px; line-height: 1.5; opacity: 0.9;">
                        Amstar Pumps<br/>
                        Door No. 214, Lenin Street, Vilankurichi,<br/>
                        Coimbatore, Tamil Nadu<br/>
                        641035, India
                    </p>
                </div>
                <div style="display: flex; gap: 15px; margin-bottom: 20px; align-items: center;">
                    <img alt="Phone" src="images /Footer/Phone Icon.svg" style="width: 18px; height: 18px; flex-shrink: 0; filter: brightness(0) invert(1);"/>
                    <p style="margin: 0; font-size: 14px; opacity: 0.9;">
                        +91 95001 84003 | +91 95001 36003
                    </p>
                </div>
                <div style="display: flex; gap: 15px; align-items: flex-start;">
                    <img alt="Mail" src="images /Footer/Mail Icon.svg" style="width: 18px; height: 18px; flex-shrink: 0; margin-top: 4px; filter: brightness(0) invert(1);"/>
                    <p style="margin: 0; font-size: 14px; line-height: 1.5; opacity: 0.9;">
                        info@amstarpumps.com<br/>
                        export@amstarpumps.com
                    </p>
                </div>
            </div>

        </div>

        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.3);">
            <p style="margin: 0; font-size: 14px; opacity: 0.8;">
                ©Amstar-2026 all rights reserved
            </p>
        </div>
    </div>
    
    <!-- Mobile responsiveness style -->
    <style>
        @media (max-width: 991px) {
            #main-footer > div > div > div {
                width: 100% !important;
            }
        }
    </style>
</footer>
<!-- footer close -->"""

with open('products.html', 'r') as f:
    content = f.read()

# Replace the footer
content = re.sub(r'<footer id="main-footer".*?</footer[^>]*>\n* *<!-- footer close -->', flex_footer, content, flags=re.DOTALL)

with open('products.html', 'w') as f:
    f.write(content)

print("Replaced products.html footer with flexbox version")
