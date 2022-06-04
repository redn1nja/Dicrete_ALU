import numpy as np
import random
from person import Person
from time import sleep
from os import system, name


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

    def get_neighbours_affect(self, y, x):
        '''
        Checks all the neighbours and returns the delta
        of transition probability for the person at (y,x)

        If the person is fully surrounded by active ukrainians,
        the maximal delta for one step is +1.0, same goes with
        active prorussian with -1.0 per step.
        '''
        affect = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0)\
                        and len(self._grid) > y+i >= 0\
                        and len(self._grid[y+i]) > x+j >= 0\
                        and self._grid[y + i, x + j] and self._grid[y, x]:
                    if self._grid[y + i, x + j].state == Person.ACTIVE_UA:
                        affect += 0.125
                    elif self._grid[y + i, x + j].state == Person.PASSIVE_UA:
                        affect += 0.0625
                    elif self._grid[y + i, x + j].state == Person.PASSIVE_RU:
                        affect -= 0.0625
                    elif self._grid[y + i, x + j].state == Person.ACTIVE_RU:
                        affect -= 0.125
                    affect *= 1 + self.AUTHORITY_MATRIX[self._grid[y, x].age][self._grid[y+i, x+j].age]
        return affect

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
            moved = Person(self._grid[y, x].age, move, self._grid[y, x].state)
            moved.transition_prob = self._grid[y, x].transition_prob
            self._grid[move[0], move[1]] = moved
            self._grid[y, x] = None

    def evolve(self):
        '''
        Iterates over all the people in the system and changes their state
        according to the neighbours.
        '''
        for row in self._grid:
            for person in row:
                if person is not None:
                    person.transition_prob += \
                        self.get_neighbours_affect(*person.coordinates)

        for row in self._grid:
            for person in row:
                if person is not None:
                    prob = random.random()
                    person.change_state(prob)
                    prob = random.random()
                    if prob < 1/(2**(person.age+2)):
                        self.move(*person.coordinates)

    def __repr__(self):
        return "\n".join(" ".join(str(item) if
                                  item else "empt" for item in row) for row in self._grid)

    def get_grid(self):
        return self._grid


if __name__ == "__main__":
    a = CellularAutomaton(5, 2, 0.5, 0.5, 0.2, 0.7)
    for i in range(120):
        system("cls" if name == "nt" else "clear")
        print(a)
        a.evolve()
        sleep(0.2)
