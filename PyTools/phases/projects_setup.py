from phases.phase_base import Phase
from utils.html_utils import find_project_html_files, game_to_html_filename, create_html_file
from utils.image_utils import thumb_path
from utils.template_utils import header_template, footer_template,render_template
from config import TOP_LEVEL_DIR
from game_data import get_game_dataframe, is_empty
import os


video_iframe_template = """
<section class="game-showcase__video">
    <iframe class="game-showcase__iframe" allowfullscreen frameborder="0" height="550" width="980" src="{video_link}"></iframe>
</section>
"""

play_button_template = """
    <a class="page-section__button" href="{play_link}" target="_blank">Play Now</a>
"""

fallback_image_link_template = """
<section class="game-showcase__image-link">
    <a href="{play_link}">
        <img class="game-showcase__thumbnail image-effect" src="{img_path}"
             alt="{title} Thumbnail" />
    </a>
</section>
"""



PROJECT_HTML_BODY_TEMPLATE = """
<div class="container">
    <section class="game-header">
    <div class="project-container">
        <h1 class="large-fade-in game-header__title">{title}</h1>
        <div class="pane">
        <h3 class="large-fade-in game-header__tagline">Project game-header__tagline goes here.</h3>
        </div>
    </div>
    </section>
    
    
    <section class="page-section" id="game-showcase"></section>

    <section class="page-section">
    <div class="pane project-header">
        <h3>{title}</h3>
        <span>(YEAR)</span>
        <p><strong>Roles:</strong> TODO</p>
    </div>
    <div class="pane project-description">
        <p>Description goes here.</p>
    </div>
    </section>

    <section class="page-section documentation">
    <h2>Project Documentation</h2>
    <ul>
        <li><a href="#">Design Doc</a></li>
    </ul>
    </section>

    <section class="page-section">
    <h2>Screenshots</h2>
    <div class="screenshot-grid">
        <!-- Add <img> here -->
    </div>
    </section>

    <section class="page-section">
    <h2>Highlight of the Project</h2>
    <p class="pane">Highlight paragraph goes here.</p>
    </section>

    <section class="page-section">
    <h2>Team Credits</h2>
    <ul>
        <li>Teammate Name - Role</li>
    </ul>
    </section>

    <div class="random-projects">
    <div class="container">
        <h2>Explore More Games</h2>
        <div class="game-grid"></div>
        <div class="carousel-buttons">
        <button id="prev-btn">Previous</button>
        <button id="next-btn">Next</button>
        </div>
        <section class="page-section">
        <a href="../index.html" class="game-link">Back To Projects</a>
        </section>
    </div>
    </div>
</div>
"""

