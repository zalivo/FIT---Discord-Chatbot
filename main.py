import os
import discord
import requests
import nltk
from dotenv import load_dotenv
from random import randint

# LOAD OUR TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def start_game(self, message):
        start = False
        game = False
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(message)
        for word in words:
            if word == 'start':
                start = True
            if word == 'game':
                game = True
        if start == True and game == True:
            self.generate_new_word_to_rhyme(self)

    word_to_rhyme = ''
    rhyming_words = []
    score = 0
    used_words = []
    penalty_points = {}
    game = 'rhyme'
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    def generate_new_word_to_rhyme(self):
        api_url = 'https://api.datamuse.com/words?ml=funny'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            response = response.json()
            self.word_to_rhyme = response[randint(0, len(response)-1)]['word']
            api_url = 'https://api.datamuse.com/words?rel_rhy={}'.format(self.word_to_rhyme)
            response = requests.get(api_url)
            if response.status_code == requests.codes.ok:
                # convert response.txt string to json
                self.rhyming_words = response.json()
            else:
                print("Error:", response.status_code, response.text)

            # send message to the same channel
        else:
            print("Error:", response.status_code, response.text)

        async def rhyme(self, message):
            # Check is the words has been used already
            if message.content in self.used_words:
                await message.channel.send("You already used that word")
                await self.on_fail(message)
                return

            for word in self.rhyming_words:
                if word['word'] == message.content:
                    self.used_words.append(message.content)
                    self.score += 1
                    await message.channel.send(
                        f"Correct {message.content} rhymes with {self.word_to_rhyme}\n Your score is {self.score} 🔥")
                    return
            await message.channel.send(
                f"Incorrect {message.content} does not rhymes with {self.word_to_rhyme}\n Your score was {self.score} 🔥")
            await self.on_fail(message)

        # async def describe (self, message):
        #     # Example: adjectives that are often used to describe ocean


    async def on_fail(self, message):
        self.score = 0
        self.used_words = []
        self.generate_new_word_to_rhyme()
        # Check if author is already in the penalty dictionary
        if message.author in self.penalty_points:
            self.penalty_points[message.author] += 1
        else:
            self.penalty_points[message.author] = 1

        await message.channel.send(f"New word to rhyme is {self.word_to_rhyme}")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        #send message to the same channel
        if message.author == client.user:
            return
        if message.content == 'hello':
            await message.channel.send('WELCOME STRING')
            return
        if message.content == 'ping':
            await message.channel.send('pong')
            return
        if self.game == 'rhyme':
            self.rhyme(message)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)