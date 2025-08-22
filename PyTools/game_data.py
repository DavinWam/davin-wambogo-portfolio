import pandas as pd
import pandas as pd
games = [
    {
        "title": "ENYA'S JOURNEY",
        "roles": "Game Design, Programming, UI, Level Design, Art & Animation",
        "filename": "enyas_journey",
        "thumbnail": "thumbnail_enyas_journey.jpg",
        "featured": True,
        "visibility": "public",
        "dates": "Oct 2023 – Dec 2023",
        "start_date": "2023-10-01",
        "end_date": "2023-12-31"
    },
    {
        "title": "BABY STEPS",
        "roles": "Game Designer, Games Programmer, Graphics Programmer",
        "filename": "baby_steps",
        "thumbnail": "thumbnail_baby_steps.jpg",
        "visibility": "public",
        "dates": "Apr 2024 – May 2024",
        "start_date": "2024-04-01",
        "end_date": "2024-05-31"
    },
    {
        "title": "TAXES AND TENACITY",
        "roles": "Game Design, Programming, Art & Animation",
        "filename": "taxes_and_tenactity",
        "thumbnail": "thumbnail_taxes_and_tenactity.png",
        "visibility": "public",
        "dates": "Oct 2023 – Oct 2023",
        "start_date": "2023-10-01",
        "end_date": "2023-10-31"
    },
    {
        "title": "SILENT CODES",
        "roles": "Game Design, Programming, Technical Art",
        "filename": "silent_codes",
        "thumbnail": "thumbnail_silent_codes.jpg",
        "visibility": "public",
        "dates": "Nov 2023 – Dec 2023",
        "start_date": "2023-11-01",
        "end_date": "2023-12-31"
    },
    {
        "title": "GOT STEAM, PUNK?",
        "roles": "Game Design, Level Design, Art & Animation",
        "filename": "got_steam_punk",
        "thumbnail": "thumbnail_got_steam_punk.jpg",
        "visibility": "public",
        "dates": "Sep 2021 – Nov 2021",
        "start_date": "2021-09-01",
        "end_date": "2021-11-30"
    },
    {
        "title": "LAB BAT",
        "roles": "Game Design, UI, Level Design, Art & Animation",
        "filename": "lab_bat",
        "thumbnail": "thumbnail_lab_bat.PNG",
        "visibility": "public",
        "dates": "Mar 2021 – Mar 2021",
        "start_date": "2021-03-01",
        "end_date": "2021-03-31"
    },
    {
        "title": "SCALE THE BEAST",
        "roles": "Programmer, Level Designer",
        "filename": "scale_the_beast",
        "thumbnail": "thumbnail_scale_the_beast.png",
        "visibility": "public",
        "dates": "Oct 2024 – Oct 2024",
        "start_date": "2024-10-01",
        "end_date": "2024-10-31"
    },
    {
        "title": "SPACE BLITZ",
        "roles": "Game Design, Level Design",
        "filename": "space_game",
        "thumbnail": "thumbnail_space_game.png",
        "visibility": "private",
        "dates": None,
        "start_date": None,
        "end_date": None
    },
    {
        "title": "PENROSE",
        "roles": "Level Design, Art",
        "filename": "penrose",
        "thumbnail": "thumbnail_penrose.PNG",
        "visibility": "private",
        "dates": None,
        "start_date": None,
        "end_date": None
    },
    {
        "title": "BLADES ON ICE",
        "roles": "Game Design, Programming, Animation",
        "filename": "blades_on_ice",
        "thumbnail": "thumbnail_blades_on_ice.jpg",
        "visibility": "public",
        "dates": "Oct 2024 – May 2025",
        "start_date": "2024-10-01",
        "end_date": "2025-05-31"
    },
    {
        "title": "SYNTH DOG",
        "roles": "Game Design & Audio Engineering",
        "filename": "synth_dog",
        "thumbnail": "thumbnail_synth_dog.png",
        "visibility": "hidden",
        "dates": "Nov 2024 – Dec 2024",
        "start_date": "2024-11-01",
        "end_date": "2024-12-31"
    }
]

# === Globals ===
_game_df = None
_featured_game = None

# === Public API ===

def setup_game_dataframe() -> pd.DataFrame:
    """Initializes the main game DataFrame with processed fields."""
    global _game_df
    df = pd.DataFrame(get_games())

    # Warn if 'roles' field is missing or malformed
    problems = df[df["roles"].isnull() | ~df["roles"].apply(lambda x: isinstance(x, str))]
    if not problems.empty:
        print("[Warning] Games with missing or non-string 'roles':")
        print(problems[["title", "roles"]])

    # Create a split roles list column
    df["roles_list"] = df.apply(split_roles, axis=1)

    print("[Info] Sample 'roles_list' column:")
    print(df[["title", "roles_list"]].head())

    _game_df = df
    return _game_df

def get_game_dataframe() -> pd.DataFrame:
    """Returns the cached or newly created DataFrame of games."""
    global _game_df
    if _game_df is None:
        _game_df = setup_game_dataframe()
    return _game_df

def get_games() -> list[dict]:
    """Returns the raw list of game dictionaries."""
    # Replace this with your static or loaded list
    return games

def get_games_as_records() -> list[dict]:
    """Returns the processed DataFrame as a list of dicts."""
    return get_game_dataframe().to_dict("records")

def get_featured_game(df: pd.DataFrame = None) -> dict:
    """Returns the featured game or defaults to the first."""
    global _featured_game
    df = df if df is not None else get_game_dataframe()
    return _featured_game or (df.iloc[0].to_dict() if not df.empty else None)

def set_featured_game(game: dict):
    """Sets a manually chosen featured game."""
    global _featured_game
    _featured_game = game

def get_non_featured_games(df: pd.DataFrame = None) -> pd.DataFrame:
    """Returns games that are not marked as featured."""
    df = df if df is not None else get_game_dataframe()
    return df[df["featured"] != True]

def get_non_featured_records(df: pd.DataFrame = None) -> list[dict]:
    """Returns non-featured games as a list of dicts."""
    return get_non_featured_games(df).to_dict("records")

def get_unique(df_or_list, column: str) -> list:
    """Returns a sorted list of unique values in a column (supports DataFrame or list-of-dict input)."""
    df = pd.DataFrame(df_or_list)

    if column not in df.columns:
        return []

    series = df[column].dropna()

    if series.apply(lambda x: isinstance(x, list)).any():
        series = series.explode()
    else:
        series = series.astype(str).str.split(",").explode()

    return (
        series.dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

# === Utilities ===

def split_roles(game_row) -> list:
    """Splits the 'roles' string into a list. Compatible with dict or Series input."""
    if isinstance(game_row, dict):
        roles = game_row.get("roles", "")
    else:  # pandas Series
        roles = game_row["roles"] if "roles" in game_row else ""
    return [r.strip() for r in roles.split(",") if r.strip()]