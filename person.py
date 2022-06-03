
class Person:
    '''
    Class that describes a single person

    Possible states:
        -active_ua
        -passive_ua
        -surzhyk
        -passive_ru
        -active_ru
    '''
    def __init__(self, age, region, coordinates, ukrlang_parents):
        self.age = age
        self.region = region
        self.coordinates = coordinates
        self.parents = ukrlang_parents
        self.state = None

    def __str__(self) -> str:
        return f'Person({self.age}, {self.region}, {self.coordinates}, {self.parents}) is in {self.state} state'
