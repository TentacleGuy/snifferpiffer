import serial
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Serielle Schnittstelle
ser = serial.Serial('COM1', 115200)  # Passe dies an deinen Port an

logfile = None  # Datei-Handler, initialisiert auf None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_sniffer')
def start_sniffer():
    global logfile
    if logfile is None:
        # Erstelle einen neuen Dateinamen mit Zeitstempel
        filename = "sniffer_log_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        logfile = open(filename, "wb")  # Öffne die neue Datei zum Schreiben

    while True:
        if ser.in_waiting:
            packet = ser.read(ser.in_waiting).hex()  # Lies die Daten vom ESP32
            logfile.write(packet.encode())  # Schreibe die Pakete in die Datei
            logfile.flush()
            socketio.emit('new_packet', {'data': packet})

@socketio.on('stop_sniffer')
def stop_sniffer():
    global logfile
    if logfile:
        logfile.close()  # Schließe die Datei
        logfile = None

if __name__ == '__main__':
    socketio.run(app, debug=True)
