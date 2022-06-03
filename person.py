
class Person:
    def __init__(self, age, region, coordinates, ukrlang_parents):
        self.age = age
        self.region = region
        self.coordinates = coordinates
        self.parents = ukrlang_parents
        self.lang = None

    def __str__(self) -> str:
        return f'Person({self.age}, {self.region}, {self.coordinates}, {self.parents}) is {self.lang} speaker'
    
