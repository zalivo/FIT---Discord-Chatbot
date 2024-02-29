import os
import time

import discord
import nltk
from dotenv import load_dotenv

from competition import Competition

# LOAD OUR TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class Bot(discord.Client):
    competition = None  # The competition, if there is one

    async def on_message(self, message):
        """
        This function is called every time a message is sent in the server
        :param message:
        :return:
        """
        print(f'Message from {message.author}: {message.content}')
        if message.author == client.user:
            return
        if not self.competition:
            await self.start_competition(message)
        else:  # If a competition is running
            if self.competition.round == self.competition.rounds:  # If the game is over
                await message.channel.send("The game is over! 🏁")
                self.competition = None
            else:
                await self.competition.play(message)

    async def start_competition(self, message):
        """
        This function is for listening whether they want to start a game
        :param message:
        :return:
        """
        print("Starting a new competition")
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(message.content)
        if 'start' in words and 'game' in words:  # If the message contains the words "start" and "game" the game starts
            await message.channel.send(
                "Hey, my name is Piccolo and I'll be your Game-master 😎 "
                "\n https://giphy.com/gifs/mma-announcer-carlos-kremer-xT39Db8zIOODTppk08")
            time.sleep(1)
            self.competition = Competition()
            await self.competition.start_a_game(message)
        else:  # It will tell the user how to start the game
            await message.channel.send(
                'Hello, if you would like to start a game just type "start game" 🤓 '
                '\n https://giphy.com/gifs/Friends-episode-15-friends-tv-the-one-where-estelle-dies-W3a0zO282fuBpsqqyD')


intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
client.run(TOKEN)
