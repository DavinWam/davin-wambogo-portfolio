from utils.image_utils import thumb_path
from game_data import format_teammate_entry,  get_teammates, get_contributions

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
        "title": game_data.get("title", ""),
        "roles": game_data.get("roles", ""),
        "filename": game_data.get("filename", ""),
        "alt": game_data.get("title", ""),
        "style": "",
        "dates": game_data.get("dates", ""),
        "year": (game_data.get("start_date", "")[:4] if game_data.get("start_date") else ""),
        "tagline": game_data.get("tagline", ""),
        "highlight": game_data.get("highlight", ""),
        "play_link": game_data.get("play_link", ""),
        "video_link": game_data.get("video_link") or game_data.get("video", ""),
    }

    # === Handle full teammate list formatting ===
    if "{teammates}" in template_str:
        teammates = get_teammates(game_data)
        formatted = [format_teammate_entry(t) for t in teammates if format_teammate_entry(t)]
        context["teammates"] = ", ".join(formatted)

    if extra_data:
        context.update(extra_data)

        if "teammate_index" in extra_data:
            index = extra_data["teammate_index"]
            teammates = get_teammates(game_data)
            if isinstance(index, int) and 0 <= index < len(teammates):
                teammate = teammates[index]
                context["teammate_name"] = teammate.get("teammate_name", "")
                context["teammate_role"] = teammate.get("role", "")
            else:
                context["teammate_name"] = ""
                context["teammate_role"] = ""

        if "contributions_index" in extra_data:
            index = extra_data["contributions_index"]
            contributions = get_contributions(game_data)
            if isinstance(index, int) and 0 <= index < len(contributions):
                context["contribution"] = contributions[index]
            else:
                context["contribution"] = ""    

        if "documentation_index" in extra_data:
            index = extra_data["documentation_index"]
            docs = game_data.get("documentation", [])
            if isinstance(index, int) and 0 <= index < len(docs):
                doc = docs[index]
                context["link"] = doc.get("link", "")
                context["link_name"] = doc.get("name", "")
            else:
                context["link"] = ""
                context["link_name"] = ""

    img_funcs = _validate_and_get_img_funcs(template_str, extra_data)

    result = template_str
    for func in img_funcs:
        replacement = func(game_data["title"])
        result = result.replace("{img_path}", replacement, 1)


    return result.format(**context)

def render_template_list(
    data_list: list,
    template: str,
    game_data: dict = None,
    join_with: str = "",
    wrap_tag: str = None,
    index_names: list[str] = None
) -> str:
    game_data = game_data or {}
    blocks = []

    for i, item in enumerate(data_list):
        context = {}

        # Add all index names to the context
        if index_names:
            for name in index_names:
                context[name] = i

        rendered = render_template(template, game_data, extra_data=context)
        if wrap_tag:
            rendered = f"<{wrap_tag}>{rendered}</{wrap_tag}>"
        blocks.append(rendered)

    return join_with.join(blocks)




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
        if _extract_img_placeholders(template_str) > 0:
            raise ValueError("No image function(s) provided to render_template.")
        return []


    if len(img_funcs) != num_placeholders:
        raise ValueError(
            f"Mismatch: template has {num_placeholders} '{{img_path}}' placeholder(s), "
            f"but {len(img_funcs)} image function(s) provided."
        )

    return img_funcs