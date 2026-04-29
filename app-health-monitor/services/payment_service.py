from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "payment-service",
        "status": "healthy",
        "timestamp": str(datetime.datetime.now())
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"service": "payment-service", "status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)