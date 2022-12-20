from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

MAX_MESSAGE_LENGTH: int = 250
MAX_NICKNAME_LENGTH: int = 25


class User:

    def __init__(self, user_id: int, user_password: int, user_nickname: str,
                 message: str):
        self.user_id: int = user_id
        self.user_password: int = user_password
        self.user_nickname: str = user_nickname
        self.message: str = message

    def full_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_password": self.user_password,
            "user_nickname": self.user_nickname,
            "message": self.message
        }

    def safe_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_nickname": self.user_nickname,
            "message": self.message
        }


all_users: dict[int, User] = {}
next_user_id = 0


@app.route('/users', methods=['GET', "POST", "DELETE"])
def users():
    global all_users
    global next_user_id

    if request.method == 'GET':
        return jsonify(
            {"users": [user.safe_dict() for user in all_users.values()]})
    elif request.method == 'POST':
        next_user_id += 1
        user_password = random.randint(1, 999999)
        user_nickname = request.json['user_nickname']
        if len(user_nickname) > MAX_NICKNAME_LENGTH:
            return jsonify({"error": "Nickname too long"}), 400
        if request.json["message"] is None:
            return jsonify({"error": "No message provided."}), 400
        if len(request.json["message"]) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": "Length of message is invalid."}), 400
        message = request.json['message']
        user = User(next_user_id, user_password, user_nickname, message)
        all_users[next_user_id] = user
        return jsonify(user.full_dict())
    elif request.method == "DELETE":
        if request.json["user_password"] is None:
            return jsonify({"error": "No password provided."}), 400
        if request.json["user_password"] != all_users[
                request.json["user_id"]].user_password:
            return jsonify({"error": "Wrong password."}), 400
        del all_users[request.json["user_id"]]
        return jsonify({"status": "success"}), 200


@app.route("/message/<int:user_id>", methods=["GET", "PATCH"])
def message(user_id=None):
    global all_users

    if user_id is None:
        return jsonify({"error": "No user ID provided."}), 400
    if not user_id in all_users.keys():
        return jsonify({"error": "User ID does not exist."}), 400

    if request.method == "GET":
        return jsonify({"message": all_users[user_id].message}), 200
    if request.method == "PATCH":
        if request.json["user_password"] is None:
            return jsonify({"error": "No password provided."}), 400
        if int(request.json["user_password"]
               ) != all_users[user_id].user_password:
            return jsonify({"error": "Wrong password."}), 400
        if request.json["message"] is None:
            return jsonify({"error": "No message provided."}), 400
        if len(request.json["message"]) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": "Length of message is invalid."}), 400
        all_users[user_id].message = request.json["message"]
        return jsonify({"status": "success"}), 200