
class Person:
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
    

