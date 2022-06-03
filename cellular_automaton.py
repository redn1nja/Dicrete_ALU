import numpy as np
import random
from person import Person


class CellularAutomaton:
    '''
    Class that represents a grid of people, who interact together and form a society.
    '''

    def __init__(self, width, height, ua_percentage, youth_percentage, adult_percentage, fill):
        self._grid = np.array([[Person(self.generate_age(youth_percentage, adult_percentage), (j, i), self.generage_state(
            ua_percentage)) if random.random() <= fill else None for i in width] for j in height])

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
    
