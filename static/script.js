const socket = io();

       // Start Sniffer
       function startSniffer() {
        socket.emit('command', 'start');
    }

    // Stop Sniffer
    function stopSniffer() {
        socket.emit('command', 'stop');
    }

// Empfangene Pakete in die Tabelle einfügen
socket.on('new_packet', function(msg) {
    const table = document.getElementById("packetTable");
    const row = table.insertRow(-1);
    const cell = row.insertCell(0);
    cell.innerHTML = msg.data;
    console.log(msg.data);
});
