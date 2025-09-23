import pickle
import os
import re
from datetime import datetime

# Define the file path for saving member data
DATA_FILE = './data/members.dat'
members = []

# Constants for error messages
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

def load_members():
    """Load member data from a binary file using pickle."""
    global members
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            try:
                members = pickle.load(f)
            except (pickle.UnpicklingError, EOFError):
                members = []
    print("회원 관리 파일을 불러왔습니다..... ")

def save_members():
    """Save member data to a binary file using pickle."""
    # Ensure the directory exists before saving
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(members, f)
    print("회원 정보가 파일에 저장되었습니다......")

def display_main_menu():
    """Display the main menu options."""
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

def print_member_list(member_list):
    """
    Prints a formatted list of members.
    No: 2 digits, Name: 10 chars, Phone: 16 chars, Relation: 10 chars.
    Address: '-' if empty, otherwise prints the value.
    """
    print(f"총 등록 회원 수: {len(member_list)}")
    print(f"{'No':<3} | {'Name':<10} | {'Phone':<16} | {'Relation':<10} | Address")
    print("-" * 65)
    for i, member in enumerate(member_list):
        address = member.get('address', '')
        if not address:
            address_str = '-'
        else:
            address_str = address

        print(f"[{i+1:2d}] | {member['name']:<10} | {member['phone']:<16} | {member['relation']:<10} | {address_str}")


def list_members():
    """Handle listing and viewing member details."""
    while True:
        print("\n[1. 회원 목록 출력]")
        print('='*20)
        if not members:
            print("등록된 회원이 없습니다.")
            return

        print_member_list(members)

        inputMsg = "상세 조회할 번호를 입력하거나, 'back'을 입력해 메인 메뉴로 돌아가세요: "

        choice = input(inputMsg)
        if not choice: 
            print(inputMsg)
            continue
        
        try:
            member_index = int(choice) - 1
            if 0 <= member_index < len(members):
                view_detail(members[member_index])
            else:
                print(ERROR_MESSAGES["invalid_input"])
        except ValueError:
            print(ERROR_MESSAGES["invalid_input"])

def view_detail(member):
    """Display detailed information for a single member."""
    print("\n[회원 상세 정보]")
    print('='*20)
    print(f"이름: {member['name']}")
    print(f"전화번호: {member['phone']}")
    print(f"관계: {member['relation']}")
    print(f"주소: {member['address']}")
    print(f"등록일시: {member['reg_date']}")

    while True:
        choice = input("목록으로 돌아가시겠습니까? (1. 예, 2. 아니오): ")
        try: 
            if not choice:
                print(ERROR_MESSAGES["invalid_input"])
                continue    
            elif choice == '1':
                return
        except: 
            print(ERROR_MESSAGES["invalid_input"])

def add_member():
    """Handle adding a new member."""
    while True:
        print("\n[2. 회원 신규 등록]")
        print('='*20)
        name = input("이름: 한영자 1자 이상 5자 이내")
        # --- Validation ---
        if not name:
            print(ERROR_MESSAGES["name_empty"])
            continue
        # Validate Name (1-5 Korean or English characters)
        if not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', name):
            print(ERROR_MESSAGES["name_format"])
            continue

        phone = input("전화번호: xxx-xxxx-xxxx (숫자와 - 만 입력가능)")
        # Validate Phone Number (not empty, 000-0000-0000 format)
        if not phone:
            print(ERROR_MESSAGES["phone_empty"])
            continue
        if not re.fullmatch(r'\d{3}-\d{4}-\d{4}', phone):
            print(ERROR_MESSAGES["phone_format"])
            continue

        relation_input = input("관계 (1.가족, 2.친구, 3.기타): ")
        # Validate Relation (not empty, in map)
        if not relation_input:
            print(ERROR_MESSAGES["relation_empty"])
            continue
        relation_map = {'1': '가족', '2': '친구', '3': '기타'}
        if relation_input not in relation_map:
            print(ERROR_MESSAGES["relation_format"])
            continue
        
        relation = relation_map[relation_input]
        
        address = input("주소: ")
        if not address:
            print(ERROR_MESSAGES["address_empty"])
            continue

        # --- Duplication Check ---
        if any(m['phone'] == phone for m in members):
            print(ERROR_MESSAGES["duplicate_phone"])
            choice = input("메인 메뉴로 돌아가려면 'back'을 입력하거나, 새로 추가하려면 'add'를 입력하세요: ")
            if not choice:
                print(ERROR_MESSAGES['invalid_input'])
            if choice.lower() == 'back':
                return
            continue

        new_member = {
            'name': name,
            'phone': phone,
            'relation': relation,
            'address': address,
            'reg_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add timestamp
        }
        members.append(new_member)
        print("저장 완료.")

        choice = input("메인 메뉴로 돌아가려면 'back'을 입력하거나, 새로 추가하려면 'add'를 입력하세요: ")
        if choice.lower() == 'back':
            return
        if choice.lower() != 'add':
            print(ERROR_MESSAGES["invalid_input"])
            return

