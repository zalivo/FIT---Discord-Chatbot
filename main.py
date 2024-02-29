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
        # TODO: add commands, to skip a game, to see the leaderboard, to see the rules, to see the help, end the game
        if not self.competition:
            await self.start_competition(message)
        else:  # If a competition is running
            await self.competition.play(message)
            # check if the game is over
            if self.competition.game_round == self.competition.num_rounds + 1:
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
        if 'start' in words or 'game' in words:  # If the message contains the words "start" and "game" the game starts
            await message.channel.send(
                "Hey, my name is Piccolo and I'll be your Game-master 😎 "
                "\n https://giphy.com/gifs/mma-announcer-carlos-kremer-xT39Db8zIOODTppk08")
            time.sleep(1)
            # if a number is given, use it as the number of rounds, the number can be anywhere in the message
            for word in words:
                if word.isdigit():
                    self.competition = Competition(int(word))
                    break
            if not self.competition:
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
