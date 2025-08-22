import os
from bs4 import BeautifulSoup
from phases.phase_base import Phase
from game_data import get_game_dataframe, get_featured_game, get_non_featured_games
from utils.image_utils import thumb_path, banner_path
from utils.template_utils import render_game, render_games

class game_carousel_setup(Phase):
    def __init__(self):
        super().__init__("GameCarouselSetup")
        self.html_files = {"index": os.path.join("..", "docs", "index.html")}
        self.games = get_game_dataframe()
        self.article_template = (
            '<article class="game">\n'
            '  <h3{style}><span class="title">{title}</span> {roles}</h3>\n'
            '  <a href="projects/{filename}.html">'
            '<img class="image-effect" src="{img_path}" alt="{title} Thumbnail"></a>\n'
            '</article>'
        )
        self.featured_template = (
            '  <h3{style}><span class="title">{title}</span> {roles}</h3>\n'
            '  <a href="projects/{filename}.html">'
            '<img class="image-effect" src="{img_path}" alt="{title} Thumbnail"></a>\n'
        )

    def enter(self):
        print(f"[{self.name}] Injecting carousel into index.html")

        soup = self.open_htmls(["index"])[0]

        featured_game = get_featured_game(self.games)
        games_to_show = get_non_featured_games().sort_values("end_date", ascending=False).to_dict("records")




        carousel_html = render_games(games_to_show, self.article_template, {"img_func": thumb_path})
        featured_html = render_game(featured_game, self.featured_template, {
            "img_func": banner_path,
            "style": ' style="width:40%;"'
        })

        self.overwrite_html_by_id(soup, "game-carousel", carousel_html)
        self.overwrite_html_by_id(soup, "featured-game", featured_html)

        self.write_html("index")
        print(f"[{self.name}] Injection complete.")
