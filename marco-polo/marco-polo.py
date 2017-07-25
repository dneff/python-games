#!/usr/bin/python
import sys
sys.stdout.flush()

import random

event_probabilities = [6,4,4,6,6,6,6,4,4,1,6,8,18,10]
months = ['March','May','July','September','November','January']

class Traveler(object):
    """Represents user"""
    def __init__(self,
                 jewels=300,
                 food=0,
                 oil=0,
                 clothes=2, 
                 weapons=30, 
                 medicines=5,
                 beasts=0,
                 beast_quality=0,
                 beast_load=0,
                 beast_capacity=0,
                 beast_sick=99,
                 hunting=2):
        
        self.journey = 0
        self.distance = 0
        self.total_distance = 0
        self.food_status = 0
        self.food_eaten = 0
        self.food_eaten_last = 0
        self.food_quality = 0
        self.jewels = jewels
        self.food = food
        self.oil = oil
        self.clothes = clothes
        self.naked = False
        self.weapons = weapons
        self.medicines = medicines
        self.beasts = 0
        self.beast_quality = beast_quality
        self.beast_load = beast_load
        self.beast_capacity = beast_capacity        
        self.beast_sick = beast_sick
        self.hunting = hunting
        self.health = 0
        self.health_total = 0
        self.wound = 0
        self.wound_total = 0
     
def intro():
    print("WELCOME\n".center(80))

def hunting_init(t):
    """iniitialize hunting skill"""
    print("HUNTING".center(80))
    print("Before you begin your journey, please rate your skill with the crossbow with the crossbow:")
    print("    (1) Can hit a charging deer at 300 paces")
    print("    (2) Can hit a deer at 50 paces")
    print("    (3) Can hit a sleeping squirrel at 5 paces")
    print("    (4) Can hit your foot if lucky")
    skill = int(input("How do you rate yourself? "))
    skill = verify_range(1,4,skill)
    t.hunting = skill

def supplies_init(t):
    """get initial supplies"""
    print("SUPPLIES".center(80))
    print("After three months at sea, you arrived at the seaport of Laissus,")
    print("Armenia. There are many merchants in the port city and you can")
    print("easily get all the supplies you need.")

    print("Several traders offer you camels at prices between {} and {} each.".format(17, 24))
    camel_price = int(input("How much do you want to pay for a camel? "))
    camel_price = verify_range(17, 24, camel_price)
    t.beast_quality = camel_price
    
    print("You will need at least 7 camels but no more than 12.")
    camel_count = int(input("How many camels do you want? "))
    camel_count = verify_range(7, 12, camel_count)
    t.beasts += camel_count
    t.jewels -= camel_price * camel_count
    t.beast_capacity = 3 * t.beasts - 6
    
    print("\nOne large sack of food costs 2 jewels. You will need at least")
    print("8 sacks to get to Babylon (Baghdad).")
    print("You can carry a max of {} sacks.".format(t.beast_capacity))
    food = int(input("How many sacks of food do you want? "))
    food = verify_range(8, t.beast_capacity, food)
    t.food = food
    t.jewels -= food * 2
    t.beast_load = food
    
    print("\nA skin of oil costs 2 jewels. You should have at least")
    print("6 full skins for cooking in the desert.")
    print("Your camels can carry {} skins.".format(t.beast_capacity - t.beast_load))
    oil = int(input("How many skins of oil do you want? "))
    oil = verify_range(5, t.beast_capacity - t.beast_load, oil)
    t.oil = oil
    t.jewels -= oil * 2
    t.beast_capacity -= oil

def traveler_sick(t):
    """deal with sickness"""
    pass

def traveler_barter(t):
    """barter for supplies"""
    barter = input("You have {} jewels. Do you want to barter here? [y/n] ".format(t.jewels))
    if verify_yes_no(barter) == 'y':
        camel_price   = random.randint(1,8) + 17
        food_price    = random.randint(1,4) + 2
        oil_price     = random.randint(1,4) + 2
        clothes_price = random.randint(1,8) + 8
        balm_price    = 2
        arrow_count   = random.randint(1,6) + 6

    
def traveler_eat(t):
    """wherein the traveler consumes foodstuffs"""
    pass

def traveler_naked(t):
    """out of clothes"""
    print("You were warned about getting more modest clothes.")
    print("Futhermore, your sandals are in shreds.")
    if t.naked:
        print("Word has been received about your disreputable appearance.")
        print("The people are not willing to deal with you and they")
    else:
        print("The Tartars chase you from town and")
        
    if random.randint(1,100) > 20:
        print("warn you not to return...")
        t.naked = True
    else:
        print("stone you. You are badly wounded and vow to get new")
        print("clothes as soon as possible.")
        t.naked = True
        t.wound = 1.5
        
