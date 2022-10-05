from flask import Flask, request, jsonify
import random

app = Flask(__name__)

class User:
    def __init__(self, user_id: int, user_password: int, user_nickname: str, icon: str):
        self.user_id: int = user_id
        self.user_password: int = user_password
        self.user_nickname: str = user_nickname
        self.icon: str = icon

    def full_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_password": self.user_password,
            "user_nickname": self.user_nickname,
            "icon": self.icon
        }
    def safe_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_nickname": self.user_nickname,
            "icon": self.icon
        }

all_users: dict[int, User] = {}
user_id = 0

@app.route('/users', methods=['GET', "POST", "DELETE"])
def users():
    global all_users
    global user_id

    if request.method == 'GET':
        return jsonify({"users": [user.safe_dict() for user in all_users.values()]})
    elif request.method == 'POST':
        user_id += 1
        user_password = random.randint(1, 999999)
        user_nickname = request.json['user_nickname']
        if len(user_nickname) > 25:
            return jsonify({"error": "Nickname too long"}), 400
        if request.json["icon"] is None:
            return jsonify({"error": "No icon provided."}), 400
        if len(request.json["icon"]) != 1:
            return jsonify({"error": "Length of icon is invalid."}), 400
        icon = request.json['icon']
        user = User(user_id, user_password, user_nickname, icon)
        all_users[user_id] = user
        return jsonify(user.full_dict())
    elif request.method == "DELETE":
        if request.json["user_password"] is None:
            return jsonify({"error": "No password provided."}), 400
        if request.json["user_password"] != all_users[user_id].user_password:
            return jsonify({"error": "Wrong password."}), 400
        del all_users[request.json["user_id"]]

@app.route("/icon/<int:user_id>", methods=["GET", "POST"])
def icon(user_id = None):
    global all_users

    if user_id is None:
        return jsonify({"error": "No user ID provided."}), 400
    if not user_id in all_users.keys():
        return jsonify({"error": "User ID does not exist."}), 400

    if request.method == "GET":
        return jsonify({"icon": all_users[user_id].icon}), 200
    if request.method == "POST":
        if request.json["user_password"] is None:
            return jsonify({"error": "No password provided."}), 400
        if request.json["user_password"] != all_users[user_id].user_password:
            return jsonify({"error": "Wrong password."}), 400
        if request.json["icon"] is None:
            return jsonify({"error": "No icon provided."}), 400
        if len(request.json["icon"]) != 1:
            return jsonify({"error": "Length of icon is invalid."}), 400
        all_users[user_id].icon = request.json["icon"]
        return jsonify({"status": "success"}), 200