def update_member():
    """Handle updating a member."""
    while True:
        print("\n[3. 회원 수정]")
        keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
        
        # --- Search ---
        search_results = [m for m in members if keyword in m['name'] or keyword in m['phone']]
        if not search_results:
            print(ERROR_MESSAGES["not_found"])
            action = input("1. 다시 검색하기, 'back'을 입력해 메인 메뉴로 돌아가기: ")
            if action == '1':
                continue
            return

        print_member_list(search_results)

        choice = input("수정할 번호를 입력하거나, 'back'을 입력해 메인 메뉴로 돌아가세요: ")
        if choice.lower() == 'back':
            return
            
        try:
            update_index = int(choice) - 1
            if 0 <= update_index < len(search_results):
                selected_member = search_results[update_index]
                
                print("\n수정할 항목을 입력하세요 (변경하지 않으려면 그냥 엔터를 누르세요):")
                
                # Input and validation loop
                while True:
                    new_name = input(f"이름 ({selected_member['name']}): ")
                    if new_name and not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', new_name):
                        print(ERROR_MESSAGES["name_format"])
                        continue
                    
                    new_phone = input(f"전화번호 ({selected_member['phone']}): ")
                    if new_phone and not re.fullmatch(r'\d{3}-\d{4}-\d{4}', new_phone):
                        print(ERROR_MESSAGES["phone_format"])
                        continue

                    new_relation_input = input(f"관계 (1.가족, 2.친구, 3.기타) ({selected_member['relation']}): ")
                    relation_map = {'1': '가족', '2': '친구', '3': '기타'}
                    if new_relation_input and new_relation_input not in relation_map:
                        print(ERROR_MESSAGES["relation_format"])
                        continue
                    
                    new_address = input(f"주소 ({selected_member['address']}): ")

                    # Check for phone duplication only if a new phone number was entered
                    if new_phone and any(m['phone'] == new_phone for m in members if m != selected_member):
                        print(ERROR_MESSAGES["duplicate_phone"])
                        continue # Restart the input loop
                    
                    # Update fields that are not empty
                    if new_name:
                        selected_member['name'] = new_name
                    if new_phone:
                        selected_member['phone'] = new_phone
                    if new_relation_input:
                        selected_member['relation'] = relation_map[new_relation_input]
                    if new_address:
                        selected_member['address'] = new_address
                    
                    print("수정 완료.")
                    break # Exit the input loop

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

def remove_member():
    """Handle removing a member."""
    while True:
        print("\n[4. 회원 삭제]")
        keyword = input("검색할 이름 또는 전화번호를 입력하세요: ")
        
        search_results = [m for m in members if keyword in m['name'] or keyword in m['phone']]
        if not search_results:
            print(ERROR_MESSAGES["not_found"])
            action = input("1. 다시 검색하기, 'back'을 입력해 메인 메뉴로 돌아가기: ")
            if action == '1':
                continue
            return

        print_member_list(search_results)

        choice = input("삭제할 번호를 입력하거나, 'back'을 입력해 메인 메뉴로 돌아가세요: ")
        if choice.lower() == 'back':
            return
            
        try:
            delete_index = int(choice) - 1
            if 0 <= delete_index < len(search_results):
                member_to_delete = search_results[delete_index]
                
                confirm = input(ERROR_MESSAGES["delete_confirm"].format(name=member_to_delete['name']))
                if confirm == '1':
                    members.remove(member_to_delete)
                    print("삭제되었습니다.")
                else:
                    print("삭제가 취소되었습니다.")
                return # Return to main menu after action
            else:
                print(ERROR_MESSAGES["invalid_input"])
        except ValueError:
            print(ERROR_MESSAGES["invalid_input"])

def main():
    """Main program loop."""
    load_members()
    while True:
        choice = display_main_menu()
        if choice == '1':
            list_members()
        elif choice == '2':
            add_member()
        elif choice == '3':
            update_member()
        elif choice == '4':
            remove_member()
        elif choice == '5':
            while True:
                confirm = input("정말로 종료하시겠습니까? (1. 예, 2. 아니오): ")
                if confirm == '1':
                    save_members()
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
