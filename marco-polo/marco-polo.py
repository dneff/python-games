#!/usr/bin/python
import sys, time, random, bisect
from helper import *

sys.stdout.flush()

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
        self.desert = False
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
        hunting_init(self)
        supplies_init(self)

def intro():
    print("WELCOME\n".center(80))

def traveler_barter(t):
    """barter for supplies"""
    barter = verify_input("You have {} jewels. Do you want to barter here? [y/n] ".format(t.jewels), 'str')

    if verify_yes_no(barter) == 'n':
        return

    camel_price   = random.randint(1,8) + 17
    food_price    = random.randint(1,4) + 2
    oil_price     = random.randint(1,4) + 2
    clothes_price = random.randint(1,8) + 8
    balm_price    = 2
    arrow_count   = random.randint(1,6) + 6

    print("Camels cost {} jewels here".format(camel_price))
    p = verify_input("How many do you want?", 'int')
    camels = verify_range(0,t.jewels//camel_price, p)
    t.beasts += camels
    t.jewels -= camel_price * camels
    t.beast_capacity += camels
    t.beast_quality -= camels

    shopping = True
    print("Sacks of food cost {} jewels.".format(food_price))
    while shopping:
        p = verify_input("How many do you want?",'int')
        food = verify_range(0,t.jewels//food_price, p)
        if t.food + food + t.oil > t.beast_capacity * 3:
            print("Your camels can't carry that much.")
        else:
            t.food += food
            t.jewels -= food_price * food
            shopping = False

    shopping = True
    print("Skins of oil cost {} jewels.".format(oil_price))
    while shopping:
        p = verify_input("How many do you want?", 'int')
        oil = verify_range(0,t.jewels//oil_price, p)
        if t.oil + oil + t.food > t.beast_capacity * 3:
            print("Your camels can't carry that much.")
        else:
            t.oil += oil
            t.jewels -= oil_price * oil
            shopping = False

    print("Clothing costs {} jewels each.".format(clothes_price))
    p = verify_input("How many do you want?", 'int')
    clothes = verify_range(0,t.jewels//clothes_price, p)
    t.clothes += clothes
    t.jewels -= clothes * clothes_price

    print("Healing balms are {} jewels.".format(balm_price))
    p = verify_input("How many do you want?", 'int')
    medicine = verify_range(0,t.jewels//balm_price, p)
    t.medicines += medicine
    t.jewels -= medicine * balm_price

    print("You can get {} arrows for 1 jewel.".format(arrow_count))
    p = verify_input("How many jewels do you want to spend?", 'int')
    arrows = verify_range(0,t.jewels, p) * arrow_count
    t.jewels -= p
    t.weapons += arrows

    print("Here is what you now have:")
    resource_print(t)

def traveler_eat(t):
    """wherein the traveler consumes foodstuffs"""
    if t.food < 3:
        traveler_starve(t)
        return
    eating = True
    while eating:
        print("On the next stage of your journey, how do you want to eat:")
        print("\t 1: Reasonably well")
        print("\t 2: Adequately")
        print("\t 3: Poorly")
        eaten = verify_input("?", 'int')
        eaten = verify_range(1,3,eaten)
        eaten = 6 - eaten
        if t.food < eaten:
            print("You don't have enough food to eat that well. Try again.")
            continue
        food_reserve = t.food - eaten
        if food_reserve < 3:
            print("if you eat this much, you'll only have {} sack of food left.".format(food_reserve))
            a = verify_input("Are you sure?", 'str')
            if verify_yes_no(a) == 'n':
                continue
        t.food -= eaten
        t.distance -= (eaten - 1) * 50
        t.food_quality = t.food_eaten_last + eaten
        t.food_eaten_last = eaten

        eating = False

def traveler_starve(t):
    """out of food"""
    print("You don't have enough food to go on.")
    if t.jewels < 15:
        if t.camels > 0:
            a = verify_input("Do you want to eat a camel?", 'str')
            if verify_yes_no(a) == 'y':
                t.beasts -= 1
                corpse = random.randint(3,5)
                t.food += corpse
                print("You manage to get about {} sacks out of it.".format(corpse))
        else:
            print("You don't even have a camel left to eat.")
    else:
        print("You should have bought food at the market. Now it will cost you.")
        food_price = random.randint(5,9)
        print("The price is {} per sack".format(food_price))
        count = verify_input("How many sacks do you want? ", 'int')
        count = verify_range(0, t.jewels//food_price, count)
        t.food += count
        t.jewels -= food_price * count

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
    count = random.randint(1,3)
    if t.medicines > count:
        print("You use {} bottles of balm to heal your wounds.".format(count))
        t.medicines -= count
        return
    else:
        count -= t.medicines
        t.medicines = 0
        print("You need more balm to heal your wounds.")
        print("Fortunately, you find some nomads willing to sell you")
        print("Two bottles for 4 jewels each.")
        if t.jewels > 8:
            purchase = verify_input("Do you agree to buy them?", 'str')
            purchase = verify_yes_no(purchase)
            if purchase == 'y':
                print("It works well and you're soon feeling better.")
                t.jewels -= 8
                t.medicines = 0
                return
        else:
            print("Alas you don't have enough jewels to buy them.")
    print("Your wound is badly infected.")
    if(random.randint(1,100) <= 80):
        print("but you push on to the next village.")
    else:
        print("but you keep going away.")
        print("unfortunately, the strain is too much for you and, after weeks")
        print("of agony, you succumb to your wounds and die in the wilderness.")
        end_status(t)

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
    months = ['March','May','July','September','November','January']
    year = 1271 + t.journey//6
    month = months[t.journey % 6]
    print("Date: {} {}".format(month, year))

def traveler_shoot(t):
    """shoot the crossbow"""
    shooting_words = ["BANG", "POW", "THWACK", "ZING"]
    word = shooting_words[random.randint(0,len(shooting_words) - 1)]
    start = time.clock()
    hit = False
    while hit == False:
        shot = verify_input("Type this word: {} :".format(word), 'str')
        if shot.upper() == word:
            hit = True
        else:
            print("That's not it, try again.")
    return int(time.clock() - start)

def traveler_hunt(t):
    """let's go a-hunting"""
    prey = ["wild boar", "big stag", "black bear"]
    bagged = 0
    if t.weapons < 15:
        print("You don't have enough arrows to hunt for food.")
        return
    print("There goes a {} ...".format(prey[random.randint(0,2)]))
    t.weapons -= 15
    shoot = traveler_shoot(t)
    if shoot <= 1:
        print("With shooting that good, the Khan will want you in his army!")
        bagged += 3
    elif shoot <= 3:
        print("Not bad; You finally brought one down.")
        bagged += 2
    else:
        print("Were you too excited? All your shots went wild.")
    print("You bagged {} bags of food.".format(bagged))

def events(t):
    """special events"""    
    event_probabilities = [6,4,4,6,18,10,6,6,6,4,4,1,6,8]    
    event_odds = [sum(event_probabilities[0:x]) for x in range(0,len(event_probabilities))]
    event_odds.sort()
    map_events = ['camel_hurt','camel_sick', 'camel_wander', 'bad_water','lost', 'rains', 'food_rotten', 'food_stolen', 'fire', 'burn', 'storms','infection', 'clothing_tear', 'sick', 'bandits']
    event = map_events[bisect.bisect(event_odds, random.randint(1,100))]
    if event == 'camel_hurt':
        print("A camel injured its leg.")
        camel_eval(t)
    elif event == 'camel_sick':
        print("One of your camels is very sick and can't carry its full load.")
        camel_eval(t)
    elif event == 'camel_wander':
        print("Two camels wander off. You finally find them after several days.")
        t.distance -= 20
    elif event == 'bad_water':
        print("Long stretch with bad water. You spend time looking for clean wells.")
        t.distance -= 50
    elif event == 'lost':
        print("You get lost trying to find an easier route.")
        t.distance -= 100
    elif event == 'rains':
        print("Heavy rains completely wash away the route.")
        t.distance -= 90
    elif event == 'food_rotten' and t.desert == False:
        print("Some of your food rots in humid weather.")
        t.food -= 1
    elif event == 'food_stolen':
        print("Marauding animals got into your food supply.")
        t.food -= 1
    elif event == 'fire':
        print("A fire flares up and destroys some of your food and clothes.")
        t.food -= 1
        t.clothes -= 1
        if t.oil > 1:
            t.oil -= 1
    elif event == 'burn' and t.desert == True:
        print("You get a nasty burn from an oil fire.")
        t.wound = 5
    elif event == 'storms':
        print("High winds, sand storms and ferocious heat slow you down.")
        t.distance -= 70
    elif event == 'infection':
        print("A gash in your leg looks infected. It hurts like the blazes.")
        t.wound = .5
        traveler_heal(t)
    elif event == 'clothing_tear':
        print("Jagged rocks tear your sandals and clothing. You'll need replacements soon.")
        t.clothes -= 1
        t.distance -= 30
    elif event == 'sick':
        print("All of you have horrible stomach cramps and intestinal disorder.")
        t.distance -= 275
    elif event == 'bandits':
        print("Bloodthirsty bandits are attacking your caravan!")
        bandits_eval(t)

def camel_eval(t):
    print("Do you want to:")
    print("\t1: Nurse it along")
    print("\t2: Abandon it")
    print("\t3: Sell it")
    fate = verify_input("?", 'int')
    fate = verify_range(1,3,fate)
    if fate == 1:
        t.beast_sick = t.journey + 2
    elif fate == 2:
        print("You kill the camel for food.")
        t.beasts -= 1
        t.food += 3
        t.beast_capacity = 3 * t.beast_load - t.food - t.oil
        print("You get the equivalent of 3 sacks of food.")
    elif fate == 3:
        t.beasts -= 1
        t.jewels += 10
        print("It is a poor beast and you only get 10 jewels for it.")
    # load check
    t.beast_load = t.beasts
    if t.beast_sick <= t.jewels:
        t.beast_load -= .6
        t.beast_quality -= 1
    if t.food + t.oil >= 3 * t.beast_load:
        print("You have too large a load for your animals.")
        excess = int(t.food + t.oil - 3 * t.beast_load - .9)
        while(excess > 0):
            print("You have to sell {} sacks of food or skins of oil.".format(excess))
            food_sell = random.randint(1,excess)
            oil_sell = excess - food_sell
            wages = food_sell * 3 + oil_sell * 5
            t.oil -= oil_sell
            t.food -= food_sell
            t.jewels += wages
            print("You made {} from selling {} sacks of food and {} skins of oil.".format(wages, food_sell, oil_sell))
            excess = int(t.food + t.oil - 3 * t.beast_load - .9)
                            
def bandits_eval(t):
    print("You grab your crossbow...")
    fatal = False
    if t.weapons < 5:
        print("You try to drive them off, but you run out of arrows.")
        print("They grab some jewels and food.")
        t.food -= 1
        fatal = True
    else:
        shot = traveler_shoot(t)
        if shot <= 1:
            print("Wow! Sensational shooting!")
        elif shot <= 3:
            print("With practice you could shoot the crossbow, but most of your")
            print("shots missed. An iron mace got you in the chest. They took some jewels.")
            t.wound = 1
            t.jewels -= 5
            traveler_heal(t)
            t.weapons -= 3 + 2 * t.hunting
            resource_verify(t)
            return
        else:
            print("Better stick to trading. Your aim is terrible.")
            fatal = True
    if fatal == True:
        if random.randint(1,100) > 20:
            print("You caught a knife to the shoulder. That's going to take")
            print("quite a while to heal.")
            traveler_heal(t)
            t.wound = 2
            t.jewels -= 10
            t.weapons -= 4 + 2 * t.hunting
        else:
            print("They are savage, evil barbarians. They kill you and take")
            print("your remaining camels and jewels.")
            t.jewels = 0
            t.beasts = 0
            end_status(t)
    
def desert(t):
    """in the desert?"""
    t.desert == True
    if t.distance < 2100 or t.distance > 5900:
        t.desert = False
        return
    if t.distance > 2600 and t.distance < 4100:
        t.desert = False
        return
    if t.distance > 4600 and t.distance < 5400:
        t.desert = False
        return

    d_name = ''
    if t.distance < 4100:
        d_name = "Dasht-e-Kavir (Persian)"
    elif t.distance > 5399:
        d_name = "Gobi (Cathay)"
    else:
        d_name = "Taklimakan (Lop)"

    print("You are in the {} desert.".format(d_name))

    if t.oil >= 3:
        t.oil -= 3
        print("Use 3 skins of oil for cooking.")
    else:
        print("You ran out of oil for cooking.")
        if t.oil > 1:
            t.oil -= random.randint(0, t.oil)
    if random.randint(1, 100) < 25:
        print("You get horribly sick from eating raw and undercooked food.")
        t.oil = 0
        t.health = 1
        t.distance -= 80
        t.medicines -= 1

    events(t)
    resource_rebase(t)

def end_status(t):
    t.journey += 1
    resource_rebase(t)
    date_print(t)
    if t.total_distance < 6000:
        print("Sorry you didn't make it.")
    else:
        print("Congratulations! You made it!")
    sys.exit(0)

def main():
    game = Traveler()

    intro()
    verify_continue()

    while game.total_distance < 6000:

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
        traveler_eat(game)

        # hunting check
        if random.randint(1,100) <= 18:
            traveler_hunt(game)

        # desert check
        desert(game)

        # event check
        if game.desert == False:
            events(game)

        # advance travel and print calendar
        game.journey += 1
        date_print(game)
        game.total_distance += game.distance
        game.distance += 40 + game.beast_quality * 20 + random.randint(0, 100)
        resource_rebase(game)
        print("You have traveled {} miles.".format(game.total_distance))

    end_status(game)

if __name__ == "__main__":
    main()
