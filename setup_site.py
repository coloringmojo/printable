import os
from datetime import datetime
import yaml
import subprocess

# --- CONFIG ---
IMAGES_ROOT = "Images"        # change to your folder (case-sensitive)
POSTS_DIR = "_posts"
layouts_folder = "_layouts"
css_folder = "css"
GITHUB_REMOTE = "origin"      # remote name
DEFAULT_KEYWORDS = ["Coloring Pages", "Free Printables PDF", "xmas printable coloring pages", "easy coloring pages for kids"]
CAPTION_DEFAULT = "Color and enjoy! Perfect for kids' fun and creativity."

# --- CREATE LAYOUTS & CSS ---
files_content = {
    f"{layouts_folder}/default.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<title>{{ page.title }} | ColoringMojo</title>\n<link rel=\"stylesheet\" href=\"{{ '/css/override.css' | relative_url }}\">\n</head>\n<body>\n<header>\n  <h1><a href=\"{{ site.baseurl }}/\">ColoringMojo</a></h1>\n  <nav>\n    <a href=\"{{ site.baseurl }}/\">Home</a> | \n    <a href=\"{{ site.baseurl }}/all-posts.html\">All Posts</a>\n  </nav>\n</header>\n<main>\n  {{ content }}\n</main>\n<footer>\n  <p>&copy; 2025 ColoringMojo. All Rights Reserved.</p>\n</footer>\n</body>\n</html>",
    f"{layouts_folder}/gallery.html": """---
layout: default
---
{% assign sections = site.categories | keys %}
{% for section in sections %}
  <h2>{{ section | capitalize }}</h2>
  <div class="section-grid">
    {% assign posts_in_section = site.categories[section] %}
    {% for post in posts_in_section %}
      <div class="image-card">
        <a href="{{ post.url | relative_url }}">
          <div class="image-overlay">
            <span class="views">{{ post.views }} views</span>
            {% if post.trending %}<span class="trending">🔥</span>{% endif %}
            <span class="pin-button">📌</span>
          </div>
          <img src="{{ post.image }}" alt="{{ post.alt }}">
        </a>
        {% if post.caption %}<p class="caption">{{ post.caption }}</p>{% endif %}
      </div>
    {% endfor %}
  </div>
{% endfor %}
<style>
.section-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1.5em; margin-bottom:3em; }
.image-card { position:relative; border:1px solid #ddd; border-radius:15px; overflow:hidden; transition:transform 0.2s; background:#fff;}
.image-card:hover{transform:scale(1.03);}
.image-card img{width:100%; border-radius:15px;}
.caption{font-size:0.85em; padding:0.3em; text-align:center;}
.image-overlay{position:absolute; top:5px; left:5px; display:flex; gap:0.5em;}
.image-overlay span{background:rgba(0,0,0,0.6); color:#fff; padding:2px 5px; border-radius:5px; font-size:0.8em;}
.trending{color:#ff6f61;}
.pin-button{cursor:pointer;}
</style>""",
    f"{layouts_folder}/post.html": """---
layout: default
---
<nav class="breadcrumbs"><a href="{{ site.baseurl }}/">Home</a> / {% for cat in page.categories %}<a href="{{ site.baseurl }}/categories/{{ cat }}">{{ cat | capitalize }}</a> / {% endfor %}{{ page.title }}</nav>
<article class="post-image">
  <h1>{{ page.title }}</h1>
  <div class="post-image-container">
    <img src="{{ page.image }}" alt="{{ page.alt }}">
    <div class="post-buttons">
      <button onclick="downloadImage('{{ page.image | absolute_url }}')">⬇️ Download</button>
      <button onclick="printHighRes('{{ page.image | absolute_url }}')">🖨️ Print</button>
      <a href="https://www.pinterest.com/pin/create/button/?url={{ page.url | absolute_url }}&media={{ page.image | absolute_url }}&description={{ page.alt }}" target="_blank">📌 Pin</a>
    </div>
  </div>
  {% if page.caption %}<p class="caption">{{ page.caption }}</p>{% endif %}
  <h3>People also loved</h3>
  <div class="related-grid">
    {% assign related = site.posts | where_exp:"p","p.categories contains page.categories[0]" | sample:4 %}
    {% for r in related %}
      {% if r.url != page.url %}
      <a href="{{ r.url | relative_url }}"><div class="related-card"><img src="{{ r.image }}" alt="{{ r.alt }}"></div></a>
      {% endif %}
    {% endfor %}
  </div>
</article>
<script>
function downloadImage(url){const a=document.createElement('a');a.href=url;a.download='image';document.body.appendChild(a);a.click();a.remove();}
function printHighRes(url){var w=window.open('','Print');w.document.write('<img src="'+url+'" style="width:100%">');w.document.write('<script>window.print();window.close();<\/script>');}
</script>
<style>
.post-image-container{text-align:center;margin:2em 0;}
.post-image-container img{max-width:100%; border-radius:15px;}
.post-buttons{display:flex; justify-content:center; gap:1em; margin:1em 0;}
.post-buttons button, .post-buttons a{padding:0.5em 1em; background:#ff6f61;color:#fff;border:none;border-radius:5px;text-decoration:none;cursor:pointer;}
.post-buttons button:hover,.post-buttons a:hover{background:#ff4a3a;}
.related-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1em; margin-top:1em;}
.related-card img{width:100%; border-radius:10px; border:1px solid #ddd;}
.breadcrumbs{font-size:0.8em; margin:0.5em 0; color:#555;}
</style>""",
    f"{css_folder}/override.css": """body { font-family: Arial, sans-serif; background: #f7f7f7; margin:0; padding:0;}
header { background:#ff6f61; color:#fff; padding:1em; text-align:center; }
header a { color:#fff; text-decoration:none; font-weight:bold; }
nav a { margin:0 0.5em; color:#fff; }
main { max-width:1200px; margin:2em auto; padding:0 1em; }
footer { text-align:center; padding:1em; font-size:0.8em; color:#555; background:#eee; margin-top:2em;}"""
}

