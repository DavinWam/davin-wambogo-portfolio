import os

def find_project_html_files(projects_dir: str) -> list[str]:
    """Returns a list of all HTML filenames in the projects folder."""
    return sorted([
        fname for fname in os.listdir(projects_dir)
        if fname.endswith(".html")
    ])

def game_to_html_filename(game: dict) -> str:
    return f"{game['filename']}.html"

def create_html_file(
    output_path: str,
    templates: list[str],
    context: dict
) -> bool:
    """Safely creates an HTML file by combining templates with a context dict.
    Returns True if file was created, False if it already exists.
    """
    import os

    if os.path.exists(output_path):
        return False  # Do not overwrite

    try:
        with open(output_path, "x", encoding="utf-8") as f:
            for template in templates:
                f.write(template.format(**context))
        return True
    except FileExistsError:
        return False