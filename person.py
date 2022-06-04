"""
Person implementation
"""


class Person:
    '''
    Class that represents a single person

    Possible states:
        - active_ua
        - passive_ua
        - surzhyk
        - passive_ru
        - active_ru

    Possible ages:
        - youth (0)
        - adult (1)
        - senior (2)
    '''
    ACTIVE_UA = 4
    PASSIVE_UA = 3
    SURZHYK = 2
    PASSIVE_RU = 1
    ACTIVE_RU = 0
    TRANSITION_LIST = ["active_ru", "passive_ru", "surzhyk",
                       "passive_ua", "active_ua"]

    def __init__(self, age, coordinates, state):
        self.age = age
        self.coordinates = coordinates  # (y,x) for the position on the grid
        self.state = state
        # 1 for more possible transition to proukrainian, -1 for transition to prorussian,
        self.transition_prob = 0

    def __str__(self) -> str:
        return f'Person({self.age}, {self.coordinates}) is in {self.state} state'

    def change_state(self, prob):
        '''
        Updates transition_prob according to the neighbours.
        '''
        if prob < abs(self.transition_prob):
            self.state += int(self.transition_prob / abs(self.transition_prob))
            self.state = self.ACTIVE_UA if self.state > self.ACTIVE_UA else self.state
            self.state = self.ACTIVE_RU if self.state < self.ACTIVE_RU else self.state

    def __repr__(self) -> str:
        return self.TRANSITION_LIST[self.state]
