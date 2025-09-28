# ------------------------------------------------------------------------------------ #
# 1stSuject_mmpUsingClass.py 1차 과제 회원관리 class 를 사용한 방법
# ------------------------------------------------------------------------------------ #

import pickle
import os
import re
from datetime import datetime

# 회원관리 저장 파일 지정
DATA_FILE = './data/members.dat'

# 에러메세지 상수 선언
ERROR_MESSAGES = {
    "name_empty": "이름 오류: 이름을 입력해야 합니다.",
    "name_format": "이름 오류: 이름은 한글 또는 영문 1자 이상 5자 이하로 입력해야 합니다.",
    "phone_empty": "전화번호 오류: 전화번호를 입력해야 합니다.",
    "phone_format": "전화번호 오류: '000-0000-0000' 형식으로 입력해야 합니다.",
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
    """ 회원 한명을 위한 데이터 클래스 이름, 전화번호, 관계, 주소, 최종수정일 """
    def __init__(self, name, phone, relation, address='-', reg_date=None):
        self.name = name
        self.phone = phone
        self.relation = relation
        self.address = address
        self.reg_date = reg_date if reg_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class MemberManager:
    """ 회원관리를 위한 클래스, 등록/수정/삭제처리, 파일 입출력 및 메뉴 출력 
        load_members(self) # 파일 오픈 및 read
        save_members() # 회원정보 저장
        display_main_menu() # 메인 메뉴 출력
        print_member_list() # 1. 회원 목록 출력
        list_members()      # 1.1 목록 출력 후 상세조회 회원 선택
        view_detail()       # 1.2 회원 상세 조회
        add_member()        # 2. 회원 추가
        update_member()     # 3. 회원정보 수정
        remove_member()     # 4. 회원 삭제
    """
    def __init__(self, data_file): # 실행시 저장파일 읽어오기 
        self.data_file = data_file
        self.members = [] # 데이터 목록용 빈 리스트
        self.load_members() # 회원정보 로드 @self.members

    def load_members(self):
        """ 파일에 저장된 자료 읽어서 self.members에 로드하기 """
        if os.path.exists(self.data_file): # 파일 존재 여부 확인
            with open(self.data_file, 'rb') as f: # binary mode로 read
                try:
                    self.members = pickle.load(f) # members에 파일 로딩 
                except (pickle.UnpicklingError, EOFError):
                    self.members = []
        print("회원 관리 파일을 불러왔습니다.")

    def save_members(self):
        """ pickle 를 이용하여 회원정보 파일에 binary mode로 저장"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.members, f)
        print("회원 정보가 파일에 저장되었습니다.")

    def display_main_menu(self):
        """ 메인 메뉴 출력 및 메뉴 번호 입력받기."""
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

    def print_member_list(self, member_list):
        """
        등록 회원수 및 목록 출력
        No: 5 자리, 이름: 10자리, 전화번호: 16 자리, 관계: 10 자리, 주소 : '-' if empty else prints the value.
        """
        print(f"총 회원 수: {len(member_list)}")
        print(f"{'No':<5} | {'이름':<10} | {'전화번호':<16} | {'관계':<10} | 등록일시") # 목록 형식 지정
        print("-" * 65)
        for i, member in enumerate(member_list):
            
            print(f"[{i+1:5d}] | {member.name:<10} | {member.phone:<16} | {member.relation:<10} | {member.regdate}") # 형식에 맞게 출력

    def list_members(self):
        """ 목록 조회 후 상세보기 회원 순번 받기."""
        while True:
            print("\n[1. 회원 목록 출력]")
            if not self.members:
                print("등록된 회원이 없습니다.")
                return

            self.print_member_list(self.members)

            while True:
                choice = input("상세 조회할 번호를 입력하거나, '<' 을 입력해 돌아가세요: ")
                if not choice :
                    print(ERROR_MESSAGES['invalid_input']) # 값을 입력하세요
                    continue

                if choice.lower() == '<': # main menu로 돌아가기 
                    return                
                try:
                    member_index = int(choice) - 1
                    if 0 <= member_index < len(self.members):
                        self.view_detail(self.members[member_index])
                        break # 상세 조회 후 밖으로 빠져나가 다시 목록 조회
                    else:
                        print(ERROR_MESSAGES["invalid_input"])
                        continue
                except ValueError:
                    print(ERROR_MESSAGES["invalid_input"])

    def view_detail(self, member):
        """ 회원 상세 조회 후 목록으로 이동 """
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
        """ 회원 추가 ."""
        while True:
            print("\n[2. 회원 신규 등록]")
            print("="*65)
            print("* 표시된 항목은 반드시 입력하셔야 합니다.")
            name = input("이름*: ")
            if not name: # 입력값이 없는 경우 에러 메세지 출력
                print(ERROR_MESSAGES["name_empty"])
                continue
            if not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', name): # 입력값이 한영자 5자이가 아닌 경우 에러 처리
                print(ERROR_MESSAGES["name_format"])
                continue

            phone = input("전화번호*: ")
            if not phone: # 입력값이 없는 경우 에러 메세지 출력
                print(ERROR_MESSAGES["phone_empty"])
                continue
            if not re.fullmatch(r'\d{3}-\d{4}-\d{4}', phone):
                print(ERROR_MESSAGES["phone_format"])
                continue

            relation_input = input("관계* (1.가족, 2.친구, 3.기타): ")
            if not relation_input: # 입력값이 없는 경우 에러 메세지 출력
                print(ERROR_MESSAGES["relation_empty"])
                continue
            relation_map = {'1': '가족', '2': '친구', '3': '기타'} # 입력 가능한 값 지정 
            if relation_input not in relation_map: # 입력 가능한 값이 아닌 경우 에러 메세지 출력
                print(ERROR_MESSAGES["relation_format"])
                continue
            relation = relation_map[relation_input] # 입력한 숫자에 해당하는 value(한글) 저장
            
            address = input("주소: ")
            # if not address: # 주소는 필수 입력값에서 제외
            #     print(ERROR_MESSAGES["address_empty"])
            #     continue

            if any(member.phone == phone for member in self.members):
                print(ERROR_MESSAGES["duplicate_phone"])
                choice = input("메인 메뉴로 돌아가려면 '<'을 입력하거나, 새로 추가하려면 'add'를 입력하세요: ")
                if choice.lower() == '<':
                    return
                continue

            new_member = Member(name, phone, relation, address)
            self.members.append(new_member)
            print("저장 완료.")

            choice = input("메인 메뉴로 돌아가려면 '<'을 입력하거나, 새로 추가하려면 'add'를 입력하세요: ")
            if choice.lower() == 'back':
                return
            if choice.lower() != 'add':
                print(ERROR_MESSAGES["invalid_input"])
                return

    def update_member(self):
        """Handle updating a member."""
        while True:
            print("\n[3. 회원 수정]")
            keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
            
            search_results = [m for m in self.members if keyword in m.name or keyword in m.phone]
            if not search_results:
                print(ERROR_MESSAGES["not_found"])
                action = input("1. 다시 검색하기, '<'을 입력해 메인 메뉴로 돌아가기: ")
                if action == '1':
                    continue
                return

            self.print_member_list(search_results)

            choice = input("수정할 번호를 입력하거나, '<'을 입력해 메인 메뉴로 돌아가세요: ")
            if choice.lower() == 'back':
                return
                
            try:
                update_index = int(choice) - 1
                if 0 <= update_index < len(search_results):
                    selected_member = search_results[update_index]
                    
                    print("\n수정할 항목을 입력하세요 (변경하지 않으려면 그냥 엔터를 누르세요):")
                    
                    while True:
                        new_name = input(f"이름 ({selected_member.name}): ")
                        if new_name and not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', new_name):
                            print(ERROR_MESSAGES["name_format"])
                            continue
                        
                        new_phone = input(f"전화번호 ({selected_member.phone}): ")
                        if new_phone and not re.fullmatch(r'\d{3}-\d{4}-\d{4}', new_phone):
                            print(ERROR_MESSAGES["phone_format"])
                            continue

                        new_relation_input = input(f"관계 (1.가족, 2.친구, 3.기타) ({selected_member.relation}): ")
                        relation_map = {'1': '가족', '2': '친구', '3': '기타'}
                        if new_relation_input and new_relation_input not in relation_map:
                            print(ERROR_MESSAGES["relation_format"])
                            continue
                        
                        new_address = input(f"주소 ({selected_member.address}): ")

                        if new_phone and any(member.phone == new_phone for member in self.members if member != selected_member):
                            print(ERROR_MESSAGES["duplicate_phone"])
                            continue
                        
                        if new_name:
                            selected_member.name = new_name
                        if new_phone:
                            selected_member.phone = new_phone
                        if new_relation_input:
                            selected_member.relation = relation_map[new_relation_input]
                        if new_address:
                            selected_member.address = new_address
                        
                        print("수정 완료.")
                        break

                    while True:
                        action = input("1. 메인 메뉴로 돌아가기, 2. 수정 계속하기: ")
                        if action == '1':
                            return
                        if action == '2':
                            break
                        print(ERROR_MESSAGES["invalid_input"])
                else:
                    print(ERROR_MESSAGES["invalid_input"])
            except ValueError:
                print(ERROR_MESSAGES["invalid_input"])

    def remove_member(self):
        """Handle removing a member."""
        while True:
            print("\n[4. 회원 삭제]")
            keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
            
            search_results = [m for m in self.members if keyword in m.name or keyword in m.phone]
            if not search_results:
                print(ERROR_MESSAGES["not_found"])
                action = input("1. 다시 검색하기, '<'을 입력해 메인 메뉴로 돌아가기: ")
                if action == '1':
                    continue
                return

            self.print_member_list(search_results)

            choice = input("삭제할 번호를 입력하거나, '<'을 입력해 메인 메뉴로 돌아가세요: ")
            if choice.lower() == '<':
                return
                
            try:
                delete_index = int(choice) - 1
                if 0 <= delete_index < len(search_results):
                    member_to_delete = search_results[delete_index]
                    
                    confirm = input(ERROR_MESSAGES["delete_confirm"].format(name=member_to_delete.name))
                    if confirm == '1':
                        self.members.remove(member_to_delete)
                        print("삭제되었습니다.")
                    else:
                        print("삭제가 취소되었습니다.")
                    return
                else:
                    print(ERROR_MESSAGES["invalid_input"])
            except ValueError:
                print(ERROR_MESSAGES["invalid_input"])

def main():
    """Main program loop."""
    manager = MemberManager(DATA_FILE)
    while True:
        choice = manager.display_main_menu()
        if choice == '1':
            manager.list_members()
        elif choice == '2':
            manager.add_member()
        elif choice == '3':
            manager.update_member()
        elif choice == '4':
            manager.remove_member()
        elif choice == '5':
            while True:
                confirm = input("정말로 종료하시겠습니까? (1. 예, 2. 아니오): ")
                if confirm == '1':
                    manager.save_members()
                    print("프로그램을 종료합니다.")
                    return
                elif confirm == '2':
                    break
                else:
                    print(ERROR_MESSAGES["invalid_input"])
        else:
            print(ERROR_MESSAGES["invalid_menu_number"])

if __name__ == "__main__":
    main()
