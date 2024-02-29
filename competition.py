import time

import nltk
from random import randint, choice
from penalty import Penalty

import rhyme
from startingletter import StartingLetter


class Competition:
    def __init__(self, num_rounds=3):
        print(num_rounds)
        self.num_rounds = num_rounds  # Number of rounds
        self.game_round = 0  # Current round
        self.possible_games = [rhyme.Rhyme, StartingLetter]  # List of possible games
        self.penalty = Penalty()  # We are using the penalty class to store the penalty points of the players

        # generate games here, and shuffle them such that they don't repeat right after each other
        self.games = [(choice(self.possible_games)(self)) for _ in range(self.num_rounds)]
        # TODO shuffle them such that they don't repeat right after each other

    async def start_a_game(self, message):
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

        :param message:
        :return:
        """
        print("Playing a game")
        # TODO: Move logic for repeated words to here
        # TODO: Make people unable to respond consecutively
        await self.game().play(message)

    def game(self):
        return self.games[self.game_round - 1]
