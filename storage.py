import json
import os

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Warning: data.json is corrupted.")
        return []

    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"Error saving data: {e}")