import hashlib, uuid, psycopg2, flask
import random, string
from flask import request
from psycopg2 import ProgrammingError

SALT_LENGTH = 20

def find_hash(entered_password: str, salt: str) -> str:
    """
    Find the hash of an entered password with a salt.
    Arguments:
        `entered_password: str`: the password attempt to generate a hash for.
        `salt: str`: the given salt to help generate the hash.
    Returns:
        `str`: the resulting sha265 hash.
    """
    h = haslib.new('sha256')
    h.update((entered_password + salt).encode())
    return h.hexdigest()

def make_data(name: str, entered_password: str) -> tuple[str, str, str, str]:
    """
    Create data for insertion into user table.
    Arguments:
        `name: str`: the entered username.
        `entered_password: str`: the entered password.
    Returns:
        `str`: the randomly generated user ID.
        `str`: the username to insert.
        `str`: the hash to insert.
        `str`: the randomly generated salt to insert.
    """
    password_salt = random.choices(string.printable, k=SALT_LENGTH)
    password_hash = find_hash(entered_password, password_salt)
    return uuid.uuid4(), name, password_hash, password_salt

def post_new_user(conn) -> tuple[dict[str, str], int]:
    """
    Post a user to the database, given a POST request with a name and password.
    Arguments:
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
    Returns:
        `dict[str, str]`: Return information.
        `int`: Response code.
    """
    data = flask.request.get_json()
    name = data["name"]
    entered_password = data["entered_password"]
    name, password_hash, password_salt = make_data(name, entered_password)
    uid = uuid.uuid4()
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO users (id, name, hash, salt) VALUES ('{uid}', '{name}', '{password_hash}', '{password_salt}');")
    return {"message": "User added."}, 200

def get_user_from_id(conn, user_id: str) -> tuple[dict[str, str], int]:
    """
    Select a user from the identifier.
    Arguments:
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
    Returns:
        `dict[str, str]`: Returned data in dictionary form.
        `int`: Response code.
    """
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}';")
        try:
            info = cursor.fetchone()
        except ProgrammingError:
            return {}, 404
    return info, 200

def delete_user_from_id(conn, user_id: str) -> tuple[dict[str, str], int]:
    """
    Delete a user from a table with their ID.
    Arguments:
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
        `user_id: str`: Unique ID of user to delete.
    Returns:
        `dict[str, str]`: Deleted row from table, if applicable.
        `int`: Response code.
    """
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE * FROM users WHERE id = '{user_id}' RETURNING *;")
        try:
            info = cursor.fetchone()
        except ProgrammingError:
            return {}, 404
    return info, 200
        
def create_user_api(app: flask.Flask, conn) -> None:
    """
    Create a user API route.
    Arguments:
        `app: flask.Flask`: Flask app to create the API for.
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
    Returns:
        `None`
    """
    ENDPOINT_NAME = "/users"    

    @app.post(f"{ENDPOINT_NAME}")
    def post_user() -> tuple[dict[str, str], int]:
        return post_new_user(conn)

    @app.get(f"{ENDPOINT_NAME}")
    def get_user() -> tuple[dict[str, str], int]:
        user_id = request.args.get("id")
        return get_user_from_id(conn, user_id)
    
    @app.delete(f"{ENDPOINT_NAME}")
    def delete_user() -> tuple[dict[str, str], int]:
        user_id = request.args.get("id")
        return delete_user_from_id(conn, user_id)