class projects_setup(Phase):
    def __init__(self):
        super().__init__(
            name="ProjectHtmlPhase",
            description="Scans the projects folder for valid project HTML files. If any are missing, it creates a new one using the default template."
        )
        self._created = []
        self.games = get_game_dataframe().to_dict("records")
        
        self.projects_dir = os.path.join(TOP_LEVEL_DIR, "projects")
        self.existing_files = set(find_project_html_files(self.projects_dir))
        
        # Register all paths into html_files
        for game in self.games:
            filename = game_to_html_filename(game)
            full_path = os.path.join(self.projects_dir, filename)
            self.html_files[game["filename"]] = full_path

    def enter(self):
        self.make_missing_project_html_files()
        self.open_htmls([game["filename"] for game in self.games])

        for game in self.games:
            if game["title"] != "Blades on Ice":
                continue  # skip all others for now

            label = game["filename"]
            soup = self.soups[label]

            self.insert_title(soup, game)
            self.insert_tagline(soup, game)
            self.insert_showcase(soup, game)  # just testing this

            self.write_html(label)


    def report(self) -> str:
        if not self._created:
            return f"[{self.name}] All project HTML files already exist."
        return f"[{self.name}] Created {len(self._created)} new HTML file(s):\n- " + "\n- ".join(self._created)
    
    def make_missing_project_html_files(self):
        for game in self.games:       
            filename = game_to_html_filename(game)
            full_path = os.path.join(self.projects_dir, filename)

            if filename in self.existing_files:
                print(f"[{self.name}] ✔ Found: {filename}")
                continue

            context = {
                "title": game["title"],
                "roles": game.get("roles", "TBD"),
            }

            created = create_html_file(
                output_path=full_path,
                templates=[header_template, PROJECT_HTML_BODY_TEMPLATE, footer_template],
                context=context
            )

            if created:
                self._created.append(filename)
                print(f"[{self.name}] ✨ Created: {filename}")
                
        if len(self._created) == 0 and len(self.games) > 0:
            print(f"[{self.name}] ✅ All {len(self.games)} project HTML files already exist.")
        elif len(self._created) < len(self.games):
            print(f"[{self.name}] ⚠ Only {len(self._created)} of {len(self.games)} project HTML files were newly created.")
        else:
            print(f"[{self.name}] ✨ Created all {len(self.games)} project HTML files.")

    def insert_text_value(self, soup, value: str, class_name: str, game: dict = None):
        if not value:
            return

        success = self.set_text_by_class(soup, class_name, value)
        if not success:
            print(
                f"[{self.name}] Warning: Could not find '.{class_name}' "
                f"for game '{game.get('title', '[Unknown Title]')}' "
                f"(file: '{game.get('filename', '[unknown]')}')"
            )



    # Stub functions for updating each section (to be implemented one-by-one)
    def insert_title(self, soup, game):
        self.insert_text_value(
            soup,
            value=game.get("title", ""),
            class_name="game-header__title",
            game=game,
        )

    def insert_tagline(self, soup, game):
        self.insert_text_value(
            soup,
            value=game.get("tagline", ""),
            class_name="game-header__tagline",
            game=game,
        )


    def insert_showcase(self, soup, game):

        video_link = game.get("video_link") or game.get("video")
        play_link = game.get("play_link")

        html_parts = []

        if not is_empty(video_link):
            html_parts.append(render_template(video_iframe_template, game))

        if is_empty(video_link) and not is_empty(play_link):
            html_parts.append(render_template(
                fallback_image_link_template, game, {"img_func": thumb_path}
            ))

        if not is_empty(play_link):
            html_parts.append(render_template(play_button_template, game))

        if html_parts:
            combined_html = "\n".join(html_parts)
            self.overwrite_html_by_id(soup, "game-showcase", combined_html)


    def insert_play_link(self, soup, game):
        if not game.get("play_link"): return
        link = soup.select_one(".game-link")
        if link:
            link["href"] = game["play_link"]

    def insert_project_header(self, soup, game):
        if not game.get("game-header__title"): return
        header = soup.select_one(".project-header h3")
        year = soup.select_one(".project-header span")
        roles = soup.select_one(".project-header p")
        if header:
            header.string = game["game-header__title"]
        if year and game.get("start_date"):
            year.string = game["start_date"][:4]
        if roles and game.get("roles"):
            roles.string = f"Roles: {game['roles']}"

    def insert_project_description(self, soup, game):
        if not game.get("description"): return
        desc = soup.select_one(".project-description p")
        if desc:
            desc.string = game["description"]

    def insert_documentation(self, soup, game):
        if not game.get("documentation"): return
        doc_list = soup.select_one(".documentation ul")
        if doc_list:
            doc_list.clear()
            for doc in game["documentation"]:
                li = soup.new_tag("li")
                a = soup.new_tag("a", href=doc.get("url", "#"))
                a.string = doc.get("name", "Doc")
                li.append(a)
                doc_list.append(li)

    def insert_screenshots(self, soup, game):
        pass


    def insert_highlight(self, soup, game):
        if not game.get("highlight"): return
        p = soup.select_one(".page-section p.pane")
        if p:
            p.string = game["highlight"]

    def insert_team_credits(self, soup, game):
        if not game.get("team"): return
        ul = soup.select_one(".page-section ul")
        if ul:
            ul.clear()
            for entry in game["team"]:
                li = soup.new_tag("li")
                li.string = entry
                ul.append(li)