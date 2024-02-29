from random import choice


def message_congratulate_correct():
    return choice([
        "Correct ✅. ",
        "✅ ",
        "Congrats! 🎉 "])


def message_next_word():
    return choice(["What else have you got?",
                   "Can you think of more words?",
                   "And next one is...?",
                   "Give me more words 😤"])


class StreakGame:
    def __init__(self, competition_object):
        self.competition = competition_object  # We are using the competition class to store the competition
        self.used_words = []  # Store list of words that are already used
        self.streak = 0  # Keeping track of the correct rhymes in a row

    async def play(self, message):
        """
        This function is for listening to the words that the user sends and checking if they rhyme with the word to rhyme
        :param message:
        :return:
        """
        # Check is the words has been used already
        if message.content in self.used_words:
            await self.on_fail(message, reason="already used")
            return

    async def on_success(self, message):
        """
        This function returns a message to send when the user rhymes a word correctly
        :param message:
        :return: the message to send
        """
        self.used_words.append(message.content)
        self.streak += 1  # Increase the streak of the group by 1
        await message.channel.send(
            message_congratulate_correct() + self.message_confirm_correct(
                message) + "\n" + self.message_on_streak() + "\n" + message_next_word())

    def message_confirm_correct(self, message):
        return f"PLACEHOLDER {message.content}."

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
            streak_message += "\n🏆" + choice(["Your streak is at ",
                                              "You have a streak of ",
                                              "You are at ",
                                              "You have done a grand total of "])
            streak_message += str(self.streak) + " correct answers in a row! 🏆"
        return streak_message

    async def on_fail(self, message, reason="already used"):
        """
        This function is called when the user fails to rhyme a word
        :param reason:
        :param message:
        :return:
        """
        self.competition.penalty.penalty(message.author)  # Add a penalty point to the user
        # Generate a message to send

        await message.channel.send(self.message_on_fail(message.author)
                                   + "\n" + self.message_fail_reason(reason, message)
                                   + "\n" + self.competition.penalty.message_on_penalty(message.author))
        await self.competition.start_a_game(message)  # Start a new game

    def message_on_fail(self, author):
        return choice([
            f"{author} goofed up! ❌",
            f"Ding ding ding! 🔔 {author} made a mistake",
            f"Ouch! {author} made a mistake ❌"])

    def message_fail_reason(self, reason, message):
        if reason == "already used":
            return choice([
                f"{message.content} has already been used.",
                f"{message.author} is falling into repetition, {message.content} has already been said.",
                f"{message.author} is a copycat, someone mentioned {message.content} already.",
                f"How original 🥱 {message.author}, {message.content} is already taken.",
                f"Someone said {message.content} already."
            ])

    def message_on_start(self):
        return "\n" + choice(["Let's go!", "Vamos!", "Let's play!", "Let's get into it!"]) + "🏁"