# Create folders
os.makedirs(layouts_folder, exist_ok=True)
os.makedirs(css_folder, exist_ok=True)
os.makedirs(POSTS_DIR, exist_ok=True)

# Write layouts and CSS
for path, content in files_content.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created/Updated: {path}")

# --- FUNCTIONS FOR POSTS ---
def slugify(filename):
    name, _ = os.path.splitext(filename)
    return name.lower()

def title_from_filename(filename, main_keyword=""):
    name, _ = os.path.splitext(filename)
    return f"{main_keyword} Coloring Page {name}" if main_keyword else f"{name} Coloring Page"

def generate_post(image_path, categories, main_keyword=""):
    filename = os.path.basename(image_path)
    slug = slugify(filename)
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = title_from_filename(filename, main_keyword)
    alt_text = ", ".join([main_keyword] + DEFAULT_KEYWORDS) if main_keyword else ", ".join(DEFAULT_KEYWORDS)
    front_matter = {
        "layout": "post",
        "title": title,
        "date": date_str,
        "categories": categories,
        "image": "/" + image_path.replace("\\","/"),
        "alt": alt_text,
        "caption": CAPTION_DEFAULT,
        "image_only": True,
        "views": 0,
        "trending": False
    }
    post_file = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")
    with open(post_file, "w", encoding="utf-8") as f:
        f.write("---\n"+yaml.dump(front_matter, sort_keys=False)+"---\n")
    print(f"Created post: {post_file}")

# --- SCAN IMAGES AND GENERATE POSTS ---
for root, dirs, files in os.walk(IMAGES_ROOT):
    for file in files:
        if file.lower().endswith((".jpg",".jpeg",".png")):
            rel_path = os.path.relpath(os.path.join(root,file), start=".")
            category_path = os.path.relpath(root, IMAGES_ROOT).replace("\\","/").split("/")
            main_keyword = category_path[-1].capitalize() if category_path else ""
            generate_post(rel_path, category_path, main_keyword)

# --- AUTO GIT COMMIT & PUSH ---
subprocess.run(["git", "add", "_layouts/*", "css/*", "_posts/*"])
subprocess.run(["git", "commit", "-m", "Auto setup layouts, CSS, and generate posts"])
subprocess.run(["git", "push", GITHUB_REMOTE, "main"])
print("All done! Changes pushed to GitHub.")
# paste all code above → Ctrl+O → Enter → Ctrl+X

