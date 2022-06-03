import numpy as np
import random
from person import Person


class CellularAutomaton:
    '''
    Class that represents a grid of people, who interact together and form a society.
    '''

    def __init__(self, width, height, ua_percentage, youth_percentage, adult_percentage, fill):
        self._grid = np.array([[Person(self.generate_age(youth_percentage, adult_percentage), (j, i), self.generage_state(
            ua_percentage)) if random.random() <= fill else None for i in range(width)] for j in range(height)])

    @staticmethod
    def generate_age(prob_y, prob_a):
        final_prob = random.random()
        if final_prob <= prob_y:
            return 0
        if prob_y < final_prob < prob_y+prob_a:
            return 1
        return 2

    @staticmethod
    def generage_state(prob):
        states_ukr = ['active_ua', 'passive_ua']
        states_negative = ['surzhyk', 'passive_ru', 'active_ru']
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
                if not (i == 0 and j == 0):
                    if self._grid[y + i, x + j] is None:
                        continue

                    if self._grid[y + i, x + j].state == 'active_ua':
                        affect += 0.125
                    elif self._grid[y + i, x + j].state == 'passive_ua':
                        affect += 0.0625
                    elif self._grid[y + i, x + j].state == 'passive_ru':
                        affect -= 0.0625
                    elif self._grid[y + i, x + j].state == 'active_ru':
                        affect -= 0.125
        return affect

    def evolve(self):
        '''
        Iterates over all the people in the system and changes their state according to the neighbours.
        '''
        pass

    def __repr__(self):
        return str(self._grid)


a = CellularAutomaton(8, 8, 0.5, 0.5, 0.2, 0.5)
print(a)
print(a.get_neighbours_affect(3,5))