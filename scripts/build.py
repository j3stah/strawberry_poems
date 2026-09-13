from pathlib import Path
from datetime import datetime
import html

POEMS_DIR = Path("poems")


def parse_poem(path):
    text = path.read_text(encoding="utf-8").strip()

    lines = text.splitlines()

    title = lines[0].strip()

    date = ""
    poem_start = 1

    if len(lines) > 1 and lines[1].strip():
        date = lines[1].strip()
        poem_start = 2

    # Skip blank lines between metadata and poem
    while poem_start < len(lines) and not lines[poem_start].strip():
        poem_start += 1

    poem = "\n".join(lines[poem_start:]).strip()

    return title, date, poem


def parse_date(date):
    try:
        return datetime.strptime(date, "%B %d, %Y")
    except ValueError:
        return datetime.min


def make_poem_page(title, date, poem):
    title_html = html.escape(title)
    date_html = html.escape(date)

    poem_html = html.escape(poem)
    poem_html = poem_html.replace("\n\n", "</p><p>")
    poem_html = poem_html.replace("\n", "<br>\n")

    date_section = f"<p><em>{date_html}</em></p>" if date else ""

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

        {date_section}

        <div class="poem">
            <p>{poem_html}</p>
        </div>
    </main>
</body>
</html>
"""


def make_poems_index(poems):
    links = []

    for title, date, path in poems:
        title_html = html.escape(title)
        date_html = html.escape(date)

        date_section = f" <em>{date_html}</em>" if date else ""

        links.append(
            f'        <li><a href="poems/{path.stem}.html">{title_html}</a>{date_section}</li>'
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
    title, date, poem = parse_poem(poem_file)

    output_file = POEMS_DIR / f"{poem_file.stem}.html"

    output_file.write_text(
        make_poem_page(title, date, poem),
        encoding="utf-8"
    )

    poems.append((title, date, poem_file))

    print(f"Generated {output_file}")


# Newest poems first
poems.sort(key=lambda poem: parse_date(poem[1]), reverse=True)

Path("index.html").write_text(
    make_poems_index(poems),
    encoding="utf-8"
)

print("Generated index.html")
