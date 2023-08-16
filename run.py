from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-python', methods=['GET'])
def run_python():
    output = subprocess.check_output(['python', 'script.py'])
    return jsonify(output=output.decode('utf-8'))



if __name__ == '__main__':
    app.run(debug=True)
