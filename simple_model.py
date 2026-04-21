import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("🚀 Building Simple NIDS Model...")

# Column names for NSL-KDD
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

print("📥 Loading data...")
try:
    # Load first 10,000 rows for quick testing
    df = pd.read_csv('data/raw/train.txt', names=columns, nrows=10000)
    print(f"✅ Data loaded: {len(df)} samples")
    
except FileNotFoundError:
    print("❌ Dataset not found! Run download_data.py first")
    exit()

print(f"📊 Dataset shape: {df.shape}")
print(f"📈 Samples loaded: {len(df)}")

# Create binary labels (Normal vs Attack)
print("\n🔧 Creating labels...")
df['label'] = df['attack_type'].apply(lambda x: 0 if x == 'normal' else 1)
normal_count = (df['label'] == 0).sum()
attack_count = (df['label'] == 1).sum()
print(f"Normal samples: {normal_count}")
print(f"Attack samples: {attack_count}")
print(f"Attack percentage: {attack_count/(normal_count+attack_count)*100:.1f}%")

# Select only numerical features for simplicity
print("\n⚙️ Selecting features...")
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if 'label' in numerical_cols:
    numerical_cols.remove('label')
if 'difficulty_level' in numerical_cols:
    numerical_cols.remove('difficulty_level')

print(f"Using {len(numerical_cols)} numerical features")

# Prepare data
X = df[numerical_cols].fillna(0)
y = df['label']

# Split data
print("\n📊 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training: {len(X_train)} samples")
print(f"Testing: {len(X_test)} samples")

# Train Random Forest
print("\n🤖 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predict and evaluate
print("\n📈 Evaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"🎯 Accuracy: {accuracy:.4f}")

# More detailed report
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Attack']))

# Create models directory if not exists
os.makedirs('models', exist_ok=True)

# Save the model
joblib.dump(model, 'models/simple_model.pkl')
print("\n💾 Model saved to: models/simple_model.pkl")

# Test with single prediction
print("\n🧪 Testing with sample prediction...")
sample = X_test.iloc[0:1]
prediction = model.predict(sample)[0]
prob = model.predict_proba(sample)[0]

print(f"Sample features: {sample.shape[1]} features")
print(f"Prediction: {'🚨 ATTACK' if prediction == 1 else '✅ NORMAL'}")
print(f"Confidence - Normal: {prob[0]:.2%}")
print(f"Confidence - Attack: {prob[1]:.2%}")

print("\n" + "="*50)
print("🎉 FIRST MODEL COMPLETE!")
print("="*50)