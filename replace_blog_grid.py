import re

with open('blog.html', 'r') as f:
    content = f.read()

new_grid = """<div class="row g-4 gy-5">
                        <div class="col-lg-4 col-md-6 mb10">
                            <div class="hover">
                                <div class="post-image mb-2 overflow-hidden">
                                    <a href="blog-1.html">
                                        <img alt="" src="images/blog/1.webp" class="hover-scale-1-1">
                                    </a>
                                </div>
                                <div class="pt-2 h-100">
                                    <h4><a class="text-dark" href="blog-1.html" style="font-family: 'Alan Sans', sans-serif;">Our Journey Towards Carbon Neutral Manufacturing</a></h4>
                                    <p class="mb-3" style="font-family: 'Alan Sans', sans-serif;">At AMSTAR Pumps, progress has never been limited to performance alone...</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-4 col-md-6 mb10">
                            <div class="hover">
                                <div class="post-image mb-2 overflow-hidden">
                                    <a href="blog-2.html">
                                        <img alt="" src="images/blog/2.webp" class="hover-scale-1-1">
                                    </a>
                                </div>
                                <div class="pt-2 h-100">
                                    <h4><a class="text-dark" href="blog-2.html" style="font-family: 'Alan Sans', sans-serif;">The Evolution of Pump Efficiency</a></h4>
                                    <p class="mb-3" style="font-family: 'Alan Sans', sans-serif;">Efficiency is at the heart of modern pump design, but it hasn’t always been that way...</p>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-4 col-md-6 mb10">
                            <div class="hover">
                                <div class="post-image mb-2 overflow-hidden">
                                    <a href="blog-3.html">
                                        <img alt="" src="images/blog/3.webp" class="hover-scale-1-1">
                                    </a>
                                </div>
                                <div class="pt-2 h-100">
                                    <h4><a class="text-dark" href="blog-3.html" style="font-family: 'Alan Sans', sans-serif;">Solar Water Pumps and Sustainable Agriculture</a></h4>
                                    <p class="mb-3" style="font-family: 'Alan Sans', sans-serif;">Agriculture relies on water, and moving that water requires energy...</p>
                                </div>
                            </div>
                        </div>
                    </div>"""

content = re.sub(r'<div class="row g-4 gy-5">.*?</div>\s*</div>\s*</section>', new_grid + '\n                </div>\n            </section>', content, flags=re.DOTALL)

with open('blog.html', 'w') as f:
    f.write(content)

