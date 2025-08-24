from phases.phase_base import Phase
from phases.game_carousel_setup import game_carousel_setup
from phases.projects_setup import projects_setup
import pandas as pd
from game_data import setup_game_dataframe

def prompt_run_phase(phase: Phase) -> bool:
    print(f"\nPHASE: {phase.name}")
    if phase.description:
        print(f"  Description: {phase.description}")
    report = phase.report()
    if report:
        print(f"  Report: {report}")
    response = input("  Run this phase? [y/N]: ").strip().lower()
    return response == "y"


def run_phases(phases):
    for phase in phases:
        if prompt_run_phase(phase):
            print(f">> Entering: {phase.name}")
            phase.enter()
            print(f"<< Exiting: {phase.name}")
            phase.exit()
        else:
            print(f"-- Skipped: {phase.name}")

if __name__ == "__main__":
    setup_game_dataframe()
    run_phases([
        game_carousel_setup(),
        projects_setup()
    ])
