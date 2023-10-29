from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# player.py
class Player:
    def __init__(self, name, budget, image_path):
        self.name = name
        self.budget = budget
        self.image_path = image_path
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)
        character.set_owner(self)

    def deduct_budget(self, amount):
        self.budget -= amount

# character.py
class Character:
    def __init__(self, name, base_price, role, image_path, owner="Un Sold"):
        self.name = name
        self.image_path = image_path
        self.base_price = base_price
        self.role = role
        self.owner = owner
        self.performance_points = 0

    def set_owner(self, player):
        self.owner = player
        self.name = player.name

    def update_performance_points(self, points):
        self.performance_points += points

# character_pool.py

class CharacterPool:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)


class BiddingEngine():
    def __init__(self):
        self.Dont_Know = None

    def start_bidding(self, players, character_pool):
        for character in character_pool.characters:
            print(f"\nBidding for {character.name}:")
            current_bidder = random.choice(players)
            sold_price = 0
            current_bid_price = character.base_price
            while True:
                bid_continue = str(input(f"{current_bidder.name}, continue at {current_bid_price} for {character.name}"))
                if bid_continue=="y":
                    sold_price = current_bid_price
                    bid_owner = current_bidder
                    current_bid_price += 20
                    current_bidder = players[(players.index(current_bidder)+1)%len(players)]
                elif sold_price==0:
                    print(f"{character.name} with base price {character.base_price} gone unsold.")
                    break
                else:
                    bid_owner.add_character(character)
                    bid_owner.deduct_budget(sold_price)
                    print(f"{character.name}, sold to {bid_owner.name} at {sold_price} million rupees.")
                    print(f"{players[0].name} has a budget of {players[0].budget}")
                    print(f"{players[1].name} has a budget of {players[1].budget}")
                    break
                if current_bidder.budget<current_bid_price:
                    bid_owner.add_character(character)
                    bid_owner.deduct_budget(sold_price)
                    print(f"{character.name}, sold to {bid_owner.name} at {sold_price} million rupees.")
                    print(f"{players[0].name} has a budget of {players[0].budget}")
                    print(f"{players[1].name} has a budget of {players[1].budget}")
                    break                    



# scoring_engine.py
class ScoringEngine:
    def calculate_points(self, character):
        runs = int(input(f"Run scored by {character.name}: "))
        wickets = int(input(f"Wicket taken by {character.name}: "))
        catches = int(input(f"Catch taken by {character.name}: "))
        stumps = int(input(f"Stump by {character.name}: "))
        performance_points = runs + wickets*30 + catches*8 + stumps*8
        character.update_performance_points(performance_points)

# game_manager.py
class GameManager:
    def __init__(self, players, character_pool):
        self.players = players
        self.character_pool = character_pool

    def start_game(self):
        print("\nBidding phase:")
        bidding_engine = BiddingEngine()
        bidding_engine.start_bidding(self.players, self.character_pool)

        print("\nScoring phase:")
        scoring_engine = ScoringEngine()
        for character in character_pool.characters:
            scoring_engine.calculate_points(character)

        while True:
            match_finished = str(input(f"is match finished: "))
            if match_finished == "yes":
                self.determine_winner()
                break

    def determine_winner(self):
        player_scores = {player.name: sum(character.performance_points for character in player.characters) for player in self.players}
        winner = max(player_scores, key=player_scores.get)
        print(f"\n{winner} wins the game with a total score of {player_scores[winner]} points!")



# cp = [character1, character2]

@app.route('/')
def index():
    return render_template('main.html', character_pool=character_pool, players=players)

@app.route('/bid_increase', methods=['POST'])
def submit_form():
    button_clicked = request.form.get('button_clicked') == 'True'

    # Now 'button_clicked' will be a boolean True if the button was clicked
    return f'Button Clicked: {button_clicked}'

# @app.route('/deduct_budget', methods=['POST'])
# def deduct_budget():
#     if request.method == 'POST':
#         player_index = request.form['player_index']
#         print(f'\n Player index is to find {player_index}\n')
#         player_index = int(player_index)
#         print(f'\n Player index is {player_index}\n')
#         players[player_index].deduct_budget(50)
#     return redirect(url_for('index'))

if __name__ == "__main__":
    player1 = Player("Waru", 100, "CSK.png")
    player2 = Player("Aru", 100, "SRH.png")
    players = [player1, player2]

    character_pool = CharacterPool()
    character1 = Character("Character 1", 6, "WK-Bater", "bastow.webp")
    character2 = Character("Character 2", 6, "Batter", "bastow.webp")
    character3 = Character("Character 3", 6, "Bowler", "bastow.webp")
    character4 = Character("Character 4", 6, "Bowling-Allrounder", "bastow.webp")
    character5 = Character("Character 5", 6, "Batting-Allrounder", "bastow.webp")
    character6 = Character("Character 6", 4, "Bolwer", "bastow.webp")
    # Add more characters to the pool

    character_pool.add_character(character1)
    character_pool.add_character(character2)
    character_pool.add_character(character3)
    character_pool.add_character(character4)
    character_pool.add_character(character5)
    character_pool.add_character(character6)
    # Add more characters to the pool
    random.shuffle(character_pool.characters)

    game_manager = GameManager(players, character_pool)


    print("""Game Rule:
          Each players has a budget of 1000 milion rupees to buy charecters.
          There is no limit on number of buy.
          You have to bid with other player to buy you charecter.
          The player win the bid take the ownership of the charecter.
          Then after the real match performance points own by each charecter will be computed.
          For each run charecter will gain 1 point.
          For each wicket charecter will win 30 point.
          For each catch charecter will gain 8 points.
          For each sump charecter will gain 8 points.
          The winner of this game will be decided by the total performance points gained by your charecters.
          The player with highest performance score will take the prize money.
    """)
    game_manager.start_game()
