# app.py
from flask import Flask, render_template
from flask_sockets import Sockets
import pty
import os
import fcntl
import struct
import subprocess
import threading
import queue

app = Flask(__name__)
sockets = Sockets(app)

# Initialize the hangman.py process
master_fd, slave_fd = pty.openpty()
process = subprocess.Popen(
    ['python3', 'hangman.py'],
    stdin=slave_fd,
    stdout=slave_fd,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True
)

# Set the non-blocking mode on the master FD
fcntl.fcntl(master_fd, fcntl.F_SETFL, os.O_NONBLOCK)

# Create a queue to store user input
input_queue = queue.Queue()

# Function to read Hangman process output and send it to WebSocket
def read_process_output(ws):
    while True:
        try:
            output = os.read(master_fd, 4096).decode()
        except BlockingIOError:
            output = ""

        if not output and process.poll() is not None:
            break

        for line in output.splitlines():
            ws.send(line + '\n')

# WebSocket route
@sockets.route('/ws')
def ws(ws):
    # Start a thread to continuously read and send Hangman output
    output_thread = threading.Thread(target=read_process_output, args=(ws,))
    output_thread.daemon = True
    output_thread.start()

    # Handle incoming WebSocket messages
    while not ws.closed:
        user_input = ws.receive()
        if user_input:
            input_queue.put(user_input)

# Function to send user input to Hangman process
def send_user_input():
    while True:
        user_input = input_queue.get()
        os.write(master_fd, (user_input + '\n').encode())

# Start a thread to handle user input
input_thread = threading.Thread(target=send_user_input)
input_thread.daemon = True
input_thread.start()

@app.route('/')
def index():
    return render_template('terminal.html')

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

