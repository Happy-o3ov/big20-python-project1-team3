class MemberView:
    """
    출력관리
    return:
        message(string): 출력 할 메시지 출력
    """
    def show_menu(self):
        """
        메뉴 출력
        """
        print("\n=== 회원 관리 프로그램 ===")
        print("1. 회원 목록 출력")
        print("2. 회원 정보 추가")
        print("3. 회원 정보 수정")
        print("4. 회원 정보 삭제")
        print("5. 프로그램 종료")

    def get_menu_choice(self):
        """
        메뉴 번호 입력
        Returns:
            (int): 입력된 번호
        """
        try:
            return int(input("메뉴 번호를 입력하세요: "))
        except ValueError:
            return None

    def input_member_info(self):
        """
        멤버 정보 입력
        Returns:
            (dictionary) : 입력받은 멤버값
        """
        name = input("이름: ").strip()
        phone = input("전화번호: ").strip()
        address = input("주소 (선택): ").strip()
        if not address:
            address = "-"
        relationShip = input("종류 (가족/친구/기타): ").strip()
        return  {"name": name, "phone": phone, "address": address, "relationShip": relationShip}

    def input_member_update_info(self):
        """
        전화번호 제외한 수정 정보 입력
        Returns:
            (dictionary) : 입력받은 멤버 값
        """
        name = input("이름 (최대 10글자): ").strip()
        if len(name) > 10:
            print("이름은 최대 10글자까지 입력 가능합니다.")
            name = name[:10]
        address = input("주소 (선택): ").strip()
        relationShip = input("종류 (가족/친구/기타): ").strip()
        return {"name": name, "address": address, "relationShip": relationShip}


    def input_name(self, action="조회"):
        """
        이름 값 입력받기
        선택한 메뉴의 기능에따라 입력받을 값 선택
        Args:
            action (str, optional): 옵션. Defaults to "조회".

        Returns:
            (String): 입력받을 값 출력
        """
        return input(f"{action}할 회원 이름: ").strip()

    def input_phone(self, action="삭제"):
        """
        전화번호값 입력받기
        Args:
            action (str, optional): 옵션. Defaults to "삭제".

        Returns:
            _type_: _description_
        """
        return input(f'{action}할 회원 전화번호: ').strip()

    def input_index(self, action="선택"):
        """
        인덱스 값 입력받기
        선택한 메뉴의 기능에따라 입력받을 값 선택
        Args:
            action (str, optional): 입력받은 index값. Defaults to "선택".

        Returns:
            (int): 입력받은 인덱스값 리스트는 0 부터 시작하므로 받은값 -1 
        """
        try:
            return int(input(f"{action}할 번호 선택: ")) - 1
        except ValueError:
            return -1

    def confirm(self, message):
        """
        확인 메시지
        정말로 실행 할 작업인지 체크
        """
        return input(f"{message} (y/n): ").lower() == "y"

    def show_members(self, data):
        """
        멤버 출력
        Args:
            data (dictionary): 출력 할 데이터 중복이 있을경우 리스트 형태로 출력
        """
        if not data:
            print("등록된 회원이 없습니다.")
        else:
            for i, (phone, info) in enumerate(data.items(), 1):
                print(f"[{i}] 이름: {info['name']}, 전화번호: {phone}, 주소: {info['address']}, 종류: {info['relationShip']}")
    def show_message(self, message):
        """
        출력
        """
        print(message)
        