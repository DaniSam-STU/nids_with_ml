import pandas as pd
import urllib.request
import os

print("📥 Downloading NSL-KDD dataset...")

# Create directories
os.makedirs('data/raw', exist_ok=True)

# Download files
urls = {
    'train': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt',
    'test': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt'
}

for name, url in urls.items():
    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, f'data/raw/{name}.txt')
        print(f"✅ {name} downloaded successfully!")
    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")

print("\n🎉 Dataset download complete!")
print("Files saved in: data/raw/")