# Salsa Engine
# Author: Craig Fritz

# Description: This program uses the simulated evolution algorithm (genetic algorithm) to generate a list of salsas that
# are tailored to the user's tastes.

# Copyright (C) 2020 Craig Fritz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Files:
# salsa_array.txt:        contains the current salsa population
# salsa_hashmap.txt:      contains all scored salsas and their scores
# salsa_leaderboard.txt:  contains best salsas found so far

from enum import Enum
from random import randrange
from random import random
from os import path
import jsonpickle

# CONTROL VARIABLES
population = 10               # number of salsas per generation
mutation_rate = 0.2           # chance a trait will mutate, >=1 means all traits always mutate, <=0 means never mutate
leaderboard_size = 10         # number of best salsas to save


# INGREDIENT LIST ENUMS
class Bases(Enum):
    TOMATO = 0
    TOMATILLO = 1
    PEACH = 2
    MANGO = 3
    NECTARINE = 4
    PINEAPPLE = 5
    PAPAYA = 6
    BLACKBERRIES = 7
    BLUEBERRIES = 8
    STRAWBERRIES = 9
    RASPBERRIES = 10
    JICAMA = 11
    # CRANBERRIES = 12

class Peppers(Enum):
    JALAPENO = 0
    SERRANO = 1
    HABANERO = 2
    CHIPOTLE = 3
    ARBOL = 4
    CASCABEL = 5
    FRESNO = 6
    THAI = 7


class Herbs(Enum):
    CILANTRO = 0
    MINT = 1
    PARSLEY = 2
    TARRAGON = 3
    BASIL = 4


class Methods(Enum):
    BLENDER = 0
    CHOP = 1
    CHAR = 2


method_descriptions = {}
method_descriptions[Methods.BLENDER.name] = "10 minutes: Throw all your items into a blender"
method_descriptions[Methods.CHOP.name] = "20 minutes: Chop everything into cute little cubes for a pico be gallo vibe"
method_descriptions[Methods.CHAR.name] = "30 minutes: Char everything but the herbs on a grill or broiler to maximize smoky flavors, then toss it all in the blender"


# SALSA CLASS ##########################################################################################################
class Salsa:
    # creates a salsa with the first ingredient from each list
    def __init__(self):
        self.base = []
        for i in range(0, 3):
            self.base.append(Bases.TOMATO)
        self.pepper = Peppers.JALAPENO
        self.herb = Herbs.CILANTRO
        self.method = Methods.BLENDER
        self.score = 0

    # sets all ingredients to a random member of their respective lists
    def randomize(self):
        for i in range(0, 3):
            self.base[i] = Bases(randrange(len(Bases)))
        self.pepper = Peppers(randrange(len(Peppers)))
        self.herb = Herbs(randrange(len(Herbs)))
        self.method = Methods(randrange(len(Methods)))
        self.base.sort(key=lambda x: x.value)

    def print(self):
        print("Ingredients:", self.base[0].name, self.base[1].name, self.base[2].name, self.pepper.name, self.herb.name, "\nCook method:", method_descriptions[self.method.name])

    def print_score(self):
        print("Score: ", self.score)

    # comparator function
    def equals(self, other_salsa):
        if self.base[0] == other_salsa.base[0] and self.base[1] == other_salsa.base[1] and self.base[2] == other_salsa.base[2] and self.pepper == other_salsa.pepper and self.herb == other_salsa.herb and self.method == other_salsa.method:
            return True
        else:
            return False

    def hash_ingredients(self):
        result = self.base[0].name + self.base[1].name + self.base[2].name + self.pepper.name + self.herb.name + self.method.name
        return result


# OTHER FUNCTIONS ######################################################################################################
def save_to_file(data, file):
    fo = open(file, "w")
    data_json = jsonpickle.encode(data)
    fo.write(data_json)
    fo.close()


def load_from_file(file):
    fo = open(file, "r")
    data_json = fo.read()
    data = jsonpickle.decode(data_json)
    fo.close()
    return data


def random_wrapper():
    return random()


def random_wrapper(seed):
    return seed


