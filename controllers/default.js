const Pty = require('node-pty');
const fs = require('fs');

exports.install = function () {

    ROUTE('/');
    WEBSOCKET('/', socket, ['raw']);

};

function socket() {

    this.encodedecode = false;
    this.autodestroy();

    this.on('open', function (client) {

        // Spawn terminal
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',
            cols: 80,
            rows: 24,
            cwd: process.env.PWD,
            env: process.env
        });

        client.tty.on('exit', function (code, signal) {
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function (data) {
            client.send(data);
        });

    });

    this.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('message', function (client, msg) {
        client.tty && client.tty.write(msg);
    });
}

if (process.env.YTCREDS != null) {
    console.log("Creating yt_creds.json file.");
    fs.writeFile('yt_creds.json', process.env.YTCREDS, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
            socket.emit("console_output", "Error saving YouTube credentials: " + err);
        }
    });
}

if (process.env.DRIVECREDS != null) {
    console.log("Creating drive_creds.json file.");
    fs.writeFile('drive_creds.json', process.env.DRIVECREDS, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
            socket.emit("console_output", "Error saving Google Drive credentials: " + err);
        }
    });
}