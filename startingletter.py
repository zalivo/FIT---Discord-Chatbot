from random import randint, choice

import nltk

from abstractstreakgame import StreakGame


class StartingLetter(StreakGame):

    def __init__(self, competition_object):
        super().__init__(competition_object)
        self.starting_letter = None
        self.generate_starting_letter()  # We are generating a new word to start

    def message_on_start(self):
        return f"\nThe starting letter is **{self.starting_letter}**." + super().message_on_start()

    def generate_starting_letter(self):
        """
        This function generates a new word to start
        :return:
        """
        self.starting_letter = chr(randint(97, 122))  # Generate a random letter

    async def play(self, message):
        """
        This function is for listening to the words that the user sends and checking if they start with the word to start
        :param message:
        :return:
        """
        await super().play(message)
        # Check if the word starts with the word to start
        if message.content[0] != self.starting_letter:
            await self.on_fail(message, reason="does not start")
        elif message.content not in nltk.corpus.words.words():  # use nltk to check if the word is a valid word
            await self.on_fail(message, reason="not a word")
        else:
            await self.on_success(message)

    def message_fail_reason(self, reason, message):
        if reason == "does not start":
            return choice([
                f"{message.content} does not starts with {self.starting_letter}.",
                f"It seems {message.author} thought {message.content} starts with {self.starting_letter}.",
                f"Obviously {message.content} does not start with {self.starting_letter}."])
        elif reason == "not a word":
            return choice([
                f"{message.content} is not a word.",
                f"{message.content} is not a valid word.",
                f"{message.content} is not a word in English.",
                f"{message.content} is not a word, it is a made up word."
            ])
        else:
            return super().message_fail_reason(reason, message)

    def message_confirm_correct(self, message):
        return choice([f"{message.content} starts with {self.starting_letter}.",
                       f"{message.content} does indeed start with {self.starting_letter}",
                       f"{message.content} does indeed start with {self.starting_letter}",
                       ])
