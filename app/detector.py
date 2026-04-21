from realtime_monitor import get_network_stats

attack_count = 0
recent_detections = []

def classify_traffic(stats):
    global attack_count, recent_detections

    label = "Normal"
    confidence = 99.0

    # Simple ML-style decision rules
    if stats["packets_recv"] > 300:
        label = "DoS Attack"
        confidence = 97.5
    elif stats["bytes_recv"] > 800000:
        label = "Data Exfiltration"
        confidence = 96.2

    if label != "Normal":
        attack_count += 1
        recent_detections.insert(0, {
            "type": label,
            "confidence": confidence,
            "time": stats["timestamp"]
        })

    recent_detections[:] = recent_detections[:5]

    return label, confidence, attack_count, recent_detections

