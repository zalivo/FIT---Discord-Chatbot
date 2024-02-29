from random import randint, choice


class Penalty:
    penalty_points = {}

    def message_on_fail(self, author):
        return choice([
            f"{author} goofed up! ❌",
            f"Ding ding ding! 🔔 {author} made a mistake",
            f"Ouch! {author} made a mistake ❌"])

    def message_on_penalty(self, author):
        """
        :return: a message to send
        """

        if self.penalty_points[author] == 1:  # First time the player made a mistake
            return choice([
                f"{author} got their first penalty point. ⚠️",
                f"{author} was doing so well, but now they have a penalty point. ⚠️"
            ])
        elif self.penalty_points[author] > 10:  # If the player has more than 10 penalty points
            return choice([
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
                f"Are you sabotaging the game {author}? You have {self.penalty_points[author]} points already!",
                f"Are you trying to collect points {author}? If so then you are doing a great job, you have {self.penalty_points[author]} points already!"])
        elif self.penalty_points[author] > 5:  # If the player has more than 5 penalty points
            return choice([
                f"Looks like {author} is struggling, they have {self.penalty_points[author]} points already!",
                f"It is not looking great for {author}, they already have {self.penalty_points[author]} points!",
                f"What are you doing {author}? You have {self.penalty_points[author]} points already!",
            ])
        else:  # If the player has > 1 penalty point
            return choice(
                [f"They have now {self.penalty_points[author]} penalty points.",
                 f"It is now {self.penalty_points[author]} penalty points for {author}.",
                 f"They are steadily collecting penalty points, they have {self.penalty_points[author]} now.",
                 f"{author} has {self.penalty_points[author]} penalty points now."
                 ])


