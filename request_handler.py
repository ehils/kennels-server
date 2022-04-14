from http.server import BaseHTTPRequestHandler, HTTPServer
# Q: BaseHTTPRequestHandler, HTTPserver, where do they come from and what are they
# A: imported from python library
from views import get_all_animals, get_single_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_all_customers, get_single_customer, get_customers_by_email, get_animals_by_location, get_employees_by_location, get_animals_by_status, delete_animal, delete_customer, delete_employee, delete_location, update_animal, create_animal
# create_customer, create_location, create_employee, delete_customer, delete_employee, delete_location, update_customer, update_location, update_employee
import json

from views.animal_requests import delete_animal

# Here's a class. It inherits from another class.
# Q: what does inherit mean in this situation?
# A: it can use methods defined within the inherited class, ie:send_headers, send_response
# Q: how are these two classes working together?
# A: we are defining the HandleREquests class and inheriting methods from BaseHTTPRequestHandler
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
    # def parse_url(self, path):
    #     # Just like splitting a string in JavaScript. If the
    #     # path is "/animals/1", the resulting list will
    #     # have "" at index 0, "animals" at index 1, and "1"
    #     # at index 2.
    #     # defines resource and id so that when they are set later on they will lead to the right path
    #     path_params = path.split("/")
    #     resource = path_params[1]
    #     id = None

    #     # Try to get the item at index 2
    #     try:
    #         # Convert the string "1" to the integer 1
    #         # This is the new parseInt()
    #         id = int(path_params[2])
    #     # Q: what do these two commands do?
    #     # A:
    #     except IndexError:
    #         pass  # No route parameter exists: /animals
    #     except ValueError:
    #         pass  # Request had trailing slash: /animals/

    #     return (resource, id)  # This is a tuple
    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response
        
        Args:
            status (number): the status code to return to the front end
        """
        
        # Q: Are these like properties on an object, of pyhton methods with a method, or functions?
        # A: methods inherited from BASEHTTPREquest
        # Q: What is the general point of these methods
        # A:
        # Returned headers, with response code passed as status arguement
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    # Q: what is the general purpose of these methods
    # A:
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            if key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)
            if key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)
            if key == "status" and resource == "animals":
                response = get_animals_by_status(value)

        self.wfile.write(response.encode())
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())   
    # Here's a method on the class that overrides the parent's method.
    # Q: what method is being overidden
    # It handles any GET request.
    # def do_GET(self):
    #     """Handles GET requests to the server"""
    #     # Set the response code to 'Ok'
    #     # uses inherted methods from above
    #     self._set_headers(200)
    #     response = {}
    #     # Your new console.log() that outputs to the terminal
    #     print(self.path)
        
    #     # Parse the URL and capture the tuple that is returned
    #     # Remember: resource is the list and id is the id of a specific dictionary within that list
    #     (resource, id) = self.parse_url(self.path)

    #     # It's an if..else statement
    #     if resource == "animals":            
    #         # In Python, this is a list of dictionaries
    #         # In JavaScript, you would call it an array of objects
    #         if id is not None:
    #             response = f"{get_single_animal(id)}"

    #         else:
    #             response = f"{get_all_animals()}"
    #     if resource == "locations":            
           
    #         if id is not None:
    #             response = f"{get_single_location(id)}"

    #         else:
    #             response = f"{get_all_locations()}"
    #     if resource == "employees":            
            
    #         if id is not None:
    #             response = f"{get_single_employee(id)}"

    #         else:
    #             response = f"{get_all_employees()}"
    #     if resource == "customers":            
            
    #         if id is not None:
    #             response = f"{get_single_customer(id)}"

    #         else:
    #             response = f"{get_all_customers()}"

    #     # This weird code sends a response back to the client
    #     self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)
        # Q: what is happening here?
        # A:
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        # string to dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None

        # Add a new animal to the list. 
        if resource == "animals":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
            self.wfile.write(f"{new_animal}".encode())
        

    #     # Initialize new animal
    #     new_customer = None

    #     # Add a new customer to the list. Don't worry about
    #     # the orange squiggle, you'll define the create_customer
    #     # function next.
    #     if resource == "customers":
    #         new_customer = create_customer(post_body)

    #     # Encode the new customer and send in response
    #         self.wfile.write(f"{new_customer}".encode())
    #     # Set response code to 'Created'
        

    #     # Initialize new employee
    #     new_employee = None

    #     # Add a new employee to the list. Don't worry about
    #     # the orange squiggle, you'll define the create_employee
    #     # function next.
    #     if resource == "employees":
    #         new_employee = create_employee(post_body)

    #     # Encode the new employee and send in response
    #         self.wfile.write(f"{new_employee}".encode())
    #     # Set response code to 'Created'
        
    #     # Initialize new location
    #     new_location = None

    #     # Add a new location to the list. Don't worry about
    #     # the orange squiggle, you'll define the create_location
    #     # function next.
    #     if resource == "locations":
    #         new_location = create_location(post_body)

    #     # Encode the new location and send in response
    #         self.wfile.write(f"{new_location}".encode())
    # # Here's a method on the class that overrides the parent's method.
    # # It handles any PUT request.

    # def do_PUT(self):
    #     # 204 is "no content"; request was successful but do not need to send back updated resource
    #     self._set_headers(204)
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     post_body = json.loads(post_body)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     # Delete a single animal from the list
    #     if resource == "animals":
    #         update_animal(id, post_body)
    #     if resource == "customers":
    #         update_customer(id, post_body)
    #     if resource == "employees":
    #         update_employee(id, post_body)
    #     if resource == "locations":
    #         update_location(id, post_body)

    #     # Encode the new animal and send in response
    #     self.wfile.write("".encode())
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        if resource == "customers":
            delete_customer(id)
        if resource == "employees":
            delete_employee(id)
        if resource == "locations":
            delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
