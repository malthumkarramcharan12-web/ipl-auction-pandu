from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

players = [
    {"name": "Virat Kohli", "price": 2},
    {"name": "MS Dhoni", "price": 2},
]

current_index = 0
current_bid = 0
current_team = ""

teams = ["MI","CSK","RCB","KKR","DC","PBKS","RR","SRH","GT","LSG"]

@app.route('/')
def home():
    return render_template("index.html", player=players[current_index], teams=teams)

@socketio.on("bid")
def handle_bid(data):
    global current_bid, current_team

    if data["amount"] > current_bid:
        current_bid = data["amount"]
        current_team = data["team"]

        emit("update", {
            "amount": current_bid,
            "team": current_team
        }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
