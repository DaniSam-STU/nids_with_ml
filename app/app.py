from flask import Flask, render_template, jsonify
from system_info import get_local_ip
from realtime_monitor import get_network_stats
from detector import classify_traffic

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", user_ip=get_local_ip())

@app.route("/api/live")
def live_api():
    stats = get_network_stats()
    label, confidence, attack_count, detections = classify_traffic(stats)

    return jsonify({
        "stats": stats,
        "label": label,
        "confidence": confidence,
        "attacks": attack_count,
        "detections": detections
    })

if __name__ == "__main__":
    print("🛡 NIDS running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
