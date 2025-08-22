import pandas as pd

total_games = len(games)

_featured_game = None

def get_games():
    return games

def set_featured_game(game):
    global _featured_game
    _featured_game = game

def get_featured_game(games):
    return _featured_game or (games[0] if games else None)

def get_non_featured_games(games):
    featured = get_featured_game(games)
    return [g for g in games if g != featured]

def split_roles(game):
    """Return a list of individual roles for a given game."""
    roles = game.get("roles", "")
    return [r.strip() for r in roles.split(",") if r.strip()]
def get_unique_roles(games):
    df = pd.DataFrame(games)
    if "roles" not in df.columns:
        return []

    # Split comma-separated roles and explode into rows
    roles_series = (
        df["roles"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .drop_duplicates()
        .sort_values()
    )
    return roles_series.tolist()


games = [
    {
        "title": "ENYA'S JOURNEY",
        "roles": "Game Design, Programming, UI, Level Design, Art & Animation",
        "filename": "enyas_journey",
        "thumbnail": "thumbnail_enyas_journey.jpg",
        "featured": True,
        "visibility": "public",
        "dates": "Oct 2023 – Dec 2023"
    },
    {
        "title": "BABY STEPS",
        "roles": "Game Designer, Games Programmer, Graphics Programmer",
        "filename": "baby_steps",
        "thumbnail": "thumbnail_baby_steps.jpg",
        "visibility": "public",
        "dates": "Apr 2024 – May 2024"
    },
    {
        "title": "TAXES AND TENACITY",
        "roles": "Game Design, Programming, Art & Animation",
        "filename": "taxes_and_tenactity",
        "thumbnail": "thumbnail_taxes_and_tenactity.png",
        "visibility": "public",
        "dates": "Oct 2023 – Oct 2023"
    },
    {
        "title": "SILENT CODES",
        "roles": "Game Design, Programming, Technical Art",
        "filename": "silent_codes",
        "thumbnail": "thumbnail_silent_codes.jpg",
        "visibility": "public",
        "dates": "Nov 2023 – Dec 2023"
    },
    {
        "title": "GOT STEAM, PUNK?",
        "roles": "Game Design, Level Design, Art & Animation",
        "filename": "got_steam_punk",
        "thumbnail": "thumbnail_got_steam_punk.jpg",
        "visibility": "public",
        "dates": "Sep 2021 – Nov 2021"
    },
    {
        "title": "LAB BAT",
        "roles": "Game Design, UI, Level Design, Art & Animation",
        "filename": "lab_bat",
        "thumbnail": "thumbnail_lab_bat.PNG",
        "visibility": "public",
        "dates": "Mar 2021 – Mar 2021"
    },
    {
        "title": "SCALE THE BEAST",
        "roles": "Programmer, Level Designer",
        "filename": "scale_the_beast",
        "thumbnail": "thumbnail_scale_the_beast.png",
        "visibility": "public",
        "dates": "Oct 2024 – Oct 2024"
    },
    {
        "title": "SPACE BLITZ",
        "roles": "Game Design, Level Design",
        "filename": "space_game",
        "thumbnail": "thumbnail_space_game.png",
        "visibility": "private",
        "dates": None
    },
    {
        "title": "PENROSE",
        "roles": "Level Design, Art",
        "filename": "penrose",
        "thumbnail": "thumbnail_penrose.PNG",
        "visibility": "private",
        "dates": None
    },
    {
        "title": "BLADES ON ICE",
        "roles": "Game Design, Programming, Animation",
        "filename": "blades_on_ice",
        "thumbnail": "thumbnail_blades_on_ice.jpg",
        "visibility": "public",
        "dates": "Oct 2024 – May 2025"
    },
    {
        "title": "SYNTH DOG",
        "roles": "Game Design & Audio Engineering",
        "filename": "synth_dog",
        "thumbnail": "thumbnail_synth_dog.png",
        "visibility": "hidden",
        "dates": "Nov 2024 – Dec 2024"
    }
]
