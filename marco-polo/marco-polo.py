#!/usr/bin/python

class Traveler(object):
    """Represents user"""
    def __init__(self, jewels=300, clothes=2, weapons=30, medicines=5, beast_sick=99,hunting_skill=2):
        self.jewels = jewels
        self.clothes = clothes
        self.weapons = weapons
        self.medicines = medicines
        self.beast_sick = beast_sick
        self.hunting_skill = hunting_skill

def getHuntingSkill(t):
    skill = 0
    while(skill == 0):
        print("Before you begin your journey, please rank your skill with the crossbow with the crossbow:")
        print("    (1) Can hit a charging deer at 300 paces")
        print("    (2) Can hit a deer at 50 paces")
        print("    (3) Can hit a sleeping squirrel at 5 paces")
        print("    (4) Can hit your foot if lucky")
    skill = int(input("How do you rank yourself?"))
    if skill < 1 or skill > 4:
        skill = 0
    t.hunting_skill = skill
    return

def getSupplies(t):



def main():
    pass


if __name__ == "__main__":
    main()
