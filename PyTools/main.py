from phases.phase_base import Phase
from phases.game_carousel_setup import game_carousel_setup
import pandas as pd
from game_data import setup_game_dataframe


def run_phases(phases):
    for phase in phases:
        print(f">> Entering: {phase.name}")
        phase.enter()
        print(f"<< Exiting: {phase.name}")
        phase.exit()

if __name__ == "__main__":
    setup_game_dataframe()
    run_phases([
        game_carousel_setup()
    ])
