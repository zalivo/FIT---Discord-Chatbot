from random import choice

import rhyme
from penalty import Penalty
from startingletter import StartingLetter


class Competition:
    """
    This class is for the competition
    It stores the number of rounds, the current round, the possible games, the games, and the penalty points
    """
    def __init__(self, num_rounds=3):
        print(num_rounds)
        self.num_rounds = num_rounds  # Number of rounds
        self.game_round = 0  # Current round
        self.possible_games = [rhyme.Rhyme, StartingLetter]  # List of possible games ADD NEW GAMES HERE
        self.penalty = Penalty()  # We are using the penalty class to store the penalty points of the players

        # generate games here, and shuffle them such that they don't repeat right after each other
        self.games = [(choice(self.possible_games)(self)) for _ in range(self.num_rounds)]
        # TODO shuffle them such that they don't repeat right after each other

    async def start_a_game(self, message):
        """
        This function is called when the game is started by the user
        or whenever a minigame is over (the minigame calls this function when it is over)
        :param message:
        :return:
        """
        print("Starting a new game")
        self.game_round += 1
        if self.game_round == self.num_rounds + 1:  # If the game is over
            await message.channel.send("\nThe game is over! 🏁") # TODO: add a gif and better leaderboard
            # print the scores in order of highest to lowest
            sorted_penalty = sorted(self.penalty.penalty_points.items(), key=lambda x: x[1], reverse=True)
            scores = "The scores are:\n"
            for player, points in sorted_penalty:
                scores += f"{player} has {points} points\n"
            await message.channel.send(scores)
        else:
            await message.channel.send(f"\nTime for round {self.game_round}!" + "\n" + self.game().message_on_start())

    async def play(self, message):
        """
        This gets called each time the user sends a message, while the game is running
        :param message:
        :return:
        """
        print("Playing a game")
        # TODO: Add curses, like full capslock or end the sentence with "your honour" or "I object" or "I rest my case"
        # TODO: Make people unable to respond consecutively
        message.content = message.content.lower()
        # TODO: process the message
        await self.game().play(message)

    def game(self):
        return self.games[self.game_round - 1]
