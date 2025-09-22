import pickle
import os

DATA_FILE = "members.dat"
VALID_TYPES = ["가족", "친구", "기타"]

class MemberModel:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        return {}

    def save_data(self):
        try:
            with open(DATA_FILE, "wb") as f:
                pickle.dump(self.data, f)
            return True
        except Exception as e:
            print(f"파일 저장 오류: {e}")
            return False

    def is_valid(self, info):
        return info["phone"] and info["type"] in VALID_TYPES

    def is_phone_duplicate(self, phone):
        for members in self.data.values():
            for member in members:
                if member["phone"] == phone:
                    return True
        return False

    def insert_member(self, name, info):
        if name not in self.data:
            self.data[name] = []
        self.data[name].append(info)

    def get_members(self, name=None):
        if name:
            return self.data.get(name, [])
        return self.data

    def update_member(self, name, index, new_info):
        self.data[name][index] = new_info

    def delete_member(self, name, index):
        del self.data[name][index]
        if not self.data[name]:
            del self.data[name]