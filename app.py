from flask import Flask, request, jsonify, Response # type: ignore
import base64
import threading

app = Flask(__name__)
latest_frame = {"data": None}

@app.route('/video_feed', methods=['POST'])
def receive_video_frame():
    data = request.get_json()
    if data and 'frame' in data:
        latest_frame['data'] = data['frame']
        return jsonify({"status": "Frame received"}), 200
    return jsonify({"error": "No frame provided"}), 400

@app.route('/live_image')
def serve_live_image():
    if latest_frame['data']:
        return Response(
            base64.b64decode(latest_frame['data']),
            mimetype='image/jpeg'
        )
    else:
        return "Waiting for live feed...", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
