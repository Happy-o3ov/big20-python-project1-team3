import pickle
from datetime import datetime
import os
import re

DATA_FILE = "../data/members.dat"
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
        phone_pattern = r"010-\d{4}-\d{4}$"
        return (
            re.match(phone_pattern, info['phone'])is not None and
            info["relationShip"] in VALID_TYPES
        )

    def is_phone_duplicate(self, phone):
        """
        전화번호 중복성 검사
        Args:
            phone (String): 입력받은 전화번호

        Returns:
            (Boolean): 입력받은 전화번호가 파일안의 전화번호와 중복된 값
        """
        return phone in self.data

    def insert_member(self, info):
        """
        정보 입력
        Args:
            info (dictionary): 입력받은 정보
        """
        self.data[info["phone"]] = {
            "name": info["name"],
            "address": info["address"],
            "relationShip": info["relationShip"],
            "regDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


    def get_members(self, name):
        """
        이름으로 멤버값 반환
        Args:

        Returns:
            data (dictionary)
        """
        return {phone: info for phone, info in self.data.items() if info["name"] == name}

    def update_member(self, phone, new_info):
        """
        멤버값 업데이트
        Args:
            phone (String): 입력받은 번호
            new_info (dictionary): 업데이트 할 정보
        """
        self.data[phone] = new_info

    def delete_member(self, phone):
        """
        정보 삭제
        Args:
            phone (String): 입력받은 번호
        """
        if phone in self.data:
            del self.data[phone]
            
    def get_all_members(self):
        """
        모든 데이터 가져오기
        Returns:
            (dictionary): 데이터
        """
        return self.data
