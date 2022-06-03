
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

    def __init__(self, age, coordinates, state):
        self.age = age
        # self.region = region
        self.coordinates = coordinates
        # self.parents = ukrlang_parents
        self.state = state

    def __str__(self) -> str:
        return f'Person({self.age}, {self.coordinates}) is {self.lang} speaker'
    
    def __repr__(self) -> str:
        return self.state
    

