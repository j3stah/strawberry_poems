from pathlib import Path
import html

POEMS_DIR = Path("poems")


def parse_poem(path):
    text = path.read_text(encoding="utf-8").strip()

    parts = text.split("\n", 1)

    title = parts[0].strip()
    poem = parts[1].strip() if len(parts) > 1 else ""

    return title, poem


def make_poem_page(title, poem):
    title_html = html.escape(title)

    poem_html = html.escape(poem)
    poem_html = poem_html.replace("\n\n", "</p><p>")
    poem_html = poem_html.replace("\n", "<br>\n")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_html}</title>
</head>
<body>
    <main>
        <a href="../index.html">← Back to poems</a>

        <h1>{title_html}</h1>

        <div class="poem">
            <p>{poem_html}</p>
        </div>
    </main>
</body>
</html>
"""


def make_poems_index(poems):
    links = []

    for title, path in poems:
        links.append(
            f'        <li><a href="poems/{path.stem}.html">{html.escape(title)}</a></li>'
        )

    poem_list = "\n".join(links)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Poems</title>
</head>
<body>
    <main>
        <h1>My Poems</h1>

        <ul>
{poem_list}
        </ul>
    </main>
</body>
</html>
"""


poems = []

for poem_file in POEMS_DIR.glob("*.txt"):
    title, poem = parse_poem(poem_file)

    output_file = POEMS_DIR / f"{poem_file.stem}.html"

    output_file.write_text(
        make_poem_page(title, poem),
        encoding="utf-8"
    )

    poems.append((title, poem_file))

    print(f"Generated {output_file}")


# Sort poems alphabetically by title
poems.sort(key=lambda poem: poem[0].lower())

Path("index.html").write_text(
    make_poems_index(poems),
    encoding="utf-8"
)

print("Generated index.html")
