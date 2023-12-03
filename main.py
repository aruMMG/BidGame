from flask import Flask, render_template, request, redirect, url_for, session
import random
from scraper import scaper

app = Flask(__name__)
app.secret_key = "hello"
# player.py
class Player:
    def __init__(self, idx, name, budget, image_path):
        self.id = idx
        self.name = name
        self.budget = budget
        self.image_path = image_path
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def deduct_budget(self, amount):
        self.budget -= amount

# character.py
class Character:
    def __init__(self, idx, name, base_price, role, image_path, owner="Un Sold"):
        self.id = idx
        self.name = name
        self.image_path = image_path
        self.base_price = base_price
        self.sold_price = None
        self.current_price = base_price
        self.role = role
        self.owner = owner
        self.performance_points = 0

    def set_owner(self, player):
        self.owner = player.name
        self.sold_price = self.current_price

    def update_current_price(self):
        self.current_price+=0.5

    def update_performance_points(self, points):
        self.performance_points += points

# character_pool.py

class CharacterPool:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

def start_bidding(character, players):
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




def calculate_points(batters_scores, bowlers_wickets):
    # runs = int(input(f"Run scored by {character.name}: "))
    # wickets = int(input(f"Wicket taken by {character.name}: "))
    # catches = int(input(f"Catch taken by {character.name}: "))
    # stumps = int(input(f"Stump by {character.name}: "))
    # performance_points = runs + wickets*30 + catches*8 + stumps*8
    # character.update_performance_points(performance_points)
    player_points = {}
    for name in set(batters_scores.keys()) | set(bowlers_wickets.keys()):
        value1 = batters_scores.get(name, 0)
        value2 = bowlers_wickets.get(name, 0)

        if name in batters_scores and name in bowlers_wickets:
            player_points[name] = value1 + (25 * value2)
        elif name in batters_scores:
            player_points[name] = value1
        elif name in bowlers_wickets:
            player_points[name] = 25 * value2

    return player_points
@app.route('/')
def enter_game():
    return render_template('enter_game.html')

@app.route('/start', methods=['POST'])
def index():
    print("it started +++++++++++++++++++")
    player0_name = request.form.get("player0_name")
    player1_name = request.form.get("player1_name")
    players[0].name = player0_name
    players[1].name = player1_name
    return render_template('main.html', character_pool=character_pool, players=players, bid_charecter=None)

@app.route('/bid_increase', methods=['POST'])
def bid_increase():
    button_clicked = request.form.get('button_clicked') == 'True'
    player_id = int(request.form.get('player_id'))
    print(f"bidder name {player_id}")
    bid_charecter_id = int(request.form.get('bid_charecter_id'))
    for character in character_pool.characters:
        if character.id == bid_charecter_id:
            bid_charecter = character
    for player in players:
        if player.id == player_id:
            bid_charecter.current_price += 0.5 
            sold_price = bid_charecter.current_price
            p_id = int((player.id+1)%len(players))
            print(f"other bidder name {p_id}")
            other_bidder = players[(player.id+1)%len(players)]
            print(f"other bidder name {other_bidder.name}")
            
            if other_bidder.budget < sold_price:
                player.add_character(bid_charecter)
                player.deduct_budget(sold_price)
                bid_charecter.set_owner(player)
                # bid_charecter = player.characters[-1]
                # print(f"{character.name}, sold to {bid_charecter.owner.name} at {sold_price} cr rupees.")
                print(f"{player.name} has a budget of {player.budget}")
                print(f"{player.name} has a budget of {player.budget}")
                
                message = f"{bid_charecter.name} is sold to {player.name} at {sold_price} cr rupees"
                # Change the return to render file to finsih the bit and continue fr other charecters        
                return render_template("bid_finish.html",  character_pool=character_pool, players=players, bid_charecter=bid_charecter, message=message)
    return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter=bid_charecter)

