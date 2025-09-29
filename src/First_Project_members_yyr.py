import os
import pickle
import re

FILE_NAME = "../data/member.dat"

# 전화번호를 key, 값은 이름·관계·주소
members = {}

# --- 파일 로드/저장 ---
def load_file():
    global members
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            members = pickle.load(f)
    else:
        members = {}

def save_file():
    with open(FILE_NAME, "wb") as f:
        pickle.dump(members, f)

# --- 유효성 검사 ---
def valid_name(name):
    return 1 <= len(name) <= 5 and name.isalnum() # 이름 1글자 이상 ~ 5글자 이내

def valid_phone(phone):
    return re.match(r"^010-\d{4}-\d{4}$", phone) is not None

def valid_rel(rel):
    return rel in ["1", "2", "3"]

def valid_addr(addr):
    return len(addr) <= 100

# --- 기능 ---
def list_members():
    if not members:
        print("회원이 없습니다.")
        return
    print("\n[회원 목록]")
    for idx, (phone, info) in enumerate(members.items(), 1):
        print(f"{idx}. 이름:{info['name']}, 전화:{phone}, 관계:{info['rel']}, 주소:{info['addr']}")
    print(f"총 인원: {len(members)}\n")

def add_member():
    name = input("이름 (1~5자): ")
    if not valid_name(name):
        print("이름 형식 오류")
        return

    phone = input("전화번호 (010-0000-0000): ")
    if not valid_phone(phone):
        print("전화번호 형식 오류")
        return
    if phone in members:
        print("이미 등록된 전화번호입니다.")
        return

    rel = input("관계 (1가족,2친구,3기타): ")
    if not valid_rel(rel):
        print("관계 입력 오류")
        return

    addr = input("주소 (100자 이내): ")
    if not valid_addr(addr):
        print("주소 입력 오류")
        return

    members[phone] = {"name": name, "rel": rel, "addr": addr}
    print("저장 완료!")

# --- 이름으로 회원 찾기 ---
def search_by_name(name):
    results = [(phone, info) for phone, info in members.items() if info['name'] == name]
    return results

def modify_member():
    name = input("수정할 회원 이름: ")
    results = search_by_name(name)
    if not results:
        print("해당 이름의 회원이 없습니다.")
        return

    # 같은 이름이 여러 개면 선택
    if len(results) > 1:
        print("동명이인이 있습니다. 선택해주세요:")
        for i, (phone, info) in enumerate(results, 1):
            print(f"{i}. 전화:{phone}, 이름:{info['name']}, 관계:{info['rel']}, 주소:{info['addr']}")
        try:
            sel = int(input("번호 선택: ")) - 1
            phone = results[sel][0]
        except (ValueError, IndexError):
            print("잘못된 선택")
            return
    else:
        phone = results[0][0]

    new_name = input("새 이름 (1~5자): ")
    if not valid_name(new_name):
        print("이름 오류")
        return

    new_phone = input("새 전화번호 (010-0000-0000): ")
    if not valid_phone(new_phone) or (new_phone != phone and new_phone in members):
        print("전화번호 오류 또는 중복")
        return

    new_rel = input("새 관계 (1,2,3): ")
    if not valid_rel(new_rel):
        print("관계 오류")
        return

    new_addr = input("새 주소 (100자 이내): ")
    if not valid_addr(new_addr):
        print("주소 오류")
        return

    # 전화번호 변경 처리
    if new_phone != phone:
        members[new_phone] = members.pop(phone)

    members[new_phone].update({"name": new_name, "rel": new_rel, "addr": new_addr})
    print("수정 완료!")

def delete_member():
    name = input("삭제할 회원 이름: ")
    results = search_by_name(name)
    if not results:
        print("해당 이름의 회원이 없습니다.")
        return

    # 같은 이름이 여러 개면 선택
    if len(results) > 1:
        print("동명이인이 있습니다. 선택해주세요:")
        for i, (phone, info) in enumerate(results, 1):
            print(f"{i}. 전화:{phone}, 이름:{info['name']}, 관계:{info['rel']}, 주소:{info['addr']}")
        try:
            sel = int(input("번호 선택: ")) - 1
            phone = results[sel][0]
        except (ValueError, IndexError):
            print("잘못된 선택")
            return
    else:
        phone = results[0][0]

    confirm = input("정말 삭제하시겠습니까? (y/n): ")
    if confirm.lower() == "y":
        del members[phone]
        print("삭제 완료!")
    else:
        print("취소됨")

# --- 메인 루프 ---
def main():
    load_file()
    while True:
        print(
    "🔴🟠🟡🟢🔵🟣⚫⚪⚫🟣🔵🟢🟡🟠🔴\n",
      "\n",
      "1. 회원 목록\n",
      "2. 회원 추가\n",
      "3. 회원 수정\n",
      "4. 회원 삭제\n",
      "5. 종료\n",
      "\n",
    "🟥🟧🟨🟩🟦🟪⬛⬜⬛🟪🟦🟩🟨🟧🟥\n")
        choice = input("번호 입력: ")

        if choice == "1":
            list_members()
        elif choice == "2":
            add_member()
        elif choice == "3":
            modify_member()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            confirm = input("종료하시겠습니까? (y/n): ")
            if confirm.lower() == "y":
                save_file()
                print("저장 후 종료합니다.")
                break
        else:
            print("올바른 번호를 입력하세요.")

if __name__ == "__main__":
    main()
