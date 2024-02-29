# Setup
1. Clone the repository
2. Import libraries if neccescairy
3. Run main.py to start the bot 
4. Invite it to a discord channel.
5. Type anything, and play the game!

# Add more games
1. Copy rhyme.py and rename it to your game. Then add it to the games list in competition.py. 
2. Edit the game to your liking.

You can also add a custom game to the games list in competition.py. The game should be a class with the following methods:
```python
def __init__(self, competition_object):
    super().__init__(competition_object)
    # YOUR GAME VARIABLES

def message_on_start(self):
    return f"\nYOUR GAME EXPLEANATION" + super().message_on_start()

async def play(self, message):
    # YOUR GAME LOGIC
    pass 
```
call
```python
await self.competition.start_a_game(message)
```
to end your minigame