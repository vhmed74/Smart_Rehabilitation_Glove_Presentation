import re

with open('index_backup.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract CSS and Scripts (everything before and after swiper-wrapper)
match = re.search(r'(<div class="swiper-wrapper">)(.*?)(</div>\s*<!-- Pagination -->)', content, re.DOTALL)
if not match:
    print("Could not find swiper-wrapper")
    exit(1)

pre_content = content[:match.start(2)]
slides_content = match.group(2)
post_content = content[match.end(2):]

# Find all slides
slides = re.split(r'<!-- ═+[^═]+═+ -->\s*<div class="swiper-slide">|<div class="swiper-slide">', slides_content)
slides = [s for s in slides if s.strip()] # filter empty

print(f"Found {len(slides)} slides.")

# Let's inspect the slides array to know what's where.
for i, s in enumerate(slides):
    # print a snippet of each slide to identify it
    snippet = s[:100].replace('\n', ' ')
    print(f"Slide {i+1}: {snippet}")
