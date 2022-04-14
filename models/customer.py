class Customer():
    # parameter order matches arguments passed in instance of Class (see customer_requests)
        # parameters with a default value of null have to go at the end of the list of parameters
    def __init__(self, id, name, address, email="", password=""):
# this is the order of the dictionary sent back in postman      
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password