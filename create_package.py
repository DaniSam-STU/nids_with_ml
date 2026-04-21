# create_package.py
import zipfile
import os

def create_package():
    """Create final ZIP package"""

    print("Creating distribution package...")

    # Files to include
    files_to_include = [
        "launch.py",
        "run.bat",
        "run.sh",
        "README.md",
        "requirements.txt"
    ]

    # Folders to include
    folders_to_include = [
        "app",
        "models",
        "project_visuals",
        "data"
    ]

    # ZIP file name
    zip_filename = "NIDS_Project_Complete.zip"

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:

        # Add files
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Added file: {file}")
            else:
                print(f"⚠️ Skipped (not found): {file}")

        # Add folders
        for folder in folders_to_include:
            if os.path.exists(folder):
                for root, _, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"✅ Added: {file_path}")
            else:
                print(f"⚠️ Skipped folder (not found): {folder}")

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)

    print("\n" + "=" * 50)
    print(f"🎉 ZIP CREATED SUCCESSFULLY")
    print(f"📦 File: {zip_filename}")
    print(f"📏 Size: {size_mb:.2f} MB")
    print("=" * 50)

if __name__ == "__main__":
    create_package()
