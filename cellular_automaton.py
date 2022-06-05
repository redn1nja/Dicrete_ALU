import numpy as np
import random
from person import Person


class CellularAutomaton:
    '''
    Class that represents a grid of people,
    who interact together and form a society.
    '''
    AUTHORITY_MATRIX = [[1, 0.5, 0.25],
                        [0.25, 0.5, 0.125],
                        [0.0625, 0.125, 0.25]]

    def __init__(self, width, height, ua_percentage, youth_percentage,
                 adult_percentage, fill):
        self.total_births = 0
        self.total_deaths = 0
        self._grid = np.array([[Person(self.generate_age(youth_percentage, adult_percentage),
                                       (j, i), self.generage_state(ua_percentage))
                               if random.random() <= fill else None
                               for i in range(width)] for j in range(height)])

    @staticmethod
    def generate_age(prob_y, prob_a):
        final_prob = random.random()
        if final_prob <= prob_y:
            return Person.YOUTH
        if prob_y < final_prob < prob_y+prob_a:
            return Person.ADULT
        return Person.SENIOR

    @staticmethod
    def generage_state(prob):
        states_ukr = [Person.ACTIVE_UA, Person.PASSIVE_UA, Person.SURZHYK]
        states_negative = [Person.SURZHYK, Person.PASSIVE_RU, Person.ACTIVE_RU]
        if random.random() <= prob:
            return random.choice(states_ukr)
        return random.choice(states_negative)

    def get_clear_surroundings(self, y, x):
        set_of_coords = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0)\
                        and len(self._grid) > y+i >= 0\
                        and len(self._grid[y+i]) > x+j >= 0:
                    if not self._grid[y+i, x+j]:
                        set_of_coords.add((y+i, x+j))
        return set_of_coords

    def get_neighbours_affect(self, y, x):
        '''
        Checks all the neighbours and returns the delta
        of transition probability for the person at (y,x)

        If the person is fully surrounded by active ukrainians,
        the maximal delta for one step is +1.0, same goes with
        active prorussian with -1.0 per step.
        '''
        affect = 0
        num_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0)\
                        and len(self._grid) > y+i >= 0\
                        and len(self._grid[y+i]) > x+j >= 0\
                        and self._grid[y + i, x + j] and self._grid[y, x]:
                    num_neighbors += 1

                    if self._grid[y + i, x + j].state == Person.ACTIVE_UA:
                        affect += 0.125
                    elif self._grid[y + i, x + j].state == Person.PASSIVE_UA:
                        affect += 0.0625
                    elif self._grid[y + i, x + j].state == Person.PASSIVE_RU:
                        affect -= 0.0625
                    elif self._grid[y + i, x + j].state == Person.ACTIVE_RU:
                        affect -= 0.125
                    affect *= (1 + self.AUTHORITY_MATRIX[self._grid[y, x].age_group][self._grid[y+i, x+j].age_group])
                    affect /= num_neighbors
                    self.marriage(y, y+i, x, x+j)
        return affect

    def marriage(self, y, y1, x, x1):
        lang_delta = abs(self._grid[y, x].state - self._grid[y1, x1].state)+1
        chance_to_pair = 1/(2**lang_delta)

        if random.random() < chance_to_pair and self._grid[y, x].age_group in [Person.ADULT, Person.SENIOR]\
                and self._grid[y1, x1].age_group in [Person.ADULT, Person.SENIOR]:

            if not self._grid[y, x].infamily and not self._grid[y1, x1].infamily:
                self._grid[y, x].infamily = True
                self._grid[y1, x1].infamily = True

                places_for_child = self.get_clear_surroundings(
                    y, x).intersection(self.get_clear_surroundings(y1, x1))

                if places_for_child:
                    child_lang = (
                        self._grid[y, x].state + self._grid[y1, x1].state)//2
                    place = random.choice(list(places_for_child))

                    self._grid[place[0], place[1]] = self.birth(
                        place[0], place[1], child_lang)

    def move(self, y, x):
        """
        moves the person at x, y to a nearby free cell
        """
        possible_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0)\
                        and len(self._grid) > y+i >= 0\
                        and len(self._grid[y+i]) > x+j >= 0\
                        and not self._grid[y + i, x + j]:
                    possible_moves.append((y+i, x+j))

        if possible_moves:
            move = random.choice(possible_moves)
            moved = Person(self._grid[y, x].age_group, move, self._grid[y, x].state)
            moved.transition_prob = self._grid[y, x].transition_prob
            moved.age = self._grid[y, x].age

            self._grid[move[0], move[1]] = moved
            self._grid[y, x] = None

    def evolve(self):
        '''
        Iterates over all the people in the system and changes their state
        according to the neighbours. Also making people on the grid older and
        simulates birth and death. 1 tick of evolve method means 1 year.
        '''
        death_prob_dict = {
            Person.YOUTH: 0.001,
            Person.ADULT: 0.005,
            Person.SENIOR: 0.01
        }

        for row in self._grid:
            for person in row:
                if person:
                    coords = person.get_coords()
                    y, x = coords[0], coords[1]

                    person.transition_prob += \
                        self.get_neighbours_affect(y, x)

                    person.age += 1

                    if 55 >= person.age >= 24:
                        person.age_group = Person.ADULT
                    elif 55 < person.age:
                        person.age_group = Person.SENIOR

                    death = random.random()

                    if death < death_prob_dict[person.age_group]:
                        self.death(y, x)

        for row in self._grid:
            for person in row:
                if person:
                    prob = random.random()
                    person.change_state(prob)

                    prob = random.random()
                    if prob < 1/(2**(person.age_group+2)):
                        self.move(*person.coordinates)

    def birth(self, y, x, parent_lang):
        """
        Create a new Person with the language of parents
        """
        # print(f"new person at {y, x}")
        self.total_births += 1
        return Person(Person.YOUTH, (y, x), parent_lang)

    def death(self, y, x):
        # print(f"death at {y, x}")
        self.total_deaths += 1
        self._grid[y, x] = None

    def get_ua_ru_percentage(self):
        total = 0
        ua = 0
        ru = 0
        for row in self._grid:
            for el in row:
                if el:
                    total += 1
                    if el.state in (3,4):
                        ua += 1
                    elif el.state in (0,1):
                        ru += 1
        return round(100 * ua/total, 2), round(100 * ru/total, 2)
                        

    def __repr__(self):
        return "\n".join(" ".join(str(item) if
                                  item else "empt" for item in row) for row in self._grid)

    def get_grid(self):
        return self._grid
