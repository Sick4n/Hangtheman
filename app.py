from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import queue

app = Flask(__name__)

# Initialize the hangman.py process
process = subprocess.Popen(
    ['python3', 'hangman.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True
)

# Create a queue to store process output
output_queue = queue.Queue()

# Function to read Hangman process output
def read_process_output():
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_queue.put(output.strip())

# Start a thread to read output from the Hangman process
output_thread = threading.Thread(target=read_process_output)
output_thread.daemon = True
output_thread.start()

@app.route('/')
def index():
    return render_template('terminal.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    user_input = request.json.get('command')
    process.stdin.write(user_input + '\n')
    process.stdin.flush()
    return jsonify(success=True)

@app.route('/get_output', methods=['GET'])
def get_output():
    outputs = []
    while not output_queue.empty():
        outputs.append(output_queue.get())
    return jsonify(outputs=outputs)

if __name__ == '__main__':
    app.run(debug=True)

