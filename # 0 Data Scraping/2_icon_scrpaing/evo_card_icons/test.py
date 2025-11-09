import os

folder = "./"   # change this to your folder path

for filename in os.listdir(folder):
    if filename.endswith("_Evolution.webp"):
        new_name = filename.replace("_Evolution", "")
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")
