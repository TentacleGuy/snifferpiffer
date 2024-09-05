import os
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit

# Pfad zum Projektverzeichnis setzen (einen Ordner höher)
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app)
command = "none";

# Variable, um die empfangenen Daten zu speichern
latest_data = {}

# Route für das Webinterface (GET)
@app.route('/')
def index():
    return render_template('index.html')

# Start-Sniffer-Ereignis
@socketio.on('start_sniffer')
def handle_start_sniffer():
    print("Sniffer gestartet")
    global command
    command = "start"
    # Hier kannst du den ESP32 anweisen, mit dem Sniffen zu beginnen
    # Beispiel: Sende ein Signal über HTTP oder seriell an den ESP32

# Stop-Sniffer-Ereignis
@socketio.on('stop_sniffer')
def handle_stop_sniffer():
    print("Sniffer gestoppt")
    global command
    command = "stop"
    # Hier kannst du den ESP32 anweisen, das Sniffen zu stoppen

# Route für die Befehle (GET)
@app.route('/command', methods=['GET'])
def send_command():
    return command 

# Route, um Daten vom ESP zu empfangen (POST)
@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    latest_data = request.json  # Speichere die empfangenen Daten
    print(f"Empfangene Daten: {latest_data}")
    
    # Sende die empfangenen Daten in Echtzeit über SocketIO an das Frontend
    socketio.emit('new_packet', {'data': latest_data})
    return "Daten empfangen!", 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)