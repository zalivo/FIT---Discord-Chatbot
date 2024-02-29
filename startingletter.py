from random import randint, choice

import nltk
import requests


class StartingLetter:
    starting_letter = ''  # Variable to decide which word is going to be used for rhyming
    used_words = []  # Store list of words that are already used
    streak = 0  # Keeping track of the correct starts in a row

    def __init__(self, competition_object):
        self.competition = competition_object  # We are using the competition class to store the competition
        self.generate_starting_letter()  # We are generating a new word to start

    def message_on_start(self):
        end = choice(["Let's go!", "Vamos!", "Let's play!", "Let's get into it!"])
        return f"\nThe starting letter is **{self.starting_letter}**. {end} 🏁"

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
        # uncapitalize the word
        message.content = message.content.lower()
        # Check is the words has been used already
        if message.content in self.used_words:
            await self.on_fail(message, reason="already used")
            return
        # Check if the word starts with the word to start
        if message.content[0] != self.starting_letter:
            await self.on_fail(message, reason="does not start")
        elif message.content not in nltk.corpus.words.words():  # use nltk to check if the word is a valid word
            await self.on_fail(message, reason="not a word")
        else:
            await self.on_success(message)

    async def on_fail(self, message, reason="does not start"):
        """
        This function is called when the user fails to start a word
        :param reason:
        :param message:
        :return:
        """
        self.competition.penalty.penalty(message.author)  # Add a penalty point to the user
        # Generate a message to send
        does_not_start = ""
        if reason == "does not start":
            does_not_start = choice([
                f"{message.content} does not starts with {self.starting_letter}.",
                f"It seems {message.author} thought {message.content} starts with {self.starting_letter}.",
                f"Obviously {message.content} does not start with {self.starting_letter}."])
        elif reason == "already used":
            does_not_start = choice([
                f"{message.content} has already been used.",
                f"{message.author} is falling into repetition, {message.content} has already been said.",
                f"{message.author} is a copycat, someone mentioned {message.content} already.",
                f"How original 🥱 {message.author}, {message.content} is already taken.",
                f"Someone said {message.content} already."
            ])
        elif reason == "not a word":
            does_not_start = choice([
                f"{message.content} is not a word.",
                f"{message.content} is not a valid word.",
                f"{message.content} is not a word in English.",
                f"{message.content} is not a word, it is a made up word."
            ])
        await message.channel.send(self.competition.penalty.message_on_fail(message.author)
                                   + "\n" + does_not_start
                                   + "\n" + self.competition.penalty.message_on_penalty(message.author))
        await self.competition.start_a_game(message)  # Start a new game

    async def on_success(self, message):
        """
        This function returns a message to send when the user starts a word correctly
        :param message:
        :return: the message to send
        """
        self.used_words.append(message.content)
        self.streak += 1  # Increase the streak of the group by 1

        start_confirmation = choice([f"Correct ✅  {message.content} starts with {self.starting_letter}.",
                                     f"✅ {message.content} does indeed start with {self.starting_letter}",
                                     f"Congrats! 🎉 {message.content} does indeed start with {self.starting_letter}",
                                     ])

        on_next_word = choice(["What else have you got?",
                               "Can you think of more words?",
                               "And next one is...?",
                               "Give me more words 😤"])
        await message.channel.send(start_confirmation + "\n" + self.message_on_streak() + "\n" + on_next_word)

    def message_on_streak(self):
        """
        :return:
        """
        streak_message = ""
        if self.streak == 5:
            streak_message = choice(["Well done!",
                                     "Great job!"])
        elif self.streak == 10:
            streak_message = choice(["You guys are killing it!",
                                     "You folk are doing great!"])
        elif self.streak == 15:
            streak_message = choice(["You people are on fire🔥!"])
        if self.streak % 5 == 0:
            streak_message += "\n" + choice(["Your streak is at ",
                                             "You have a streak of ",
                                             "You are at ",
                                             "You have done a grand total of "])
            streak_message += str(self.streak) + " words in a row! 🏆"
        return streak_message
