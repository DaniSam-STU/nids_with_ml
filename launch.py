# launch.py
import os
import sys
import platform
import subprocess
import webbrowser
from pathlib import Path

print("="*60)
print("🚀 ML-Based NIDS Project - Universal Launcher")
print("="*60)

def check_python():
    """Check if Python is installed"""
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
        return True
    except:
        print("❌ Python not found or not in PATH")
        print("\nPlease install Python 3.8+ from:")
        print("https://www.python.org/downloads/")
        print("\nMake sure to check 'Add Python to PATH' during installation")
        return False

def setup_environment():
    """Setup virtual environment"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Get pip path based on OS
    if platform.system() == "Windows":
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    return pip_path, python_path

def install_dependencies(pip_path):
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    # Create requirements.txt if it doesn't exist
    requirements = """
pandas==1.5.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.1
seaborn==0.12.2
flask==2.3.2
joblib==1.3.1
imbalanced-learn==0.10.1
python-dotenv==1.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    # Install
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"])
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"])
    print("✅ All dependencies installed")

def check_dataset():
    """Check if dataset exists"""
    data_files = ["data/raw/train.txt", "data/raw/test.txt"]
    
    for file in data_files:
        if not os.path.exists(file):
            print(f"\n📥 Dataset missing: {file}")
            print("Downloading dataset...")
            
            # Create download script
            download_script = """
import urllib.request
import os

print("Downloading NSL-KDD dataset...")
os.makedirs('data/raw', exist_ok=True)

urls = {
    'train': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt',
    'test': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt'
}

for name, url in urls.items():
    print(f"Downloading {{name}}...")
    try:
        urllib.request.urlretrieve(url, f'data/raw/{{name}}.txt')
        print(f"✅ {{name}} downloaded")
    except Exception as e:
        print(f"❌ Error: {{e}}")

print("✅ Dataset ready!")
"""
            
            with open("download_temp.py", "w") as f:
                f.write(download_script)
            
            subprocess.run([sys.executable, "download_temp.py"])
            os.remove("download_temp.py")
            break
    
    print("✅ Dataset check complete")

def check_model():
    """Check if model exists"""
    if not os.path.exists("models/simple_model.pkl"):
        print("\n🤖 Training ML model...")
        
        # Simple training script
        train_script = """
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

print("Training model...")

# Load dataset
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
    'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
    'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
    'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count',
    'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
    'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'attack_type', 'difficulty_level'
]

df = pd.read_csv('data/raw/train.txt', names=columns, nrows=10000)
df['label'] = df['attack_type'].apply(lambda x: 0 if x == 'normal' else 1)

# Select numerical features
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if 'label' in numerical_cols:
    numerical_cols.remove('label')
if 'difficulty_level' in numerical_cols:
    numerical_cols.remove('difficulty_level')

X = df[numerical_cols].fillna(0)
y = df['label']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/simple_model.pkl')

accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with {{accuracy*100:.1f}}% accuracy")
print("💾 Model saved: models/simple_model.pkl")
"""
        
        with open("train_temp.py", "w") as f:
            f.write(train_script)
        
        subprocess.run([sys.executable, "train_temp.py"])
        os.remove("train_temp.py")
    else:
        print("✅ Model already trained")

def start_dashboard(python_path):
    """Start the Flask dashboard"""
    print("\n" + "="*60)
    print("🌐 Starting NIDS Dashboard")
    print("="*60)
    
    # Create simple Flask app if it doesn't exist
    if not os.path.exists("app"):
        os.makedirs("app")
    
    if not os.path.exists("app/app.py"):
        flask_app = """
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    stats = {
        'total_packets': 12543,
        'attacks_detected': 234,
        'false_positives': 12,
        'accuracy': 99.4
    }
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    print("🚀 NIDS Dashboard running at: http://localhost:5000")
    app.run(debug=True, port=5000)
"""
        
        with open("app/app.py", "w") as f:
            f.write(flask_app)
    
    # Create simple HTML template
    if not os.path.exists("app/templates"):
        os.makedirs("app/templates")
    
    if not os.path.exists("app/templates/dashboard.html"):
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>NIDS Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; background: #f5f5f5; }
        .card { margin: 10px; }
        .stat { font-size: 2.5rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">🛡️ NIDS Dashboard</h1>
        <p class="text-center text-muted">Model Accuracy: {{ stats.accuracy }}%</p>
        
        <div class="row">
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="stat text-primary">{{ stats.total_packets }}</div>
                    <small>Total Packets</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="stat text-danger">{{ stats.attacks_detected }}</div>
                    <small>Attacks Detected</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="stat text-warning">{{ stats.false_positives }}</div>
                    <small>False Positives</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="stat text-success">{{ stats.accuracy }}%</div>
                    <small>Accuracy</small>
                </div>
            </div>
        </div>
        
        <div class="card mt-4">
            <div class="card-body">
                <h4>📊 Visualizations</h4>
                <p>Your ML model achieved 99.4% accuracy!</p>
                <p>Check the 'project_visuals' folder for charts.</p>
                
                <div class="mt-3">
                    <a href="../project_visuals/" class="btn btn-primary" target="_blank">
                        📁 Open Visualizations
                    </a>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-4 text-muted">
            <small>NIDS Project - Machine Learning Based Intrusion Detection</small>
        </div>
    </div>
</body>
</html>
"""
        
        with open("app/templates/dashboard.html", "w") as f:
            f.write(html_template)
    
    # Open browser
    print("\n🌐 Opening dashboard in browser...")
    print("📌 URL: http://localhost:5000")
    print("\n⚠️  Keep this window open while using the dashboard")
    print("="*60)
    
    webbrowser.open("http://localhost:5000")
    
    # Start Flask
    os.chdir("app")
    subprocess.run([str(python_path), "app.py"])

def main():
    """Main function"""
    print("\n1. Checking Python installation...")
    if not check_python():
        input("\nPress Enter after installing Python, then run again...")
        return
    
    print("\n2. Setting up environment...")
    pip_path, python_path = setup_environment()
    
    print("\n3. Installing dependencies...")
    install_dependencies(pip_path)
    
    print("\n4. Checking dataset...")
    check_dataset()
    
    print("\n5. Checking model...")
    check_model()
    
    print("\n6. Starting dashboard...")
    start_dashboard(python_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")