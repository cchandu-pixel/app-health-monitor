from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "inventory-service",
        "status": "healthy",
        "timestamp": str(datetime.datetime.now())
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"service": "inventory-service", "status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)