def verify_yes_no(answer):
    answers = ['y', 'n', 'yes', 'no']
    while answer.lower() not in answers:
        answer = verify_input("Don't understand answer. Enter y/n please:", 'str')
    return answer[0].lower()

def verify_range(min, max, answer):
    response = ''
    while min > answer or max < answer:
        if answer < min:
            response = 'few'
        else:
            response = 'many'
        answer = verify_input("That is too {}. Try again:".format(response), 'int')
    return answer

def verify_continue():
    raw_input("\nPress ENTER to continue...")

def verify_input(question, input_type):
    unknown = raw_input(question)
    verified = False
    while verified != True:
        test  =  ''
        try:
            unknown = int(unknown)
            test = 'int'
        except ValueError:
            test = 'str'

        if input_type == test:
            verified = True
        else:
            unknown = raw_input("I don't understand: ")
    return unknown

def hunting_init(t):
    """iniitialize hunting skill"""
    print("HUNTING".center(80))
    print("Before you begin your journey, please rate your skill with the crossbow with the crossbow:")
    print("    (1) Can hit a charging bear at 300 paces")
    print("    (2) Can hit a deer at 50 paces")
    print("    (3) Can hit a sleeping squirrel at 5 paces")
    print("    (4) Can hit your foot if lucky")
    skill = verify_input("How do you rate yourself? ", 'int')
    skill = verify_range(1, 4, skill)
    t.hunting = skill

def supplies_init(t):
    """get initial supplies"""
    print("SUPPLIES".center(80))
    print("After three months at sea, you arrived at the seaport of Laissus,")
    print("Armenia. There are many merchants in the port city and you can")
    print("easily get all the supplies you need.")

    print("Several traders offer you camels at prices between {} and {} each.".format(17, 24))
    camel_price = verify_input("How much do you want to pay for a camel? ",'int')
    camel_price = verify_range(17, 24, camel_price)
    t.beast_quality = camel_price

    print("You will need at least 7 camels but no more than 12.")
    camel_count = verify_input("How many camels do you want? ", 'int')
    camel_count = verify_range(7, 12, camel_count)
    t.beasts += camel_count
    t.jewels -= camel_price * camel_count
    t.beast_capacity = 3 * t.beasts - 6

    print("\nOne large sack of food costs 2 jewels. You will need at least")
    print("8 sacks to get to Babylon (Baghdad).")
    print("You can carry a max of {} sacks.".format(t.beast_capacity))
    food = verify_input("How many sacks of food do you want? ", 'int')
    food = verify_range(8, t.beast_capacity, food)
    t.food = food
    t.jewels -= food * 2
    t.beast_load = food

    print("\nA skin of oil costs 2 jewels. You should have at least")
    print("6 full skins for cooking in the desert.")
    print("Your camels can carry {} skins.".format(t.beast_capacity - t.beast_load))
    oil = verify_input("How many skins of oil do you want? ",'int')
    oil = verify_range(5, t.beast_capacity - t.beast_load, oil)
    t.oil = oil
    t.jewels -= oil * 2
    t.beast_capacity -= oil
    
def resource_rebase(t):
    """ensure resources can't be negative"""
    if t.jewels    < 0: t.jewels = 0
    if t.food      < 0: t.food = 0
    if t.oil       < 0: t.oil = 0
    if t.clothes   < 0: t.clothes = 0
    if t.medicines < 0: t.medicines = 0
    if t.weapons   < 0: t.weapons = 0
    if t.total_distance  < 0: t.total_distance = 0

def resource_verify(t):
    """check for being out of jewels/clothes"""
    if t.jewels < 15:
        print("You have only {} jewels with which to barter.".format(t.jewels))

    if t.beasts < 3:
        print("You push on with your {} camels.".format(t.beasts))
    else:
        a = verify_input("Would you like to sell a camel? [y/n] ", 'str')
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