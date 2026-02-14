from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from datetime import datetime
import shutil

TEMPLATES_DIR = Path("templates")
OUT_DIR = Path("public")
STATIC_DIR = Path("static")

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

# helper for templates that might use a `static` URL
env.globals["static"] = lambda p: f"/static/{p.lstrip('/')}"
env.globals["year"] = datetime.now().year

# create output dir
OUT_DIR.mkdir(parents=True, exist_ok=True)

# copy static/ -> public/static (if static exists)
if STATIC_DIR.exists() and STATIC_DIR.is_dir():
    dest_static = OUT_DIR / "static"
    if dest_static.exists():
        shutil.rmtree(dest_static)
    shutil.copytree(STATIC_DIR, dest_static)
    print(f"Copied {STATIC_DIR} -> {dest_static}")
else:
    print("No static/ directory found — skipping static copy")

# render templates to public/
for tpl_path in TEMPLATES_DIR.rglob("*.html"):
    rel = tpl_path.relative_to(TEMPLATES_DIR).as_posix()
    # skip partials if needed
    if rel.startswith("_"):
        continue
    rendered = env.get_template(rel).render()
    out_file = OUT_DIR / rel
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(rendered, encoding="utf-8")

print(f"Rendered templates to {OUT_DIR}/")