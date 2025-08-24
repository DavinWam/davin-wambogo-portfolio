from phases.phase_base import Phase
from utils.html_utils import find_project_html_files, game_to_html_filename, create_html_file
from utils.template_utils import header_template, footer_template
from config import TOP_LEVEL_DIR
from game_data import get_game_dataframe
import os

PROJECT_HTML_BODY_TEMPLATE = """
<div class="container">
    <section class="showcase">
    <div class="project-container">
        <h1 class="large-fade-in title">{title}</h1>
        <div class="pane">
        <h3 class="large-fade-in">Project tagline goes here.</h3>
        </div>
    </div>
    </section>

    <section class="project-section">
    <a href="#" target="_blank" class="game-link">Play Now</a>
    </section>

    <section class="project-section">
    <div class="pane project-header">
        <h3>{title}</h3>
        <span>(YEAR)</span>
        <p><strong>Roles:</strong> TODO</p>
    </div>
    <div class="pane project-description">
        <p>Description goes here.</p>
    </div>
    </section>

    <section class="project-section documentation">
    <h2>Project Documentation</h2>
    <ul>
        <li><a href="#">Design Doc</a></li>
    </ul>
    </section>

    <section class="project-section">
    <h2>Screenshots</h2>
    <div class="screenshot-grid">
        <!-- Add <img> here -->
    </div>
    </section>

    <section class="project-section">
    <h2>Highlight of the Project</h2>
    <p class="pane">Highlight paragraph goes here.</p>
    </section>

    <section class="project-section">
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
        <section class="project-section">
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
            label = game["filename"]
            soup = self.soups[label]

            self.insert_title(soup, game)
            # Add additional insert_ functions here as needed

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


    # Stub functions for updating each section (to be implemented one-by-one)
    def insert_title(self, soup, game):

        title_tag = soup.find("h1", class_="large-fade-in title")
        if title_tag:
            title_tag.string = game["title"]
    def insert_tagline(soup, game):
        pass
    def insert_video(soup, game):
        pass
    def insert_play_link(soup, game):
        pass
    def insert_project_header(soup, game):
        pass
    def insert_project_description(soup, game):
        pass
    def insert_documentation(soup, game):
        pass
    def insert_screenshots(soup, game):
        pass
    def insert_highlight(soup, game):
        pass
    def insert_team_credits(soup, game):
        pass