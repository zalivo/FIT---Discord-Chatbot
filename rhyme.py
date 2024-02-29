from random import choice
import requests
from wonderwords import RandomWord

from abstractstreakgame import StreakGame

randomWord = RandomWord()


class Rhyme(StreakGame):

    def __init__(self, competition_object):
        super().__init__(competition_object)
        self.rhyming_words = None
        self.word_to_rhyme = None
        self.generate_word_to_rhyme()  # We are generating a new word to rhyme

    def message_on_start(self):
        return f"\nThe word to rhyme is **{self.word_to_rhyme}**." + super().message_on_start()

    def generate_word_to_rhyme(self):
        """
        This function generates a new word to rhyme
        :return:
        """
        self.word_to_rhyme = randomWord.word(include_parts_of_speech=["nouns"], word_min_length=3, word_max_length=10)
        api_url = 'https://api.datamuse.com/words?rel_rhy={}&max=1000'.format(
            self.word_to_rhyme)  # We use the word to get a list of words that rhyme with it
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            self.rhyming_words = response.json()  # convert response string to json
        else:
            print("Error:", response.status_code, response.text)

    async def play(self, message):
        """
        This function is for listening to the words that the user sends and checking if they rhyme with the word to rhyme
        :param message:
        :return:
        """
        await super().play(message)

        if message.content == self.word_to_rhyme:
            await self.on_fail(message, reason="original word")
            return
        # Check if the word rhymes with the word to rhyme
        for word in self.rhyming_words:
            if word['word'] == message.content:
                await self.on_success(message)
                return
        await self.on_fail(message, reason="does not rhyme")

    def message_fail_reason(self, reason, message):
        if reason == "does not rhyme":
            return choice([
                f"{message.content} does not rhymes with {self.word_to_rhyme}.",
                f"It seems {message.author} thought {message.content} rhymes with {self.word_to_rhyme}.",
                f"Obviously {message.content} does not rhyme with {self.word_to_rhyme}."])
        elif reason == "original word":
            return choice([
                f"{message.content} is the word you are suppose to rhyme upon!",
                f"Did {message.author} forget that the original word to rhyme upon is {message.content}?",
                f"{message.author} is a copycat, you are suppose to rhyme with {message.content}.",
                f"How original 🥱 {message.author}, {message.content} is already taken.",
                f"Hey! {message.content} is my word."
            ])
        else:
            return super().message_fail_reason(reason, message)

    def message_confirm_correct(self, message):
        return choice([f"{message.content} rhymes with {self.word_to_rhyme}.",
                       f"{message.content} does indeed rhyme with {self.word_to_rhyme}",
                       f"{message.content} does in fact rhyme with {self.word_to_rhyme}",
                       ])
