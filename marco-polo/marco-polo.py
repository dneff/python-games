#!/usr/bin/python

import random

event_probabilities = [6,4,4,6,6,6,6,4,4,1,6,8,18,10]
months = ['March','May','July','September','November','January']

class Traveler(object):
    """Represents user"""
    def __init__(self,
                 journey=0,
                 distance=0,
                 total_distance=0,
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
        
        self.journey = journey
        self.distance = distance
        self.total_distance = total_distance
        self.jewels = jewels
        self.food = food
        self.oil = oil
        self.clothes = clothes
        self.weapons = weapons
        self.medicines = medicines
        self.beasts = beasts
        self.beast_quality = beast_quality
        self.beast_load = beast_load
        self.beast_capacity = beast_capacity        
        self.beast_sick = beast_sick
        self.hunting = hunting
     
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
    
def resource_check(t):
    """check for being out of jewels/clothes"""
    pass

def traveler_sick(t):
    """deal with sickness"""
    pass

def traveler_barter(t):
    """barter for supplies"""
    pass
    
def traveler_eat(t):
    """wherein the traveler consumes foodstuffs"""
    pass

def events(t):
    """special events"""
    pass

def traveler_heal(t):
    """deal with medicine"""
    pass

def resource_rebase(t):
    """ensure resources can't be negative"""
    pass

def resource_print(t):
    """print inventory"""
    pass

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

def verify_yes_no(answer):
    answers = ['y','n','yes','no']
    while (answer.lower() not in answers):
        answer = input("Don't understand answer. Enter y/n please:")

def verify_range(min, max, answer):
    response = ''
    while (min > answer or max < answer):
        if answer < min:
            response = 'few'
        else:
            response = 'many'
        answer = int(input("That is too {}. Try again:".format(response)))
    return answer


def end_status():
    pass

def main():
    game = Traveler()
    intro()
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
        print("Here is what you now have:")
        
        # check for no jewels/clothes
        
        # check for sickness
        
        # recover camels
        
        # barter for supplies
        
        # no clothes penalty
        
        # eat
        
        # hunting check
        
        # desert check
        
        # event check
    




if __name__ == "__main__":
    main()
