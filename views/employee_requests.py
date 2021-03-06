import sqlite3
import json
from models import Employee, Location, Animal

EMPLOYEES = [
    {
      "id": 1,
      "name": "Tony Cheese" 
    },
    {
      "id": 2,
      "name": "Jim Heckler" 
    },
    {
      "id": 3,
      "name": "Lord Palmerstadt" 
    },
    {
      "id": 4,
      "name": "Pitt the Elder" 
    },
    {
      "id": 5,
      "name": "Derrick Whipple" 
    }
]
def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            e.animal_id,
            l.name location_name,
            l.address location_address,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status
        FROM employee e
        JOIN Location as l
            ON l.id = e.location_id         
        LEFT JOIN Animal as a
            ON a.id = e.animal_id         
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # employee class above.
            employee = Employee(row['id'], row['name'], 
                                row['address'], row['location_id'], row['animal_id'])
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            animal = Animal(row['id'], row['animal_name'])
            
            employee.location = location.__dict__
            employee.animal = animal.__dict__

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            e.animal_id,
            l.name location_name,
            l.address location_address,
            a.name animal_name
        FROM Employee e
        JOIN Location as l
            ON l.id = e.location_id         
        LEFT JOIN Animal as a
            ON a.id = e.animal_id  
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], 
                            data['address'], data['location_id'], data['animal_id'])
        location = Location(data['location_id'], data['location_name'], data['location_address'])
        animal = Animal(data['id'], data['animal_name'])
        employee.location = location.__dict__
        employee.animal = animal.__dict__
        return json.dumps(employee.__dict__)
def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            e.animal_id
        FROM employee e
        WHERE e.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], 
                                row['address'], row['location_id'], row['animal_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)
def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))
def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO employee
            ( name, address, location_id, animal_id )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_employee['name'], new_employee['address'],
              new_employee['locationId'], new_employee['animalId'], ))
        # Q: comma after last value?
        # A:
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


    return json.dumps(new_employee)


# def get_all_employees():
#     return EMPLOYEES

# def get_single_employee(id):
    
#     requested_employee = None
    
#     for employee in EMPLOYEES:
#         if employee["id"] == id:
#             requested_employee = employee

#     return requested_employee
# def create_employee(employee):
#     # Get the id value of the last employee in the list
#     max_id = EMPLOYEES[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the employee dictionary
#     employee["id"] = new_id

#     # Add the employee dictionary to the list
#     EMPLOYEES.append(employee)

#     # Return the dictionary with `id` property added
#     return employee
# def delete_employee(id):
#     # Initial -1 value for employee index, in case one isn't found
#     employee_index = -1

#     # Iterate the EMPLOYEES list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Store the current index.
#             employee_index = index

#     # If the employee was found, use pop(int) to remove it from list
#     if employee_index >= 0:
#         EMPLOYEES.pop(employee_index)
# def update_employee(id, new_employee):
#     # Iterate the EMPLOYEES list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Update the value.
#             EMPLOYEES[index] = new_employee
#             break

