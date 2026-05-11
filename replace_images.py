import re
import urllib.parse

def main():
    shop_file = '/home/potato/Documents/unwanted/Optilux HTML/shop.html'
    with open(shop_file, 'r', encoding='utf-8') as f:
        content = f.read()

    images = [
        "4” Submersible Motor.webp",
        "4” Submersible Pump.webp",
        "6” Submersible Motor.webp",
        "6” Submersible Motor(1).webp",
        "6” Submersible Motor.webp",
        "6” Submersible Pump.webp",
        "8_ Submersible Pump.webp",
        "8” Submersible Motor.webp",
        "Booster Pump.webp",
        "Cables.webp",
        "Centrifugal Pump.webp",
        "Circulatory Pump.webp",
        "Control Panel.webp",
        "De Water Pump.webp",
        "Monoblock(1).webp",
        "Monoblock.webp",
        "Openwell Single Phase.webp",
        "Openwell Three Phase.webp",
        "Pipe.webp",
        "Self Priming.webp",
        "Sewage Pump.webp",
        "Splitcase Pump.webp",
        "Vertical Multistage Pump.webp",
        "Vertical Openwell.webp"
    ]

    # Find all product items
    pattern = re.compile(r'(<div class="product-item".*?</div>\s*</div>\s*</div>\s*</div>)', re.DOTALL)
    
    parts = []
    last_end = 0
    img_idx = 0
    
    for m in pattern.finditer(content):
        parts.append(content[last_end:m.start()])
        block = m.group(1)
        
        if img_idx < len(images):
            img_name = images[img_idx]
            base_path = "images/Compressed 2/Compressed 2/" + img_name
            encoded_path = urllib.parse.quote(base_path)
            
            # Replace src="product-images/..." with src="images/..."
            block = re.sub(r'src="product-images/[^"]+"', f'src="{base_path}"', block)
            
            # Replace img=product-images%2F... with img=images%2FCompressed%202...
            block = re.sub(r'img=product-images(?:%2F|/)[^"]+(?=")', f'img={encoded_path}', block)
            
            img_idx += 1
            
        parts.append(block)
        last_end = m.end()
        
    parts.append(content[last_end:])
    
    new_content = "".join(parts)
    
    with open(shop_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Replaced {img_idx} image sections.")

if __name__ == '__main__':
    main()
