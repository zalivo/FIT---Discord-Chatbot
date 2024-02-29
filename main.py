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
    competition = None  # Empty competition

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
        else:
            if self.competition.game:  # If a game is running
                await self.competition.play(message)
            else:
                if self.competition.round < self.competition.rounds:
                    await self.competition.start_a_game(message)
                else:
                    await message.channel.send("The game is over! 🏁")
                    self.competition = None

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
                "Hey, my name is Piccolo and I'll be your Gamemaster 😎 \n https://giphy.com/gifs/mma-announcer-carlos-kremer-xT39Db8zIOODTppk08")
            time.sleep(3)
            self.competition = Competition()
            await self.competition.start_a_game(message)
        else:  # It will tell the user how to start the game
            await message.channel.send(
                'Hello, if you would like to start a game jus type "start game" 🤓 \n https://giphy.com/gifs/Friends-episode-15-friends-tv-the-one-where-estelle-dies-W3a0zO282fuBpsqqyD')


intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
client.run(TOKEN)
