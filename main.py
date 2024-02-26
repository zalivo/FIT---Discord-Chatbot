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


class MyClient(discord.Client):
    async def start_game(self, message):
        start = False
        game = False
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(message.content)
        for word in words:
            if word == 'start':
                start = True
            if word == 'game':
                game = True
        if start and game:
            await message.channel.send(
                "Hey, my name is Piccolo and I'll be your Gamemaster 😎 \n https://giphy.com/gifs/mma-announcer-carlos-kremer-xT39Db8zIOODTppk08")
            time.sleep(3)
            self.game = 'rhyme'
            self.generate_new_word_to_rhyme()
            await message.channel.send(f"Word to rhyme is {self.word_to_rhyme}")
        else:
            await message.channel.send(
                'Hello, if you would like to start a game jus type "start game" 🤓 \n https://giphy.com/gifs/Friends-episode-15-friends-tv-the-one-where-estelle-dies-W3a0zO282fuBpsqqyD')

    word_to_rhyme = ''
    rhyming_words = []
    score = 0
    used_words = []
    penalty_points = {}
    game = ''

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    def generate_new_word_to_rhyme(self):
        print("generate_new_word_to_rhyme")
        api_url = 'https://api.datamuse.com/words?rel_jja=yellow'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            response = response.json()
            self.word_to_rhyme = response[randint(0, len(response) - 1)]['word']
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
                    self.congrats(message))
                return
        await self.on_fail(message)

    def congrats(self, message):
        rhyme_confirmation = choice([f"Correct ✅  {message.content} rhymes with {self.word_to_rhyme}."])
        congratulations = ["You are on fire🔥!", "You are killing it!", "You are doing great!", "Well done!",
                          "Great job!"]
        score_messages = [" Your score is ", " You have ", " You are at ", " You have "]

        score_msg = choice(score_messages) + str(self.score)
        if self.score == 1:
            score_msg += ' point.'
        else:
            score_msg += ' points.'
        if self.score < 2:
            congratulation = congratulations[3]

        elif self.score >= 2 and self.score < 6:
            congratulation = congratulations[2]

        elif self.score >= 6 and self.score < 9:
            congratulation = congratulations[0]

        else:
            congratulation = congratulations[1]
        on_next_word = choice(
            ["What else have you got?", "Can you think of more words?", "And ...?", "Give me more words 😤"])
        return rhyme_confirmation + "\n" + score_msg + "\n" + congratulation + "\n" + on_next_word

    async def on_fail(self, message):
        # Check if author is already in the penalty dictionary
        if message.author in self.penalty_points:
            self.penalty_points[message.author] += 1
        else:
            self.penalty_points[message.author] = 1
        # send the penalty message
        await message.channel.send(self.on_penalty_message(message.author, message.content))
        self.score = 0
        self.used_words = []
        self.generate_new_word_to_rhyme()
        await message.channel.send(f"\nNew word to rhyme is **{self.word_to_rhyme}**. {self.on_new_word_message()} 🏁")

    # ARRAY FOR STORING AND RANDOMLY CHOOSING PHRASES FOR NEW WORD GENERATING
    def on_new_word_message(self):
        message_on_new_word = ["Let's go!", "Vamos!", "Let's play!", "Let's get into it!"]
        return choice(message_on_new_word)



    def on_penalty_message(self, author, content):

        start = choice([
            f"{author} goofed up! ❌",
            f"Ding ding ding! 🔔 {author} made a mistake",
            f"Ouch! {author} made a mistake ❌"])
        does_not_rhyme = choice([
            f"{content} does not rhymes with {self.word_to_rhyme}.",
            f"It seems {author} thought {content} rhymes with {self.word_to_rhyme}.",
            f"Obviously {content} does not rhyme with {self.word_to_rhyme}."
        ])
        if self.penalty_points[author] == 1:  # First time the player made a mistake
            end = choice([
                f"{author} got their first penalty point. ⚠️",
                f"{author} was doing so well, but now they have a penalty point. ⚠️"
            ])
        elif self.penalty_points[author] > 10:
            end = choice([
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
                f"Are you sabotaging the game {author}? You have {self.penalty_points[author]} points already!",
                f"Are you trying to collect points {author}? If so then you are doing a great job, you have {self.penalty_points[author]} points already!"])
        elif self.penalty_points[author] > 5:
            end = choice([
                f"Looks like {author} is struggling, they have {self.penalty_points[author]} points already!",
                f"It is not looking great for {author}, they already have {self.penalty_points[author]} points!",
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
            ])
        else:
            end = choice([f"They have now {self.penalty_points[author]}."])

        return start + "\n" + does_not_rhyme + "\n" + end

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        # send message to the same channel
        if message.author == client.user:
            return

        if self.game == '':
            await self.start_game(message)
            return
        if self.game == 'rhyme':
            await self.rhyme(message)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
