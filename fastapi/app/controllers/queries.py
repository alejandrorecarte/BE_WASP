#USER
def register_query():
    return "INSERT INTO Users (email, name, last_name, hashed_password) VALUES (%s, %s, %s, %s);"

def login_query():
    return "SELECT * FROM Users WHERE email LIKE %s;"

# POSTS
def check_post_access_query():
    return "SELECT user_email FROM Posts WHERE post_id LIKE %s"

def create_post_query():
    return "INSERT INTO Posts (title, description, is_sold ,user_email) VALUES (%s, %s, %s, %s)"

def update_post_query():
    return "UPDATE Posts SET title = %s, description = %s, is_sold = %s WHERE post_id LIKE %s"

def delete_post_query():
    return "DELETE FROM Posts WHERE post_id LIKE %s"

def get_post_query():
    return "SELECT * FROM Posts WHERE post_id LIKE %s"

def get_post_user_query():
    return "SELECT * FROM Posts WHERE user_email LIKE %s ORDER BY post_timestamp DESC LIMIT %s OFFSET %s"

def get_post_user_pages_query():
    return "SELECT COUNT(*) FROM Posts WHERE user_email LIKE %s"

def get_post_last_query():
    return "SELECT * FROM Posts ORDER BY post_timestamp DESC LIMIT %s OFFSET %s"

def get_post_last_pages_query():
    return "SELECT COUNT(*) FROM Posts"

def get_last_id():
    return "SELECT LAST_INSERT_ID()"

#VEHICLE
def check_vehicle_access_query():
    return "SELECT p.user_email FROM Vehicles v INNER JOIN Posts p ON v.post_id = p.post_id WHERE v.license_plate LIKE %s"

def create_vehicle_query():
    return "INSERT INTO Vehicles (license_plate, brand, model, registration_year, price, observations, vehicle_type, fuel_type, photo, post_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

def update_vehicle_query():
    return "UPDATE Vehicles SET brand = %s, model = %s, registration_year = %s, price = %s observations = %s, vehicle_type = %s, fuel_type = %s, photo = %s WHERE license_plate LIKE %s"

def delete_vehicle_query():
    return "DELETE FROM Vehicles WHERE license_plate LIKE %s"

def get_vehicle_query():
    return ("SELECT * FROM Vehicles WHERE license_plate LIKE %s")

def get_post_vehicles_query():
    return ("SELECT v.license_plate, v.brand, v.model, v.registration_year, v.price, v.observations, v.vehicle_type, v.fuel_type, v.photo, v.post_id FROM Vehicles v INNER JOIN Posts p ON v.post_id = p.post_id WHERE v.post_id LIKE %s")