@app.route('/bid_drop', methods=['POST'])
def bid_drop():
    button_clicked = request.form.get('button_clicked') == 'True'
    player_id = int(request.form.get('player_id'))
    print(f"widthdrawn bidder id {player_id}")
    bid_charecter_id = int(request.form.get('bid_charecter_id'))
    for character in character_pool.characters:
        if character.id == bid_charecter_id:
            bid_charecter = character
    for player in players:
        if player.id == player_id:
            sold_price = bid_charecter.current_price
            p_id = int((player.id+1)%len(players))
            print(f"other bidder name {p_id}")
            print(f"current sold price {sold_price}")
            other_bidder = players[(player.id+1)%len(players)]
            print(f"other bidder name {other_bidder.name}")
            
            other_bidder.add_character(bid_charecter)
            other_bidder.deduct_budget(sold_price)
            bid_charecter.set_owner(other_bidder)
            # bid_charecter = player.characters[-1]

            
            message = f"{bid_charecter.name} is sold to {other_bidder.name} at {sold_price} cr rupees"
            # Change the return to render file to finsih the bit and continue fr other charecters        
            return render_template("bid_finish.html",  character_pool=character_pool, players=players, bid_charecter=bid_charecter, message=message)
    return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter=bid_charecter)

@app.route('/bid_start_button', methods=['POST'])
def bid_start():
    print("in bid start button")
    print("=========================")
    button_clicked = request.form.get('button_clicked') == 'True'
    if button_clicked:
        for character in character_pool.characters:
            if character.owner=="Un Sold":
                session["current_charecter_id"] = character.id
                return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter=character)
    print("bid finished ============================")
    return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter="finished")

@app.route('/next_bid', methods=['POST'])
def next_bid():
    button_clicked = request.form.get('button_clicked') == 'True'
    bid_charecter_id = int(request.form.get('bid_charecter_id'))
    take_next = False
    if button_clicked:
        for character in character_pool.characters:
            if take_next:
                if character.owner=="Un Sold":
                    session["current_charecter_id"] = character.id
                    return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter=character)
            elif character.id == bid_charecter_id:
                take_next = True
            else:
                continue        
    print("bid finished ============================")
    return render_template("main.html",  character_pool=character_pool, players=players, bid_charecter="finished")

@app.route('/player_card')
def player_card():
    # Your code to render the player card template or return data goes here
    return render_template('player_card.html', character_pool=character_pool)

@app.route('/owner')
def owner():
    # Your code to render the player card template or return data goes here
    return render_template('owner.html', players=players, players_points=False)

@app.route('/process_url', methods=['POST'])
def process_url():
    # print("preocess url")
    url = request.form.get("url")
    batters_score, bowlers_wickets = scaper(url)
    players_points = calculate_points(batters_score, bowlers_wickets)

    return render_template('owner.html', players=players, players_points=players_points)

@app.route('/main')
def main():
    current_charecter_id = session.get('current_charecter_id')
#         players[player_index].deduct_budget(50)
#     return redirect(url_for('index'))

