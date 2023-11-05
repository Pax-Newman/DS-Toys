from pathlib import Path

import typer
import click
from questionary import select

from .game import Game
from .wordbank import WordBank, from_txt

app = typer.Typer()


@app.command()
def main(
    wordbank: Path = typer.Option("wordlist.txt", help="Path to wordbank file."),
    num_choices: int = typer.Option(
        default=6, help="Number of choices to give each round."
    ),
    model: str = typer.Option(
        "all-MiniLM-L6-v2", help="Model to use for word embeddings."
    ),
):
    # Load words
    if wordbank.suffix == ".txt":
        bank = from_txt(str(wordbank.absolute()), model)
    elif wordbank.suffix == ".db":
        bank = WordBank(str(wordbank.absolute()), model)
    else:
        raise ValueError("Wordbank must be a .txt or .db file.")


    # Initialize game
    game = Game(bank, num_choices)


    # click.clear()
    while True:
        # Start new game
        game.new_game()

        # Game loop
        while True:
            view_str = f"""
Start: {game.start_word} - Current: {game.current_word} - Target: {game.target_word}
Which word vector would you like to travel to next?
"""
            print(game.word_path)

            options = [f"{option.word} - {option.distance}" for option in game.options]
            choice = select(view_str, options).ask()

            choice_idx = options.index(choice)

            win = game.choose(choice_idx)
            if win:
                break

            click.clear()

        print(
            f"Congratulations! You reached {game.target_word} in {len(game.word_path)} steps."
        )
        print(f"Your total distance was: {game.total_distance}")
        print(f"Your path was: {game.word_path}")

        replay = select("Would you like to play again", ["Yes", "No"]).ask()

        if replay == "No":
            break

        click.clear()

