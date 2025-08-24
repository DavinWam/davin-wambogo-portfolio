from utils.image_utils import thumb_path

# === HTML Templates ===
header_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1024">
    <title>{title}</title>
    <link rel="stylesheet" href="../css/style.css">
    <script src="../loadHeader.js"></script>
</head>
<body>
    <header id="header-container"></header>
"""

footer_template = """
    <footer id="footer-container"></footer>
    <script src="RandomGame.js"></script>
    <script src="Modal.js"></script>
</body>
</html>
"""

def render_template(template_str, game_data, extra_data=None):
    context = {
        "title": game_data["title"],
        "roles": game_data.get("roles", ""),
        "filename": game_data["filename"],
        "alt": game_data["title"],
        "style": "",
    }

    img_funcs = _validate_and_get_img_funcs(template_str, extra_data)

    result = template_str
    for func in img_funcs:
        replacement = func(game_data["title"])
        result = result.replace("{img_path}", replacement, 1)

    if extra_data:
        context.update(extra_data)

    return result.format(**context)

def render_game(game: dict, template: str, extra_data: dict = None) -> str:
    return render_template(template, game, extra_data)

def render_games(
    games: list[dict],
    template: str,
    extra_data: dict = None,
    join_with: str = "\n\n",
    add_at_start: bool = False,
    add_at_end: bool = False
) -> str:
    blocks = [render_template(template, game, extra_data) for game in games]
    result = join_with.join(blocks)

    if add_at_start:
        result = join_with + result
    if add_at_end:
        result = result + join_with

    return result


def _extract_img_placeholders(template_str):
    return template_str.count("{img_path}")

def _get_img_funcs(extra_data):
    if not extra_data:
        return None
    if "img_funcs" in extra_data:
        return extra_data["img_funcs"]
    if "img_func" in extra_data:
        func = extra_data["img_func"]
        return [func] if callable(func) else func
    return None

def _validate_and_get_img_funcs(template_str, extra_data):
    num_placeholders = _extract_img_placeholders(template_str)
    img_funcs = _get_img_funcs(extra_data)

    if not img_funcs:
        raise ValueError("No image function(s) provided to render_template.")

    if len(img_funcs) != num_placeholders:
        raise ValueError(
            f"Mismatch: template has {num_placeholders} '{{img_path}}' placeholder(s), "
            f"but {len(img_funcs)} image function(s) provided."
        )

    return img_funcs