if __name__ == "__main__":
    player1 = Player(0, "Waru", 100, "CSK.png")
    player2 = Player(1, "Aru", 100, "SRH.png")
    players = [player1, player2]

    character_pool = CharacterPool()
    character0 = Character(0, "Shanto", 4, "Bater", "najmul-hossain-shanto.webp")
    character1 = Character(1, "Hridoy", 4, "Bater", "towhid-hridoy.webp")
    character2 = Character(2, "Tanzid", 4, "Batter", "tanzid-hasan.webp")
    character3 = Character(3, "Sakib", 6, "Allrounder", "shakib-al-hasan.webp")
    character4 = Character(4, "Mahedi", 2, "Allrounder", "mahedi-hasan.webp")
    character5 = Character(5, "Mahmudullah", 4, "Allrounder", "mahmudullah.webp")
    character6 = Character(6, "Mehidy Miraz", 6, "Allrounder", "mehidy-hasan-miraz.webp")
    character7 = Character(7, "Mushfiqur", 6, "WK-Bater", "mushfiqur-rahim.webp")
    character8 = Character(8, "Litton", 6, "WK-Bater", "litton-das.webp")
    character9 = Character(9, "Taskin", 4, "Bowler", "taskin-ahmed.webp")
    character10 = Character(10, "Mustafizur", 4, "Bowler", "mustafizur-rahman.webp")
    character11 = Character(11, "Hasan", 2, "Bowler", "hasan-mahmud.webp")
    character12 = Character(12, "Shoriful", 4, "Bowler", "shoriful-islam.webp")
    character13 = Character(13, "Nasum", 2, "Bowler", "nasum-ahmed.webp")
    character14 = Character(14, "Tanzim", 2, "Bowler", "tanzim-hasan-sakib.webp")
    # Add more characters to the pool

    Ind_character0 = Character(15, "Rohit", 6, "Bater", "rohit-sharma.webp")
    Ind_character1 = Character(16, "Gill", 6, "Bater", "shubman-gill.webp")
    Ind_character2 = Character(17, "Kohli", 6, "Batter", "virat-kohli.webp")
    Ind_character3 = Character(17, "Iyer", 6, "Batter", "shreyas-iyer.webp")
    Ind_character4 = Character(19, "Surya", 2, "Batter", "suryakumar-yadav.webp")
    Ind_character5 = Character(20, "Pandya", 6, "Allrounder", "hardik-pandya.webp")
    Ind_character6 = Character(21, "Jadeja", 6, "Allrounder", "ravindra-jadeja.webp")
    Ind_character7 = Character(22, "Ashwin", 4, "Allrounder", "ravichandran-ashwin.webp")
    Ind_character8 = Character(23, "Rahul", 6, "WK-Bater", "kl-rahul.webp")
    Ind_character9 = Character(24, "Ishan", 2, "WK-Bater", "ishan-kishan.webp")
    Ind_character10 = Character(25, "Sardul", 4, "Bowler", "shardul-thakur.webp")
    Ind_character11 = Character(26, "Bumrah", 6, "Bowler", "jasprit-bumrah.webp")
    Ind_character12 = Character(27, "Kuldeep", 6, "Bowler", "kuldeep-yadav.webp")
    Ind_character13 = Character(28, "Shami", 2, "Bowler", "mohammed-shami.webp")
    Ind_character14 = Character(29, "Siraj", 6, "Bowler", "mohammed-siraj.webp")


    character_pool.add_character(character0)
    character_pool.add_character(character1)
    character_pool.add_character(character2)
    character_pool.add_character(character3)
    character_pool.add_character(character4)
    character_pool.add_character(character5)
    character_pool.add_character(character6)
    character_pool.add_character(character7)
    character_pool.add_character(character8)
    character_pool.add_character(character9)
    character_pool.add_character(character10)
    character_pool.add_character(character11)
    character_pool.add_character(character12)
    character_pool.add_character(character13)
    character_pool.add_character(character14)
    character_pool.add_character(Ind_character0)
    character_pool.add_character(Ind_character1)
    character_pool.add_character(Ind_character2)
    character_pool.add_character(Ind_character3)
    character_pool.add_character(Ind_character4)
    character_pool.add_character(Ind_character5)
    character_pool.add_character(Ind_character6)
    character_pool.add_character(Ind_character7)
    character_pool.add_character(Ind_character8)
    character_pool.add_character(Ind_character9)
    character_pool.add_character(Ind_character10)
    character_pool.add_character(Ind_character11)
    character_pool.add_character(Ind_character12)
    character_pool.add_character(Ind_character13)
    character_pool.add_character(Ind_character14)
    # Add more characters to the pool
    random.shuffle(character_pool.characters)
    # bidding_engine = BiddingEngine()

    # game_manager = GameManager(players, character_pool)

    app.run(debug=True)

    # print("""Game Rule:
    #       Each players has a budget of 1000 milion rupees to buy charecters.
    #       There is no limit on number of buy.
    #       You have to bid with other player to buy you charecter.
    #       The player win the bid take the ownership of the charecter.
    #       Then after the real match performance points own by each charecter will be computed.
    #       For each run charecter will gain 1 point.
    #       For each wicket charecter will win 30 point.
    #       For each catch charecter will gain 8 points.
    #       For each sump charecter will gain 8 points.
    #       The winner of this game will be decided by the total performance points gained by your charecters.
    #       The player with highest performance score will take the prize money.
    # """)
    # game_manager.start_game()
