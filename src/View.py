class MemberView:
    def show_menu(self):
        print("\n=== 회원 관리 프로그램 ===")
        print("1. 회원 목록 출력")
        print("2. 회원 정보 추가")
        print("3. 회원 정보 수정")
        print("4. 회원 정보 삭제")
        print("5. 프로그램 종료")

    def get_menu_choice(self):
        try:
            return int(input("메뉴 번호를 입력하세요: "))
        except ValueError:
            return None

    def input_member_info(self):
        name = input("이름: ").strip()
        phone = input("전화번호: ").strip()
        address = input("주소 (선택): ").strip()
        type_ = input("종류 (가족/친구/기타): ").strip()
        return name, {"phone": phone, "address": address, "type": type_}

    def input_name(self, action="조회"):
        return input(f"{action}할 회원 이름: ").strip()

    def input_index(self, action="선택"):
        try:
            return int(input(f"{action}할 번호 선택: ")) - 1
        except ValueError:
            return -1

    def confirm(self, message):
        return input(f"{message} (y/n): ").lower() == "y"

    def show_members(self, data):
        if not data:
            print("등록된 회원이 없습니다.")
        else:
            for name, members in data.items():
                for i, info in enumerate(members, 1):
                    print(f"[{i}] 이름: {name}, 전화번호: {info['phone']}, 주소: {info['address']}, 종류: {info['type']}")

    def show_message(self, message):
        print(message)