import os
from datetime import datetime
import yaml

# --- CONFIG ---
IMAGES_ROOT = "images/Christmas/Santa"  # folder containing images
POSTS_DIR = "_posts"  # Jekyll _posts folder
CATEGORY = ["christmas", "santa"]  # categories for this folder
SEO_KEYWORDS = ["Santa", "Christmas Coloring Pages", "Free Printables PDF",
                "xmas printable coloring pages", "easy coloring pages for kids"]

CAPTION_DEFAULT = "Color and enjoy! Perfect for kids' fun and creativity."

os.makedirs(POSTS_DIR, exist_ok=True)

# --- FUNCTIONS ---
def slugify(filename):
    """Create URL-friendly slug from filename"""
    name, _ = os.path.splitext(filename)
    return name.lower().replace(" ", "-")

def generate_post(image_path):
    """Generate a Jekyll post markdown file for a given image"""
    filename = os.path.basename(image_path)
    slug = slugify(filename)
    date_str = datetime.now().strftime("%Y-%m-%d")

    title = " ".join([w.capitalize() for w in slug.split("-")])
    alt_text = ", ".join(SEO_KEYWORDS)

    front_matter = {
        "layout": "post",
        "title": title,
        "date": date_str,
        "categories": CATEGORY,
        "image": "/" + image_path.replace("\\","/"),
        "alt": alt_text,
        "caption": CAPTION_DEFAULT,
        "image_only": True,
        "views": 0,
        "trending": False
    }

    markdown = "---\n" + yaml.dump(front_matter, sort_keys=False) + "---\n"

    post_file = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")
    with open(post_file, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Created post: {post_file}")

# --- MAIN ---
for file in os.listdir(IMAGES_ROOT):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        generate_post(os.path.join(IMAGES_ROOT, file))
