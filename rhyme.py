from random import randint, choice
import requests
from wonderwords import RandomWord

randomWord = RandomWord()

class Rhyme:
    word_to_rhyme = ''  # Variable to decide which word is going to be used for rhyming
    rhyming_words = []  # Store list of words given from the API
    used_words = []  # Store list of words that are already used
    streak = 0  # Keeping track of the correct rhymes in a row


    def __init__(self, competition_object):
        self.competition = competition_object  # We are using the competition class to store the competition
        self.generate_word_to_rhyme()  # We are generating a new word to rhyme

    def message_on_start(self):
        end = choice(["Let's go!", "Vamos!", "Let's play!", "Let's get into it!"])
        return f"\nThe word to rhyme is **{self.word_to_rhyme}**. {end} 🏁"

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
        # uncapitalize the word
        message.content = message.content.lower()
        # Check if the word is the original word
        if message.content == self.word_to_rhyme:
            await self.on_fail(message, reason="original word")
            return

        # Check is the words has been used already
        if message.content in self.used_words:
            await self.on_fail(message, reason="already used")
            return
        # Check if the word rhymes with the word to rhyme
        for word in self.rhyming_words:
            if word['word'] == message.content:
                await self.on_success(message)
                return
        await self.on_fail(message)

    async def on_success(self, message):
        """
        This function returns a message to send when the user rhymes a word correctly
        :param message:
        :return: the message to send
        """
        self.used_words.append(message.content)
        self.streak += 1  # Increase the streak of the group by 1

        rhyme_confirmation = choice([f"Correct ✅  {message.content} rhymes with {self.word_to_rhyme}.",
                                     f"✅ {message.content} does indeed rhyme with {self.word_to_rhyme}",
                                     f"Congrats! 🎉 {message.content} does indeed rhyme with {self.word_to_rhyme}",
                                     ])

        on_next_word = choice(["What else have you got?",
                               "Can you think of more words?",
                               "And next one is...?",
                               "Give me more words 😤"])
        await message.channel.send(rhyme_confirmation + "\n" + self.message_on_streak() + "\n" + on_next_word)

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
            streak_message += str(self.streak) + " rhymes in a row! 🏆"
        return streak_message

    async def on_fail(self, message, reason="does not rhyme"):
        """
        This function is called when the user fails to rhyme a word
        :param reason:
        :param message:
        :return:
        """
        self.competition.penalty.penalty(message.author)  # Add a penalty point to the user
        # Generate a message to send
        does_not_rhyme = ""
        if reason == "does not rhyme":
            does_not_rhyme = choice([
                f"{message.content} does not rhymes with {self.word_to_rhyme}.",
                f"It seems {message.author} thought {message.content} rhymes with {self.word_to_rhyme}.",
                f"Obviously {message.content} does not rhyme with {self.word_to_rhyme}."])
        elif reason == "already used":
            does_not_rhyme = choice([
                f"{message.content} has already been used.",
                f"{message.author} is falling into repetition, {message.content} has already been said.",
                f"{message.author} is a copycat, someone mentioned {message.content} already.",
                f"How original 🥱 {message.author}, {message.content} is already taken.",
                f"Someone said {message.content} already."
            ])
        elif reason == "original word":
            does_not_rhyme = choice([
                f"{message.content} is the word you are suppose to rhyme upon!",
                f"Did {message.author} forget that the original word to rhyme upon is {message.content}?",
                f"{message.author} is a copycat, you are suppose to rhyme with {message.content}.",
                f"How original 🥱 {message.author}, {message.content} is already taken.",
                f"Hey! {message.content} is my word."
            ])
        await message.channel.send(self.competition.penalty.message_on_fail(message.author)
                                   + "\n" + does_not_rhyme
                                   + "\n" + self.competition.penalty.message_on_penalty(message.author))
        await self.competition.start_a_game(message)  # Start a new game
