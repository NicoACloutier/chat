import uuid, psycopg2, flask
from flask import request
from psycopg2 import ProgrammingError

def get_messages_from_info(conn, chat_id: str) -> tuple[dict[str, str], int]:
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM messages WHERE chat_id = '{chat_id}'")
        try:
            info = cursor.fetchall()
        except ProgrammingError:
            return {}, 404
    return info, 200

def delete_old_message(conn, message_id: str) -> tuple[dict[str, str], int]:
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE * FROM messages WHERE id = '{message_id}' RETURNING *;")
        try:
            info = cursor.fetchone()
        except ProgrammingError:
            return {}, 404
    return info, 200

def post_new_message(conn) -> tuple[dict[str, str], int]:
    data = flask.request.get_json()
    message, chat_id, user_id = data["message"], data["chat_id"], data["user_id"]
    message_id = uuid.uuid4()
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO messages (id, message, chat_id, user_id) VALUES ('{message_id}', '{message}', '{chat_id}', '{user_id}');")
    return {"message": "User added."}, 200

def create_message_api(app: flask.Flask, conn) -> None:
    ENDPOINT_NAME = "/messages"

    @app.post(ENDPOINT_NAME)
    def post_message() -> tuple[dict[str, str], int]:
        return post_new_message(conn)

    @app.get(ENDPOINT_NAME)
    def get_messages() -> tuple[dict[str, str], int]:
        chat_id = request.args.get("id")
        return get_messages_from_info(conn, chat_id)

    @app.delete(ENDPOINT_NAME)
    def delete_message() -> tuple[dict[str, str], int]:
        message_id = request.args.get("id")
        return delete_old_message(conn, message_id)
