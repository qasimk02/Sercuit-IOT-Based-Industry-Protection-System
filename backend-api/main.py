from time import time
from flask import Flask, jsonify, request
import sqlite3
import socket
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

status_dict = {0: "Working", 1: "DHT fail", 2: "GSM fail"}


@app.get("/")
def home():
    return ("<h1>Hello</h1>")


@app.get("/data/<int:Status>/<int:device_id>/<int:Temp>/<int:Humi>")
def allow(Status, device_id, Temp, Humi):
    print("Status:", status_dict[Status], "DevId:",
          device_id, "Temp", Temp, "Humi:", Humi)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS DataLogging(
                    Device_Id int,
                    Status text,
                    Temp int,
                    Humi int,
                    Time text)
                """)
    c.execute("INSERT INTO DataLogging VALUES (?,?,?,?,?)",
              (device_id, status_dict[Status], Temp, Humi, timestamp))
    conn.commit()
    conn.close()
    return f'Data sent by {str(device_id)} was received successfully'


@app.post("/dashboard")
def dashboard():
    device_id = 2
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    Data = c.execute(
        "SELECT * FROM DataLogging WHERE Device_Id = ? ORDER BY Time DESC limit 7", (device_id,)).fetchall()
    conn.close()
    return jsonify(Data)


@app.post("/signin")
def signIn():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    if isValid(email, password):
        return jsonify(isValid(email, password))
    else:
        return jsonify({"status": "Error logging in"})


def isValid(email, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print(email, password)
    Data = c.execute(
        "SELECT * FROM loginDetails WHERE email = ? AND password = ?", (email, password)).fetchall()
    if (Data != [] and email == Data[0][2] and password == Data[0][3]):
        conn.close()
        return Data
    else:
        conn.close()
        return False


@app.post("/signup")
def signUp():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    name = request.get_json().get("name")
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO loginDetails (name,email,password) VALUES (?,?,?)",
              (name, email, password))
    data = c.execute(
        "SELECT * FROM loginDetails WHERE email = ? AND password = ?", (email, password)).fetchall()
    conn.commit()
    conn.close()
    return jsonify(data)


if __name__ == "__main__":
    app.debug = True
    IPAddr = socket.gethostbyname(socket.gethostname())
    app.run(host=IPAddr, port=5000)
