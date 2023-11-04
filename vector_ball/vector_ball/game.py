from . import word_tree
from random import choice


class Game:
    def __init__(self, tree: word_tree.WordTree, num_choices: int) -> None:
        self.tree = tree
        self.num_choices = num_choices

        # Game State
        self.start_word = ""
        self.current_word = ""
        self.target_word = ""
        self.target_embedding = None
        self.dist_to_target = 0.0
        self.total_distance = 0.0
        self.word_path = []
        self.options = []

    def new_game(self) -> None:
        """Start a new game."""
        # Reset game state
        self.total_distance = 0.0
        self.word_path = []
        self.options = []

        # Randomly set new start and target
        while (new_start := choice(self.tree.words)) in [
            self.start_word,
            self.target_word,
        ]:
            pass

        while (new_target := choice(self.tree.words)) in [
            new_start,
            self.start_word,
            self.target_word,
        ]:
            pass

        self.start_word = new_start
        self.target_word = new_target

        self.current_word = self.start_word

        self.word_path = [new_start]

        # Fetch options for the current word
        self.options = self.tree.query(self.current_word, k=self.num_choices)

    def choose(self, option_idx: int) -> bool:
        """
        Go to an option in the current word's options.
        Returns True if the target word was reached, False otherwise.
        """

        # Update game state given the choice
        choice = self.options[option_idx]
        self.total_distance += choice.distance
        self.word_path.append(choice.word)

        if choice.word == self.target_word:
            return True

        # Fetch new options
        options = self.tree.query(self.current_word, k=self.num_choices * 2)

        # Ensure the new options don't include the previous choice
        self.options = [
            option for option in options if option.word not in self.word_path
        ][: self.num_choices]

        self.current_word = choice.word

        return False
