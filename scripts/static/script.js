const socket = io();

// Funktion zum Starten des Sniffers
function startSniffer() {
    socket.emit('start_sniffer');
}

// Funktion zum Stoppen des Sniffers
function stopSniffer() {
    socket.emit('stop_sniffer');
}

// Empfangene Pakete in die Tabelle einfügen
socket.on('new_packet', function(msg) {
    const table = document.getElementById("packetTable");
    const row = table.insertRow(-1);
    const cell = row.insertCell(0);
    cell.innerHTML = msg.data;
    console.log(msg.data);
});
