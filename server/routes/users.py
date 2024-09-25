import hashlib, uuid, psycopg2, flask
import random, string

SALT_LENGTH = 20
ENDPOINT_NAME = "/users"

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
    return uuid.uuid4() name, password_hash, password_salt

def post_new_user(conn: psycopg2.connection) -> None:
    """
    Post a user to the database, given a POST request with a name and password.
    Arguments:
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
    Returns:
        `None` (NOTE: posts to database)
    """
    data = flask.request.get_json()
    name = data["name"]
    entered_password = data["entered_password"]
    name, password_hash, password_salt = make_data(name, entered_password)

def create_user_api(app: flask.Flask, conn: psycopg2.connection) -> None:
    """
    Create a user API route.
    Arguments:
        `app: flask.Flask`: Flask app to create the API for.
        `conn: psycopg2.connection`: PostgreSQL connection to execute on.
    Returns:
        `None`
    """
    @app.post(f"{ENDPOINT}")
    def post_user():
        post_new_user(conn)
