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

    # Preserve line breaks and blank lines in the poem
    poem_html = html.escape(poem)
    paragraphs = poem_html.split("\n\n")

    poem_paragraphs = []

    for paragraph in paragraphs:
        paragraph = paragraph.replace("\n", "<br>\n")
        poem_paragraphs.append(f"                <p>{paragraph}</p>")

    poem_content = "\n".join(poem_paragraphs)

    date_section = (
        f'            <div class="poem-date">{date_html}</div>'
        if date
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../style.css">
    <title>{title_html} — H.S.</title>
</head>

<body>
    <main class="poem-page">

        <nav class="top-nav">
            <a href="../index.html">← All Poems</a>
        </nav>

        <header class="poem-header">
            <div class="small-mark">H.S.</div>

            <h1>{title_html}</h1>

            {date_section}
        </header>

        <article class="poem">
{poem_content}
        </article>

        <footer>
            <a href="../index.html">Return to the collection</a>
        </footer>

    </main>
</body>
</html>
"""


def make_poems_index(poems):
    entries = []

    for title, date, path in poems:
        title_html = html.escape(title)
        date_html = html.escape(date)

        date_section = (
            f'                <div class="poem-date">{date_html}</div>'
            if date
            else ""
        )

        entries.append(
            f"""            <li>
                <a class="poem-link" href="poems/{path.stem}.html">
                    <span class="poem-title">{title_html}</span>
                    {date_section}
                </a>
            </li>"""
        )

    poem_list = "\n".join(entries)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>H.S. — Poetry</title>
</head>

<body>
    <main class="home-page">

        <header class="site-header">
            <div class="ornament">✦</div>

            <div class="initials">H.S.</div>

            <div class="subtitle">Poetry &amp; Writing</div>

            <div class="header-rule"></div>
        </header>

        <section class="collection">
            <div class="section-label">The Collection</div>

            <h1>Poems</h1>

            <ul>
{poem_list}
            </ul>
        </section>

        <footer>
            <div class="footer-mark">H.S.</div>
        </footer>

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
