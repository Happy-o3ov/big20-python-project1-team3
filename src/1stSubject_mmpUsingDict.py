# ------------------------------------------------------------------------------------ #
# 1stSuject_mmpUsingDict.py 1차 과제 회원관리 class + Dict 를 사용한 방법
# ------------------------------------------------------------------------------------ #

import pickle
import os
import re
from datetime import datetime

# 데이터 파일 경로 설정
DATA_FILE = './data/members.dat'

# 에러 메시지 상수 정의
ERROR_MESSAGES = {
    "name_empty": "이름 오류: 이름을 입력해야 합니다.",
    "name_format": "이름 오류: 이름은 한글 또는 영문 포함 1자이상  5자 이하로 입력해야 합니다.",
    "phone_empty": "전화번호 오류: 전화번호를 입력해야 합니다.",
    "phone_format": "전화번호 오류: '010-0000-0000' 형식으로 입력해야 합니다.",
    "relation_empty": "관계 오류: 관계를 입력해야 합니다.",
    "relation_format": "관계 오류: 1, 2, 3 중 하나를 선택해야 합니다.",
    "address_empty": "주소 오류: 주소를 입력해야 합니다.",
    "duplicate_phone": "중복 오류: 이미 등록된 전화번호입니다.",
    "not_found": "검색된 목록이 없습니다.",
    "invalid_input": "잘못 입력했습니다. 다시 시도하세요.",
    "invalid_menu_number": "잘못 입력했습니다. 다시 시도하세요.",
    "exit_confirm": "정말로 종료하시겠습니까? (1. 예, 2. 아니오): ",
    "delete_confirm": "정말로 '{name}'을(를) 삭제하시겠습니까? (1. 삭제, 2. 취소하고 메인 메뉴로 돌아가기): "
}

