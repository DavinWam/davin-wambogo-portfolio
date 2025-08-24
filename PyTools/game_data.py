import json
import pandas as pd
from config import GAMES_JSON_PATH, ROLES_JSON_PATH

# === Globals ===
_game_df = None
_featured_game = None


def load_games():
    with open(GAMES_JSON_PATH, encoding="utf-8") as f:
        return json.load(f)

# === Public API ===

def setup_game_dataframe() -> pd.DataFrame:
    """Initializes the main game DataFrame with processed fields."""
    global _game_df
    #print(get_games())

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

    write_roles_json()
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
    return load_games()

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

def write_roles_json():
    df = get_game_dataframe()
    all_roles = sorted(set(role for roles in df["roles_list"] for role in roles))

    with open(ROLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_roles, f, indent=2)

    print(f"[Info] Wrote {len(all_roles)} unique roles to {ROLES_JSON_PATH}")