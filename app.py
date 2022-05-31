from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
Socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("message.html")

@Socketio.on("broadcast message")
def message_display(data):
    #call this event in the client side and display the console.log data.message
    emit("show message", {"message": data["message"]},
    broadcast=True)

if __name__ == '__main__':
    Socketio.run(app, host="0.0.0.0", port=2000, debug=True)
