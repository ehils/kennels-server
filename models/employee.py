class Employee():

    def __init__(self, id, name, address, location_id, animal_id=None):
        self.id = id
        self.name = name
        self.address = address
        self.location_id = location_id
        self.location = None
        self.animal_id = animal_id
        self.animal = None