def traveler_heal(t):
    """deal with medicine"""
    pass

def resource_rebase(t):
    """ensure resources can't be negative"""
    pass

def resource_verify(t):
    """check for being out of jewels/clothes"""
    if t.jewels < 15:
        print("You have only {} jewels with which to barter.".output(t.jewels))
        
    if t.beasts < 3:
        print("You push on with your {} camels.".output(t.beasts))
    else:
        a = raw_input("Would you like to sell a camel? [y/n] ")
        if verify_yes_no(a) == 'y':
            sale = 8 + random.randint(1,9)
            print("You get {} jewels for your best camel.".format(sale))
            t.jewels += sale
            t.beasts -= 1

    if t.clothes < 1:
        print("You should try and replace that tent you have been wearing as a")
        print("robe. It is badly torn and the Tartars find it insulting.")
        

def resource_print(t):
    """print inventory"""
    headers1 = ["Sacks of", "", "", "Skins of", "Robes and", "Balms and", "Crossbow"]
    headers2 = ["Jewels", "Camels", "Food", "Oil", "Sandals", "Unguents", "Arrows"]
    inventory = [t.jewels, t.beasts, t.food, t.oil, t.clothes, t.medicines, t.weapons]
    row_format ="{:<12}" * (len(headers1) + 1)
    print row_format.format("", *headers1)
    print row_format.format("", *headers2)
    print row_format.format("", *inventory)

def sick_verify(t):
    t.health_total += t.health
    t.health = 0
    t.wound_total += t.wound
    t.wound = 0
    if t.food_eaten == 3:
        t.food_status += .4
    if t.health_total + t.wound_total + t.food_status < 3: return
    if random.randint(1,100) > 70: return
    print("As a result of sickness, injuries, and poor eating, you  must stop")
    print("and regain your health. You trade a few tools to stay in a hut.")
    lag = random.randint(1,100) % 6
    if lag > 5:
        print("You stay for {} months but grow weaker and finally pass away.".format(lag))
        t.journey += lag
        end_status(t)
    print("You grow steadily stronger, but it is {} months until you are".format(lag * 2))
    print("again fit to travel.")
    t.health_total = 0
    t.wound_total = 0
    t.food_status = 0
    t.journey += lag
    t.medicines = t.medicines//2
    t.food = t.food//2
    if t.food < 3:
        t.food = 3
    if t.jewels > 20:
        t.jewels -= 10
    else:
        t.jewels = t.jewels//2

def date_print(t):
    """print date"""
    year = 1271 + t.journey//6
    month = months[t.journey % 6]
    print("Date: {} {}".format(month, year))

def event_check():
    """read event probabilities"""
    pass

def traveler_shoot(t):
    """shoot the crossbow"""
    pass

def events(t):
    """special events"""
    pass

def verify_yes_no(answer):
    answers = ['y','n','yes','no']
    while (answer.lower() not in answers):
        answer = input("Don't understand answer. Enter y/n please:")
    return answer[0].lower()

def verify_range(min, max, answer):
    response = ''
    while (min > answer or max < answer):
        if answer < min:
            response = 'few'
        else:
            response = 'many'
        answer = int(input("That is too {}. Try again:".format(response)))
    return answer

def verify_continue():
    raw_input("\nPress ENTER to continue...")
    pass


def end_status():
    pass

def main():
    game = Traveler()
    
    intro()
    verify_continue()
    
    hunting_init(game)
    supplies_init(game)
    while(game.total_distance < 6000):       
        # advance travel and print calendar
        game.journey += 1
        date_print(game)
        game.total_distance += game.distance
        game.distance += 40 + game.beast_quality * 20 + random.randint(0,100)
        print("You have traveled {} miles.".format(game.total_distance))
        
        # print inventory
        print("Here is what you now have:\n")
        resource_print(game)
        verify_continue()
        
        # check for no jewels/clothes
        resource_verify(game)
        
        # check for sickness
        sick_verify(game)
        
        # recover camels
        if game.beast_sick == game.journey:
            game.beast_sick = 99
            game.beast_load = game.beasts
            game.beast_quality += 1
        
        # barter for supplies
        if game.journey > 1 and game.jewels > 1:
            traveler_barter(game)
        
        # no clothes penalty
        if game.clothes < 0:
            traveler_naked(game)
            
        # eat
        
        # hunting check
        
        # desert check
        
        # event check
    

if __name__ == "__main__":
    main()
