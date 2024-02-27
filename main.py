import os
import discord
import requests
import nltk
import time
from dotenv import load_dotenv
from random import randint, choice

# LOAD OUR TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class Piccolo(discord.Client):
    word_to_rhyme = ''  # Variable to decide which word is going to be used for rhyming
    rhyming_words = []  # Store list of words given from the API
    streak = 0  # Keeping track of the correct rhymes in a row
    used_words = []  # Store list of words that are already used
    penalty_points = {}  # Storing the amount of penalty points of each player
    game = ''  # Empty game

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        """
        This function is called every time a message is sent in the server
        :param message:
        :return:
        """
        print(f'Message from {message.author}: {message.content}')
        if message.author == client.user:
            return

        if self.game == '':  # If no game is running
            await self.start_game(message)
            return
        if self.game == 'rhyme':  # If a game of rhyme is running
            await self.rhyme(message)

    async def start_game(self, message):
        """
        This function is for listening whether they want to start a game
        :param message:
        :return:
        """
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(message.content)
        if 'start' in words and 'game' in words:  # If the message contains the words "start" and "game" the game starts
            await message.channel.send(
                "Hey, my name is Piccolo and I'll be your Gamemaster 😎 \n https://giphy.com/gifs/mma-announcer-carlos-kremer-xT39Db8zIOODTppk08")
            time.sleep(3)
            self.game = 'rhyme'
            self.generate_new_word_to_rhyme()
            await message.channel.send(f"Word to rhyme is {self.word_to_rhyme}")
        else:  # It will tell the user how to start the game
            await message.channel.send(
                'Hello, if you would like to start a game jus type "start game" 🤓 \n https://giphy.com/gifs/Friends-episode-15-friends-tv-the-one-where-estelle-dies-W3a0zO282fuBpsqqyD')

    def generate_new_word_to_rhyme(self):
        """
        This function generates a new word to rhyme
        :return:
        """
        api_url = 'https://api.datamuse.com/words?rel_jja=yellow'  # We are using this api to get a list of words
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            response = response.json()
            self.word_to_rhyme = response[randint(0, len(response) - 1)][
                'word']  # We choose a random word from the list
            api_url = 'https://api.datamuse.com/words?rel_rhy={}'.format(
                self.word_to_rhyme)  # We use the word to get a list of words that rhyme with it
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                self.rhyming_words = response.json()  # convert response string to json
            else:
                print("Error:", response.status_code, response.text)
        else:
            print("Error:", response.status_code, response.text)

    async def rhyme(self, message):
        # Check is the words has been used already
        if message.content in self.used_words:
            await message.channel.send("You already used that word")
            await self.on_fail(message, reason="already used")
            return
        # Check if the word rhymes with the word to rhyme
        for word in self.rhyming_words:
            if word['word'] == message.content:
                self.used_words.append(message.content)
                self.streak += 1  # Increase the streak of the group by 1
                await message.channel.send(
                    self.message_on_successful_rhyme(message))
                return
        await self.on_fail(message)

    def message_on_successful_rhyme(self, message):
        """
        This function returns a message to send when the user rhymes a word correctly
        :param message:
        :return: the message to send
        """
        rhyme_confirmation = choice([f"Correct ✅  {message.content} rhymes with {self.word_to_rhyme}."])
        congratulation = ""
        if self.streak == 5:
            congratulation = choice(["Well done!",
                                     "Great job!"])
        elif self.streak == 10:
            congratulation = choice(["You guys are killing it!",
                                     "You folk are doing great!"])
        elif self.streak == 15:
            congratulation = choice(["You people are on fire🔥!"])
        if self.streak % 5 == 0:
            congratulation += "\n" + choice(["Your streak is at ",
                                             "You have a streak of ",
                                             "You are at ",
                                             "You have done a grand total of "])
            congratulation += str(self.streak) + " rhymes in a row! 🏆"
        on_next_word = choice(["What else have you got?",
                               "Can you think of more words?",
                               "And next one is...?",
                               "Give me more words 😤"])
        return rhyme_confirmation + "\n" + congratulation + "\n" + on_next_word

    async def on_fail(self, message, reason="does not rhyme"):
        """
        This function is called when the user fails to rhyme a word
        :param message: 
        :return: 
        """
        # Check if author is already in the penalty dictionary
        if message.author in self.penalty_points:
            self.penalty_points[message.author] += 1
        else:
            self.penalty_points[message.author] = 1
        # send the penalty message
        await message.channel.send(self.message_on_penalty(message.author, message.content, reason))
        self.streak = 0  # Reset the streak
        self.used_words = []  # Reset the used words
        self.generate_new_word_to_rhyme()  # Generate a new word to rhyme
        await message.channel.send(self.message_on_new_word())

    def message_on_new_word(self):
        end = choice(["Let's go!", "Vamos!", "Let's play!", "Let's get into it!"])
        return f"\nNew word to rhyme is **{self.word_to_rhyme}**. {end} 🏁"

    def message_on_penalty(self, author, content, reason="does not rhyme"):
        """
        This function returns a message to send when the user fails to rhyme a word
        :param reason:
        :param author: the user who failed
        :param content: the word that the user sent
        :return: a message to send
        """
        start = choice([
            f"{author} goofed up! ❌",
            f"Ding ding ding! 🔔 {author} made a mistake",
            f"Ouch! {author} made a mistake ❌"])
        if reason == "does not rhyme":
            does_not_rhyme = choice([
                f"{content} does not rhymes with {self.word_to_rhyme}.",
                f"It seems {author} thought {content} rhymes with {self.word_to_rhyme}.",
                f"Obviously {content} does not rhyme with {self.word_to_rhyme}."])
        elif reason == "already used":
            does_not_rhyme = choice([
                f"{content} has already been used.",
                f"{author} is falling into repetition, {content} has already been said.",
                f"{author} is a copycat, someone mentioned {content} already.",
                f"How original 🥱 {author}, {content} is already taken.",
                f"Someone said {content} already."
            ])
        if self.penalty_points[author] == 1:  # First time the player made a mistake
            end = choice([
                f"{author} got their first penalty point. ⚠️",
                f"{author} was doing so well, but now they have a penalty point. ⚠️"
            ])
        elif self.penalty_points[author] > 10:  # If the player has more than 10 penalty points
            end = choice([
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
                f"Are you sabotaging the game {author}? You have {self.penalty_points[author]} points already!",
                f"Are you trying to collect points {author}? If so then you are doing a great job, you have {self.penalty_points[author]} points already!"])
        elif self.penalty_points[author] > 5:  # If the player has more than 5 penalty points
            end = choice([
                f"Looks like {author} is struggling, they have {self.penalty_points[author]} points already!",
                f"It is not looking great for {author}, they already have {self.penalty_points[author]} points!",
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
            ])
        else:  # If the player has > 1 penalty point
            end = choice(
                [f"They have now {self.penalty_points[author]} penalty points.",
                 f"It is now {self.penalty_points[author]} penalty points for {author}.",
                 f"They are steadily collecting penalty points, they have {self.penalty_points[author]} now.",
                 f"{author} has {self.penalty_points[author]} penalty points now."
                 ])
        return start + "\n" + does_not_rhyme + "\n" + end


intents = discord.Intents.default()
intents.message_content = True

client = Piccolo(intents=intents)
client.run(TOKEN)