class Member:
    """개별 회원 데이터를 담는 클래스"""
    def __init__(self, name, phone, relation, address='-', reg_date=None):
        self.name = name
        self.phone = phone
        self.relation = relation
        self.address = address
        self.reg_date = reg_date if reg_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class MemberManager:
    """회원 전체를 관리하는 클래스 (딕셔너리 기반)"""
    def __init__(self, data_file):
        self.data_file = data_file
        self.members = {}  # 전화번호를 key로 하는 dict
        self.load_members()

    def load_members(self):
        """pickle로 저장된 회원 정보를 불러옴"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                try:
                    self.members = pickle.load(f)
                except (pickle.UnpicklingError, EOFError):
                    self.members = {}
        print("회원 관리 파일을 불러왔습니다.")

    def save_members(self):
        """회원 정보를 pickle로 저장"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.members, f)
        print("회원 정보가 파일에 저장되었습니다.")

    def display_main_menu(self):
        """메인 메뉴 출력 및 선택"""
        print('='*20)
        print("\n[메인 메뉴]")
        print('='*20)
        print("1. 회원 목록 출력")
        print("2. 회원 신규 등록")
        print("3. 회원 수정")
        print("4. 회원 삭제")
        print("5. 프로그램 종료")
        print('='*20)
        return input("메뉴 번호(숫자 1~5까지)를 입력하세요: ")

    def print_member_list(self, member_dict):
        """회원 목록 출력"""
        print(f"총 회원 수: {len(member_dict)}")
        print(f"{'No':<5} | {'이름':<10} | {'전화번호':<16} | {'관계':<10} | 등록일시")
        print("-" * 65)
        for i, member in enumerate(member_dict.values()):
            print(f"[{i+1:5d}] | {member.name:<10} | {member.phone:<16} | {member.relation:<10} | {member.reg_date}")

    def list_members(self):
        """전체 회원 목록 출력 및 상세 보기"""
        while True:
            print("\n[1. 회원 목록 출력]")
            if not self.members:
                print("등록된 회원이 없습니다.")
                return

            self.print_member_list(self.members)

            choice = input("상세 조회할 번호를 입력하거나, '<' 을 입력해 돌아가세요: ")
            if choice.lower() == '<':
                return
            try:
                index = int(choice) - 1
                member = list(self.members.values())[index]
                self.view_detail(member)
            except (ValueError, IndexError):
                print(ERROR_MESSAGES["invalid_input"])

    def view_detail(self, member):
        """회원 상세 정보 출력"""
        print("\n[회원 상세 정보]")
        print(f"이름: {member.name}")
        print(f"전화번호: {member.phone}")
        print(f"관계: {member.relation}")
        print(f"주소: {member.address}")
        print(f"등록일시: {member.reg_date}")

        while True:
            choice = input("회원 목록으로 돌아가시겠습니까? (1. 예, 2. 아니오): ")
            if choice == '1':
                return
            print(ERROR_MESSAGES["invalid_input"])

    def add_member(self):
        """회원 신규 등록"""
        while True:
            print("\n[2. 회원 신규 등록]")
            print("="*65)
            print("* 표시된 항목은 반드시 입력하셔야 합니다.")

            # 이름 입력
            name = input("이름*: 한글 알파벳 포함 5자까지")
            if not name:
                print(ERROR_MESSAGES["name_empty"])
                continue
            if not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', name):
                print(ERROR_MESSAGES["name_format"])
                continue

            # 전화번호 입력
            phone = input("전화번호*: 010-000-0000 형식으로 숫자와 - 만 사용하세요")
            if not phone:
                print(ERROR_MESSAGES["phone_empty"])
                continue
            if not re.fullmatch(r'\d{3}-\d{4}-\d{4}', phone):
                print(ERROR_MESSAGES["phone_format"])
                continue
            if phone in self.members:
                print(ERROR_MESSAGES["duplicate_phone"])
                continue

            # 관계 선택
            relation_input = input("관계* (1.가족, 2.친구, 3.기타): ")
            relation_map = {'1': '가족', '2': '친구', '3': '기타'}
            if relation_input not in relation_map:
                print(ERROR_MESSAGES["relation_format"])
                continue
            relation = relation_map[relation_input]

            address = input("주소: ")

            # 회원 추가
            new_member = Member(name, phone, relation, address)
            self.members[phone] = new_member
            print("저장 완료.")

            choice = input("메인 메뉴로 돌아가려면 '<'을 입력하거나, 새로 추가하려면 'add'를 입력하세요: ")
            if choice.lower() == '<':
                return
            elif choice.lower() != 'add':
                print(ERROR_MESSAGES["invalid_input"])
                return

    def update_member(self):
        """회원 정보 수정"""
        while True:
            print("\n[3. 회원 수정]")
            keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
            results = [m for m in self.members.values() if keyword in m.name or keyword in m.phone]
            if not results:
                print(ERROR_MESSAGES["not_found"])
                if input("1. 다시 검색하기, '<'을 입력해 메인 메뉴로 돌아가기: ") == '<':
                    return
                continue

            temp_dict = {str(i+1): m for i, m in enumerate(results)}
            self.print_member_list(temp_dict)

            choice = input("수정할 번호를 입력하거나, '<'을 입력해 메인 메뉴로 돌아가세요: ")
            if choice.lower() == '<':
                return
            if choice not in temp_dict:
                print(ERROR_MESSAGES["invalid_input"])
                continue

            member = temp_dict[choice]
            old_phone = member.phone

            # 필드 입력 (변경 가능)
            print("\n수정할 항목을 입력하세요 (변경하지 않으려면 그냥 엔터):")
            new_name = input(f"이름 ({member.name}): ")
            if new_name and not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', new_name):
                print(ERROR_MESSAGES["name_format"])
                continue

            new_phone = input(f"전화번호 ({member.phone}): ")
            if new_phone and not re.fullmatch(r'\d{3}-\d{4}-\d{4}', new_phone):
                print(ERROR_MESSAGES["phone_format"])
                continue
            if new_phone and new_phone != old_phone and new_phone in self.members:
                print(ERROR_MESSAGES["duplicate_phone"])
                continue

            new_relation_input = input(f"관계 (1.가족, 2.친구, 3.기타) ({member.relation}): ")
            if new_relation_input and new_relation_input not in {'1', '2', '3'}:
                print(ERROR_MESSAGES["relation_format"])
                continue
            new_relation = {'1': '가족', '2': '친구', '3': '기타'}.get(new_relation_input, member.relation)

            new_address = input(f"주소 ({member.address}): ")

            # 수정 적용
            member.name = new_name or member.name
            member.phone = new_phone or member.phone
            member.relation = new_relation
            member.address = new_address or member.address

            # 전화번호가 바뀐 경우 dict 키 변경
            if new_phone and new_phone != old_phone:
                del self.members[old_phone]
                self.members[new_phone] = member

            print("수정 완료.")
            return

    def remove_member(self):
        """회원 삭제"""
        while True:
            print("\n[4. 회원 삭제]")
            keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
            results = [m for m in self.members.values() if keyword in m.name or keyword in m.phone]
            if not results:
                print(ERROR_MESSAGES["not_found"])
                if input("1. 다시 검색하기, '<'을 입력해 메인 메뉴로 돌아가기: ") == '<':
                    return
                continue

            temp_dict = {str(i+1): m for i, m in enumerate(results)}
            self.print_member_list(temp_dict)

            choice = input("삭제할 번호를 입력하거나, '<'을 입력해 메인 메뉴로 돌아가세요: ")
            if choice.lower() == '<':
                return
            if choice not in temp_dict:
                print(ERROR_MESSAGES["invalid_input"])
                continue

            member = temp_dict[choice]
            confirm = input(ERROR_MESSAGES["delete_confirm"].format(name=member.name))
            if confirm == '1':
                del self.members[member.phone]
                print("삭제되었습니다.")
            else:
                print("삭제가 취소되었습니다.")
            return

def main():
    """메인 루프"""
    manager = MemberManager(DATA_FILE)
    while True:
        choice = manager.display_main_menu()
        if choice == '1':
            manager.list_members()
        elif choice == '2':
            # manager.add_member()
            pass
        elif choice == '3':
            # manager.update_member()
            pass 
        elif choice == '4':
            # manager.remove_member()
            pass 
        elif choice == '5':
            confirm = input(ERROR_MESSAGES["exit_confirm"])
            if confirm == '1':
                manager.save_members()
                print("프로그램을 종료합니다.")
                return
        else:
            print(ERROR_MESSAGES["invalid_menu_number"])

if __name__ == "__main__":
    main()