# MENU FUNCTIONS #######################################################################################################
def rate_salsa():
    # MAIN
    salsa_list = []
    if path.exists("salsa_array.txt"):
        salsa_list = load_from_file("salsa_array.txt")
    # else generate random salsas for salsa array
    else:
        for i in range(0, population):
            salsa = Salsa()
            salsa.randomize()
            salsa_list.append(salsa)

    if path.exists("salsa_hashmap.txt"):
        salsa_hashmap = load_from_file("salsa_hashmap.txt")
    else:
        salsa_hashmap = {}

    for salsa in salsa_list:
        if salsa.score == 0:
            if salsa.hash_ingredients() in salsa_hashmap:
                # notify of repeat salsa
                print("Duplicate salsa detected: ")
                salsa.print()
                print("Previously scored: ", salsa_hashmap[salsa.hash_ingredients()])
                print("Please use the rescore option in the menu if you'd like to update this score")
                # load its score into array
                salsa.score = salsa_hashmap[salsa.hash_ingredients()]
                continue

            salsa.print()
            score = int(input("Enter a score for this salsa (enter 0 to come back later): "))
            salsa.score = score
            save_to_file(salsa_list, "salsa_array.txt")

            # add score to salsa hashmap
            if not salsa.score == 0:
                salsa_hashmap[salsa.hash_ingredients()] = salsa.score
                save_to_file(salsa_hashmap, "salsa_hashmap.txt")

            return

    # if no highscore file create dummy file
    if not path.exists("salsa_leaderboard.txt"):
        salsa_leaderboard = []
        for i in range(0, leaderboard_size):
            salsa = Salsa()
            salsa_leaderboard.append(salsa)

        save_to_file(salsa_leaderboard, "salsa_leaderboard.txt")

    salsa_leaderboard = load_from_file("salsa_leaderboard.txt")

    # update highscore array
    for salsa in salsa_list:
        salsa_leaderboard.append(salsa)
    salsa_leaderboard.sort(key=lambda x: x.score, reverse=True)
    salsa_leaderboard = salsa_leaderboard[0:leaderboard_size]

    # print highscores
    for salsa in salsa_leaderboard:
        print("Highscores:")
        salsa.print()
        salsa.print_score()
    save_to_file(salsa_leaderboard, "salsa_leaderboard.txt")

    total_score_sum = 0
    for salsa in salsa_list:
        total_score_sum += salsa.score

    new_salsa_list = []
    for i in range(0, population):
        # init
        salsa = Salsa()
        new_salsa_list.append(salsa)

        # parent selection
        current_score_sum = 0
        for salsa in salsa_list:
            current_score_sum += salsa.score
            if random_wrapper() < (current_score_sum / total_score_sum):
                parent1 = salsa
                break

        current_score_sum = 0
        for salsa in salsa_list:
            current_score_sum += salsa.score
            if random_wrapper() < (current_score_sum / total_score_sum):
                if parent1.equals(salsa):
                    continue
                parent2 = salsa
                break

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].base[0] = parent1.base[0]
        else:
            new_salsa_list[i].base[0] = parent2.base[0]
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].base[0] = Bases(randrange(len(Bases)))

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].base[1] = parent1.base[1]
        else:
            new_salsa_list[i].base[1] = parent2.base[1]
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].base[1] = Bases(randrange(len(Bases)))

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].base[2] = parent1.base[2]
        else:
            new_salsa_list[i].base[2] = parent2.base[2]
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].base[2] = Bases(randrange(len(Bases)))

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].pepper = parent1.pepper
        else:
            new_salsa_list[i].pepper = parent2.pepper
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].pepper = Peppers(randrange(len(Peppers)))

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].herb = parent1.herb
        else:
            new_salsa_list[i].herb = parent2.herb
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].herb = Herbs(randrange(len(Herbs)))

        # crossover
        if random_wrapper() < 0.5:
            new_salsa_list[i].method = parent1.method
        else:
            new_salsa_list[i].method = parent2.method
        # mutation
        if random_wrapper() < mutation_rate:
            new_salsa_list[i].method = Methods(randrange(len(Methods)))

        # sort bases
        new_salsa_list[i].base.sort(key=lambda x: x.value)

    salsa_list = new_salsa_list
    save_to_file(salsa_list, "salsa_array.txt")

    print("new generation created")


def view_leaderboard():
    # if no highscore file create dummy file
    if not path.exists("salsa_leaderboard.txt"):
        salsa_leaderboard = []
        for i in range(0, leaderboard_size):
            salsa = Salsa()
            salsa_leaderboard.append(salsa)
        save_to_file(salsa_leaderboard, "salsa_leaderboard.txt")

    salsa_leaderboard = load_from_file("salsa_leaderboard.txt")

    # print highscore file
    for salsa in salsa_leaderboard:
        salsa.print()
        salsa.print_score()
        print("")


def change_score():
    print("Operation not yet supported")
    return


def modify_salsa():
    print("Operation not yet supported")
    return


# MAIN ########################################################################
master_loop = True
while master_loop:
    print('')
    print("Salsa Engine V2")
    print("1) View and rate salsa")
    print("2) View leaderboard")
    print("3) Change score")
    print("4) Modify salsa")
    print("0) exit")
    selection = input("Enter the number corresponding to your selection: ")
    if selection == '1':
        rate_salsa()
    elif selection == '2':
        view_leaderboard()
    elif selection == '3':
        change_score()
    elif selection == '4':
        modify_salsa()
    elif selection == '0':
        master_loop = False
    else:
        print("Invalid selection.  Type 0 to exit.")
