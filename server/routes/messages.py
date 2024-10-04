import uuid, psycopg2, flask
from flask import request

def get_messages_from_info(conn, chat_id: str) -> tuple[dict[str, str], int]:
    pass

def delete_old_message(conn, message_id: str) -> tuple[dict[str, str], int]:
    pass

def post_new_message(conn) -> tuple[dict[str, str], int]:
    pass

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
