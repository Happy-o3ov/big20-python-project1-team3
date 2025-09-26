from Model import MemberModel
from View import MemberView

class MemberController:
    """
    전체 프로그램의 동작을 담당하는 클래스
    """
    def __init__(self):
        self.model = MemberModel()
        self.view = MemberView()

    def run(self):
        """
        전체 프로그램의 동작을 실행
        선택한 메뉴의 기능을 실행하도록 함         
        """
        while True:
            self.view.show_menu()
            choice = self.view.get_menu_choice()

            if choice == 1:
                self.view.show_members(self.model.get_all_members())

            elif choice == 2:
                info = self.view.input_member_info()
                if not self.model.is_valid(info):
                    self.view.show_message("입력값이 유효하지 않습니다.")
                    continue
                if self.model.is_phone_duplicate(info["phone"]):
                    self.view.show_message("이미 등록된 전화번호입니다.")
                    continue
                self.model.insert_member(info)
                self.view.show_message("회원 정보가 추가되었습니다.")

            elif choice == 3:
                name = self.view.input_name("수정")
                members = self.model.get_members(name)
                if not members:
                    self.view.show_message("회원을 찾을 수 없습니다.")
                    continue
                self.view.show_members(members)
                idx = self.view.input_index("수정")
                if idx < 0 or idx >= len(members):
                    self.view.show_message("잘못된 번호입니다.")
                    continue
                phone = list(members.keys())[idx]
                new_info = self.view.input_member_info()
                if not self.model.is_valid(new_info):
                    self.view.show_message("입력값이 유효하지 않습니다.")
                    continue
                if self.model.is_phone_duplicate(new_info["phone"]) and new_info["phone"] != phone:

                    self.view.show_message("이미 등록된 전화번호입니다.")
                    continue
                self.model.update_member(phone, new_info)
                self.view.show_message("회원 정보가 수정되었습니다.")

            elif choice == 4:
                name = self.view.input_name("삭제")
                members = self.model.get_members(name)
                if not members:
                    self.view.show_message("회원을 찾을 수 없습니다.")
                    continue
                self.view.show_members(members)
                idx = self.view.input_index("삭제")
                if idx < 0 or idx >= len(members):
                    self.view.show_message("잘못된 번호입니다.")
                    continue
                phone = list(members.keys())[idx]
                if self.view.confirm("정말로 삭제하시겠습니까?"):
                    self.model.delete_member(phone)
                    self.view.show_message("회원 정보가 삭제되었습니다.")

            elif choice == 5:
                if self.view.confirm("정말로 종료하시겠습니까?"):
                    if self.model.save_data():
                        self.view.show_message("파일 저장 완료. 프로그램을 종료합니다.")
                        break
                    else:
                        self.view.show_message("파일 저장 중 오류가 발생했습니다.")
            else:
                self.view.show_message("잘못된 메뉴 번호입니다.")