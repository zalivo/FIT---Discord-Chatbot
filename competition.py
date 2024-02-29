import time

import nltk

from penalty import Penalty

import rhyme


class Competition:
    penalty: Penalty  # Storing the penalty object
    game = None  # Empty game
    rounds = 10  # Number of rounds
    round = 0  # Current round

    # initialize the class
    def __init__(self):
        self.penalty = Penalty()  # We are using the penalty class to store the penalty points of the players

    async def start_a_game(self, message):
        print("Starting a new game")
        self.round += 1
        # We create a new game of Rhyme using the Rhyme class
        self.game = rhyme.Rhyme(self)
        await message.channel.send(self.game.message_on_start())

    async def play(self, message):
        """

        :param message:
        :return:
        """
        print("Playing a game")
        await self.game.play(message)
