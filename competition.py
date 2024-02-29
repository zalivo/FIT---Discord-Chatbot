import time

import nltk
from random import randint, choice
from penalty import Penalty

import rhyme
from startingletter import StartingLetter


class Competition:
    penalty: Penalty  # Storing the penalty object
    games = []  # Current game
    rounds = 10  # Number of rounds
    round = 0  # Current round
    possible_games = [rhyme.Rhyme, StartingLetter]  # List of possible games

    # initialize the class
    def __init__(self):
        self.penalty = Penalty()  # We are using the penalty class to store the penalty points of the players
        # generate games here, and shuffle them such that they don't repeat right after each other
        self.games = [(choice(self.possible_games)(self)) for _ in range(self.rounds)]
        # TODO shuffle them such that they don't repeat right after each other
        print(self.games)

    async def start_a_game(self, message):
        print("Starting a new game")
        self.round += 1
        await message.channel.send(self.game().message_on_start())

    async def play(self, message):
        """

        :param message:
        :return:
        """
        print("Playing a game")
        await self.game().play(message)

    def game(self):
        return self.games[self.round - 1]
