import pickle
import os

DATA_FILE = "data\members.dat"
VALID_TYPES = ["가족", "친구", "기타"]

class MemberModel:
    """
    데이터 파일 관리 및 유효성 검사
    """
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """
        파일 불러오기
        Returns:
            (dictionary): 파일에서 데이터를 읽은 후 딕셔너리로 리턴
        """
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
        return {}

    def save_data(self):
        """
        파일 저장
        args:
            data(dictionary) : 
        returns:
            (Boolean)
        """
        try:
            with open(DATA_FILE, "wb") as f:
                pickle.dump(self.data, f)
            return True
        except Exception as e:
            print(f"파일 저장 오류: {e}")
            return False

    def is_valid(self, info):
        """
        유효성 검사
        Args:
            info (dictionary): 파일에서 읽은 데이터

        Returns:
            (boolean): 데이터안에 전화번호와 VALID_TYPES에 포함된 값
        """
        return info["phone"] and info["type"] in VALID_TYPES

    def is_phone_duplicate(self, phone):
        """
        전화번호 중복성 검사
        Args:
            phone (String): 입력받은 전화번호

        Returns:
            (Boolean): 입력받은 전화번호가 파일안의 전화번호와 중복된 값
        """
        for members in self.data.values():
            for member in members:
                if member["phone"] == phone:
                    return True
        return False

    def insert_member(self, name, info):
        """
        정보 입력
        Args:
            name (Sring): 입력받은 이름
            info (dictionary): 입력받은 정보
        """
        if name not in self.data:
            self.data[name] = []
        self.data[name].append(info)

    def get_members(self, name=None):
        """
        name을 키값으로 이름이 있으면 딕셔너리에 정보를 리스트로 저장
        없으면 딕셔너리에 저장
        Args:
            name (String): 입력된 이름
        Returns:
            data (dictionary)
        """
        if name:
            return self.data.get(name, [])
        return self.data

    def update_member(self, name, index, new_info):
        """
        멤버값 업데이트
        Args:
            name (String): 입력받은 이름
            index (int): 입력받은 업데이트 할 멤버
            new_info (dictionary): 업데이트 할 정보
        """
        self.data[name][index] = new_info

    def delete_member(self, name, index):
        """
        정보 삭제
        Args:
            name (String): 입력받은 이름
            index (int): 입력받은 삭제 할 멤버
        """
        del self.data[name][index]
        if not self.data[name]:
            del self.data[name]