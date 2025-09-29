# ------------------------------------------------------------------------------------ #
# 1stSuject.py 1차 과제 회원 및 회원관리 class + Dict 를 사용한 방법
# ------------------------------------------------------------------------------------ #

import pickle
import os
import re
from datetime import datetime
import time
from enum import Enum

# 데이터 파일 경로 설정
DATA_FILE = '../data/members.dat'

# 간단한 상수 정의 
class Command(Enum):
    ''' 입력 명령어 상수들 '''
    RETURN_TO_MAIN = '<' # 메인메뉴로 돌아가기 
    CONFIRM_YES = 'y'    # yes
    CONFIRM_NO = 'n'     # no
    ADD_AGAIN  = 'a'     # 추가 계속하기 
    SEARCH_AGAIN = 'r'   # 검색 계속하기 
    RETURN_TO_LSIT = 'l' # 조회 목록으로 돌아가기
    EDIT_AGAIN = 'e'     # 수정 계속하기 
    DEL_AGAIN  = 'd'     # 삭졔 계속하기

# 에러 메시지 상수 정의
ERROR_MESSAGES = {
    "name_empty"      : "⚠️ 이름 오류: 이름을 입력해야 합니다.",
    "name_format"     : "⚠️ 이름 오류: 이름은 한글 또는 영문 1자 이상 5자 이하로 입력해야 합니다.",
    "phone_empty"     : "⚠️ 전화번호 오류: 전화번호를 입력해야 합니다.",
    "phone_format"    : "⚠️ 전화번호 오류: '010-0000-0000' 형식으로 입력해야 합니다.",
    "relation_empty"  : "⚠️ 관계 오류: 관계를 입력해야 합니다.",
    "relation_format" : "⚠️ 관계 오류: 1, 2, 3 중 하나를 선택해야 합니다.",    
    "address_empty"   : "⚠️ 주소 오류: 주소를 입력해야 합니다.",
    "address_length"  : "⚠️ 주소는 100자 이내로 입력해주세요.",
    "duplicate_phone" : "⚠️ 중복 오류: 이미 등록된 전화번호입니다.",
    "inpt_keyword"    : "⚠️ 키워드를 입력해주세요.",
    "invalid_keyword" : "⚠️ 키워드는 1자 이상 16자 이하로 입력해주세요.",
    "invalid_keyword2": "⚠️ 한글, 영문, 숫자만 입력해주세요. 특수문자는 사용할 수 없습니다.",
    "invalid_input"   : "⚠️ 잘못 입력했습니다. 다시 시도하세요.",
    "invalid_number"  : "⚠️ 유효하지 않은 번호입니다.",
    "input_num_only"  : "⚠️ 숫자만 입력해주세요.",
    "something_wrong" : "😕 죄송합니다. 알 수 없는 문제가 발생했습니다. 입력값을 확인해주세요.",
}

# 메세지 상수 정의 
MESSAGES = {
  'openFile' : "회원 관리 파일을 불러왔습니다.",
  'inputMenuNo' : "메뉴 번호(숫자 1~5까지)를 입력하세요: ",
  'savedData' : "\n\n💾 회원 정보가 {action_type} 되었습니다.\n\n",
  'noData' : "\n\n🚫 등록된 회원이 없습니다. 🔙 메인 메뉴로 돌아갑니다. \n\n", 
  'not_found': "\n\n🚫 검색된 목록이 없습니다.\n\n",
  'getActionGo2Main' : "🔙 메인 메뉴로 돌아가려면 '<' 를 입력하세요: " ,
  'getActionAfterList' : "📄상세 조회할 번호를 입력하거나, '<' 을 입력해 메인 메뉴로 돌아가세요: ", 
  'getActionAfterView' : "👥 회원목록으로 돌아가려면 'l', 🔙 메인 메뉴로 돌아가려면 '<'을 입력하세요: ",
  'actionAfterAddOK': "🔙 메인 메뉴로 돌아가려면 '<'을 입력하거나, 새로 추가하려면 'a'를 입력하세요: ",  
  'getActionAfterNoResult'  : "🔙 메인 메뉴로 돌아가려면 '<'을 입력하거나, 다시 검색하려면 'r'를 입력하세요: ",
  'inputSearchKeyword' : "🔍 검색할 이름 또는 전화번호를 한자 이상 16자 이내로 입력하세요: ", 
  'inputNum4EditOrBack2Menu' : '✏️ 수정할 번호를 입력하거나,  🔙 메인 메뉴로 돌아가려면 '<'을 입력하세요: ',
  'getActionAfterEditOK': "🔙 메인 메뉴로 돌아가려면 '<'을 입력하거나, 계속 수정하려면 'e'를 입력하세요: ", 
  'inputNumber4DelOrBack2Menu' : "✏️ 삭제할 번호를 입력하거나,  🔙 메인 메뉴로 돌아가려면 '<'을 입력하세요: ",
  'getActionAfterDelOK': "🔙 메인 메뉴로 돌아가려면 '<'을 입력하거나, 계속 삭제하려면 'd'를 입력하세요: ", 
  'delete_confirm'  : "🚨 정말 삭제하시겠습니까? (y. 삭제(복구안됨), n. 취소하고 메인 메뉴로 돌아가기): ",  
  'exit_confirm'    : "📄 정말 종료하시겠습니까? (y. 예, n. 아니오): ",
  'mainMenu' : '''
==================================================
      [ 회원관리 프로그램 메인 메뉴 ]  
--------------------------------------------------            
      아래 번호 중 하나를 입력하세요.

      1. 👥 회원 목록 조회
      2. 🆕 회원 신규 등록
      3. ✏️ 회원 정보 검색 후 수정
      4. ❌ 회원 정보 검색 후 삭제
      5. ⏻ 프로그램 종료
-------------------------------------------------- 
   입력 항목 * 표시 : 필수 입력 항목입니다.  
--------------------------------------------------  
'''
}

# 화면 출력용 menuTitle 
MENU_TITLES = {
  '0': '[ 회원관리 프로그램 메인 메뉴 ]' ,
  '1': ' < 메인 < 1. 회원 목록 조회 ' ,
  '2': ' < 메인 < 2. 회원 정보 추가(신규 등록) ' ,
  '3': ' < 메인 < 3. 회원 정보 검색 후 수정 ' ,
  '4': ' < 메인 < 4. 회원 정보 검색 후 삭제 ' ,
  'view': ' < 메인 < 1. 회원 목록 조회 < 회원 상세조회 ' ,
  'edit': ' < 메인 < 3. 회원 정보 검색 < 회원 수정하기 '    
}

# 관계 출력용 맵
RELATION_MAP = {'1': '❤️ 가족', '2': '👪 친구', '3': '🌐 기타'}

# 회원 한 명을 위한 클래스로써 추후 추가 데이터나 기능 발생 여부를 두고 클래스를 생성함.
class Member:
    """개별 회원 데이터를 담는 클래스 선언. """
    def __init__(self) :
      self.member = {} # 한명 저장용
      self.search_results = {} # 검색 결과 저장용

    def add_member_info(self, phone, name, relation, address) -> None:
      ''' 한명의 회원 정보를 phone 을 키로 해서 dict로 저장하기 '''
      self.member[phone] = {
          'name' : name,
          'relation' : relation,
          'address' : address,
          'regDate' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      }            
# //End Of Class - Member
            

# [start class : MemberManager] --------- #
class MemberManager:
    """회원 전체를 관리하는 클래스 (딕셔너리 기반)"""
    def __init__(self, data_file):
        self.data_file = data_file   # set data file 
        self.members = {}            # 전화번호를 key로 하는 dict
        self.load_members()          # 시작하면서 data load하기 

    def print_bar(self, style_str:str="=", repeat_cnt:int=50)->None:
        '''styleStr를 입력받아 repeat_cnt번 출력하는 함수
        param: style_str 출력할 문자
               repeat_cnt : 반복할 횟수 로 10보다 크고 100보다 작아야 함
        유효성 검사를 통과하지 않으면 try exception하지 않고 그냥 기본값(= 50번) 출력
        return : None
        '''
        # repeat_cnt를 입력받았을때 정수형이고 100보다 작은 경우 
        if isinstance(repeat_cnt, int) and (10 < repeat_cnt <= 100):
            print(style_str * repeat_cnt)
        else: # 그렇지 않을때 기본값 출력
            print("=" * 50)

    def print_menu_title(self, menu_no)->None:
        ''' 메뉴 타이틀 출력하기 유효하지 않을 때 아무것도 출력하지 않음'''
        if  menu_no in MENU_TITLES : # 입력받은 번호나 param값이 메뉴타이틀 키 값에 잇으면
            print()  # 빈줄 한 줄 출력
            title_len = 60 # 60칸 
            self.print_bar('=', title_len) # 총 길이만큰 줄 출력
            print(f"{MENU_TITLES[menu_no]:^{title_len}}") # 메뉴 타이틀 중앙에 위치
            self.print_bar('=', title_len) # 총 길이만큰 줄 출력
            print() # 한줄 띄우기 

    def print_error(self, msg_name:str)->None:
        ''' error message 출력하기 '''
        message = ERROR_MESSAGES.get(msg_name)

        self.print_bar("~")
        if message: # message에 값이 있으면 출력
            print(f"{message}")
        else: # 없으면 알수 없는 에러코드 출력
            print(f"⚠️ 알 수 없는 에러 코드: '{msg_name}'")
        self.print_bar("~")
        return None

    def load_members(self):
        """pickle로 저장된 회원 정보를 불러옴"""
        if os.path.exists(self.data_file): # 파일이 있는가?
            with open(self.data_file, 'rb') as f: # 있다면 rb 모드로 open
                try:
                    self.members = pickle.load(f) # 파일 읽어서 메모리에 로드
                except (pickle.UnpicklingError, EOFError): # 예외 처리                     
                    self.members = {} # 빈 멤버 변수 선언 
        print(MESSAGES['openFile']) # logging message print

    def save_members(self, action_type="저장"):
        """회원 정보를 pickle로 저장"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True) # 파일 존재여부 확인해서 없으면 생성 just in case
        with open(self.data_file, 'wb') as f: # 파일을 쓰기 모드로 오픈
            pickle.dump(self.members, f) # 메모리에 있는걸 dump로 저장
        print(MESSAGES['savedData'].format(action_type=action_type)) # 저장완료 메세지 출력


    def display_main_menu(self) -> str:
        """ 메인 메뉴 출력 및 선택. input으로 메뉴번호를 입력받아 return 함. """
        print(MESSAGES['mainMenu'])             # 메인 메뉴 텍스트 출력 
        # time.sleep(1.5)                             # 메뉴 출력 후 잠시 term을 줌 for ipynb test용
        return input(MESSAGES['inputMenuNo'])   # 메뉴번호 입력 받고 리턴
    
    # [start func : print_member_list() ] -------------------------------------------------------
    def print_member_list(self, members):
        """회원 목록 출력"""

        print(f"총 회원 수: {len(members)}") # 총 회원수 출력
        self.print_bar("-", 80)
        print(f"{'번호':^3} | {'이름':^11} | {'전화번호':^12} | {'관계':^10} | 등록일시") # 목록 타이틀 출력
        self.print_bar("-", 80)
        
        # members 값을 for 문 돌리기 위해 enumerate 로 바꾼 후 목록 출력하기 
        for idx, (phone, member) in enumerate(members.items(), start=1): 
            print(f"{idx:^5d} | {member.get('name'):<10} | {phone:<16} | {RELATION_MAP[member.get('relation')]:<10} | {member.get('regDate')}") # 한명 정보 출력
            self.print_bar('-', 80) # 구분자 출력 

    # [star func: view_detail() ] ---------------------------------------------------------
    def view_detail(self, view_no:int) -> None:
        """회원 상세 정보 출력 
        param : 상세 조회할 회원 members의 index 번호
        """
        # 조회 순번 유효성 검사 
        # print(f"202 : view_no = {view_no}") # debugging code 
        if view_no < 0 or view_no >= len(self.members):
            self.print_error("invalid_input") # 잘못입력했습니다~ 
            return
        
        self.print_menu_title('view') # 메뉴 타이틀 출력

        # 전화번호 가 들어 있는 key 목록 추출
        phones = list(self.members.keys())
        phone = phones[view_no] # 전화번호 가져오기 
        member = self.members[phone] # 해당 전화번호로 다른 정보 가져오기 
        address = member['address'] if member['address'] else '-' # 전화번호가 없을때 - 출력하기 

        # 각 항목 출력하기 
        print(f"{'👤 이름':<12}: {member['name']}")
        print(f"{'📞 전화번호':<10}: {phone}")
        print(f"{'👪 관계':<12}: {RELATION_MAP[member['relation']]}")
        print(f"{'🏠 주소':<12}: {address}")
        print(f"{'🕒 등록일':<12}: {member['regDate']}")

    # [end func: view_detail() ] ---------------------------------------------------------

    # [star func: list_member(self, menu_no) ] -------------------------------------------
    def list_members(self, menu_no:str)->str:
      """전체 회원 목록 출력 및 상세 보기
        param : menu_no : 타이틀 출력용
      """
      # 상세조회를 여러번 할 수 있으니 메인 메뉴로 돌아가기가 있을 때까지 반복
      while True:
        self.print_menu_title(menu_no) # 메뉴 타이틀 출력

        if not self.members: # 등록된 회원이 없는 경우
          
          print(MESSAGES['noData']) # 회원없음 출력하고
          return # 빠짐

        self.print_member_list(self.members) # 회원 목록이 있는 경우 출력

        action_no = input(MESSAGES['getActionAfterList']) # 상세보기 할 회원 번호 입력 받기
        if action_no == Command.RETURN_TO_MAIN.value: # 메인 메뉴로 돌아가기 입력된 경우
          return                # 함수 호출 종료하고 메인 메뉴 출력으로 돌아가기
        try:
          view_no = int(action_no) # 상세번호를 숫자로 변경
          self.view_detail(view_no-1) # index는 0 인데 출력을 1부터 했으니 -1해서 전달하기 
        except (ValueError, IndexError): # 숫자가 아닌 경우 에러 출력
          self.print_error("invalid_input")
          
        # 상세 정보 출력 후 목록 혹은 메인 메뉴로 돌아갈지 입력받기
        while True:  
          print() # 한쭉 띠고            
          action_no = input(MESSAGES['getActionAfterView']).strip()          
          if action_no == Command.RETURN_TO_MAIN.value: # < 메뉴로 돌아가기 
              return 
          elif action_no == Command.RETURN_TO_LSIT.value: # l 목록으로
              break
          else : # 그외 값 입력시 
            self.print_error("invalid_input")          

    # [star func: input items ] ---------------------------------------------------------    
    def input_name(self, name="")-> str:
      ''' name 를 입력받아 유효성 검사 후 유효한 값만 return 한다.'''
      placeholder = "(한영숫자를 한글자 이상 5자 이내로 입력하세요)."
      while True:
        if name: 
            placeholder = f"현재 이름: [{name}] " + placeholder
        print(f"\n ⌨️ {placeholder}")
        name = input(f"👤 이름* : ") # 이름 입력받기
        if not name: # 입력값이 없는 경우 에러 메세지 출력
            self.print_error("name_empty")
            continue
        if not re.fullmatch(r'[가-힣a-zA-Z0-9. ]{1,5}', name): # 입력값이 한영자 10자이가 아닌 경우 에러 처리
            self.print_error("name_format")
            continue
        else:
            return name

    def input_phone(self)->str:
      ''' 전화번호를 입력받고 유효성 검사 통과한 경우 해당 번호를 리턴한다'''
      while True:
        placeholder = '010-0000-0000 형식으로 입력하세요~'
        print(f"\n ⌨️ {placeholder}")
        phone = input("📞 전화번호*: ")

        if not phone: # 입력값이 없는 경우 에러 메세지 출력
            self.print_error("phone_empty")
            continue
        if not re.fullmatch(r'^010-\d{4}-\d{4}', phone): # 입력형식 맞지 않으면 에러 메세지 출력
            self.print_error("phone_format")
            continue
        
        # 전화 번호 중복 체크
        if any(registed_phone == phone for registed_phone in self.members.keys()):
            self.print_error("duplicate_phone")
            action = input(MESSAGES['actionAfterAddOK'])
            if action.lower() in (Command.RETURN_TO_MAIN.value, Command.ADD_AGAIN.value):
                return action
            else:
               continue # 다시 입력받기 
        else:
            return phone

    def input_relation(self, relation:str="")->str:
      ''' 관계성 입력받아 유효성 검사 한 후 return 하기'''
      while True:
        placeholder = " ('1':가족, '2':친구, '3':기타 1,2,3 중 하나를 입력하세요.)"
        if relation in RELATION_MAP: # 기 등록 관계값이 있는 경우
           placeholder = f"현재 관계 : {RELATION_MAP[relation]} " + placeholder
           
        print(f"\n ⌨️ {placeholder}")
        relation = input("👪 관계* : ")
        if not relation: # 입력값이 없는 경우 에러 메세지 출력
            self.print_error("relation_empty")
            continue # 다시 입력 받기
        
        if relation not in RELATION_MAP: # 입력 가능한 값이 아닌 경우 에러 메세지 출력하고
            self.print_error("relation_format")
            continue # 다시 입력받기
        else:
            return relation
  
    def input_address(self, address:str="")->str:
      '''주소입력받기. 필수 입력아니지만, 입력한 경우 100자 유효성 검사'''
      while True:
        placeholder = " 100자 이내로 입력하세요. 입력하지 않으려면 enter만 입력하세요"
        if address: # 기 등록 번호가 있으면 출력해줌
           placeholder = f"현재 주소: {address}"
        print(f"\n ⌨️ {placeholder}")

        address = input("🏠 주소 : ").strip()
        if address:
            if len(address) > 100:
                self.print_error('address_length')
                continue
        return address
    # [end func: input items ] ---------------------------------------------------------      
      
    # [start func : add_member ] -----------------------------------------------------------------------------------
    def add_member(self, menu_no):
      """ 회원 추가 
        유효성 검사
        이름* : 한영 포함 1글자 이상 10자 이내
        전화번호*: 010-0000-0000 (등록만 가능하고 수정 불가)
        관계* : 1,2,3 만 가능 RELATION_MAP = {'1': '❤️ 가족', '2': '🧑‍🤝‍🧑 친구', '3': '🌐 기타'}
        주소 : 안 넣으면 default - 출력하고 입력한 경우 한영숫자 포함 100자 이내
        표시는 필수 입력 항목 임        
      """
      while True:
        self.print_menu_title(menu_no) # 메뉴 타이틀 출력
        print("* 표시된 항목은 반드시 입력하셔야 합니다.")
        name = self.input_name()

        phone = self.input_phone()
        # print(f"📞 반환된 phone 값: {phone} (type: {type(phone)})") # DEBUGING CODE

        if phone == Command.ADD_AGAIN.value: # 중복으로 인해 처음부터 등록 다시 받을 때
          continue 
        elif phone == Command.RETURN_TO_MAIN.value: # 중복으로 인해 메인 메뉴로 돌아간다고 했을 때
          return

        relation = self.input_relation()
        address = self.input_address()

        new_member = Member()
        new_member.add_member_info(phone, name, relation, address)
        self.members.update(new_member.member) # 메모리에 저장
        
        self.save_members() # 파일에 저장

        # 다음 액션(메뉴 돌아가기 혹은 계속 추가하기)
        while True: 
          action_no = input(MESSAGES['actionAfterAddOK'])
          if action_no.lower() == Command.RETURN_TO_MAIN.value: # 메인 메뉴로
              return
          if action_no.lower() != Command.ADD_AGAIN.value : # '<', 'a' 둘다 선택하지 않은 경우 에러 메세지 출력받고 다시 입력받기
              self.print_error("invalid_input")
              continue 
          else:
              break # while 문 빠져나가기 
    # [end func : add_member ] -----------------------------------------------------------------------------------

    # [star func: input_search_keyword() ] ---------------------------------------------------------
    def input_search_keyword(self)->str:
        ''' 검색할 키워드 입력 받아 유효성 검사 후 리턴하는 함수 '''
        while True:
            # 키워드 입력 받고 뒷 space 제거 
            keyword = input(MESSAGES['inputSearchKeyword']).strip()
            
            # 유효성 검사 1. 키워드를 입력하지 않았을때 에러 메세지 출력하고 계속 입력받기
            if not keyword : 
                self.print_error('inpt_keyword')
                continue
            # 유효성 검사 2. 1자 이상 16자 이내로 입력하지 않았을때
            if not (1 <= len(keyword) <= 16): 
                self.print_error('invalid_keyword')
                continue
            # 유효성 검사 3. 한글영숫자 1~16자가 아닌 문자가 있을때(특수문자등)
            if not re.fullmatch(r'[가-힣a-zA-Z0-9]{1,16}', keyword):
                self.print_error('invalid_keyword2')
                continue

            return keyword

    # [star func: search_members() ] ---------------------------------------------------------        
    def search_members(self) -> None:
        ''' 회원목록에서 키워드(전화번호 혹은 이름) 검색하기 '''
        # 검색어 입력받기 
        keyword = self.input_search_keyword()

        # 검색어로 데이터 검색하고 그 결과값 저장하기 
        self.search_results = {
            phone: info
            for phone, info in self.members.items()
            if keyword in phone or keyword in info['name'] # 전화번호 혹은 이름에서 키워드가 있는지
        }
          
    # [star func: search_condition() ] ---------------------------------------------------------    
    def search_condition(self)->bool:       
       ''' 검색어 입력받아 있으면 목록 출력하고 없으면 no data 출력하기 
       back to main 메뉴를 선택하면 return True 반환 아니면 False 
       '''   
       while True: # 올바른 다음 액션 값 받을때까지 반복
        ret_value = False
        # 검색 키워드 입력 받기고 self.members 에서 검색해서 결과를 self.search_results에 저장하기 
        self.search_members()

        # 검색결과가 없는 경우 
        if not self.search_results:                        
            # 검색 결과가 없습니다 출력
            print(MESSAGES["not_found"])

            # 다음 메인메뉴로 갈지 다시 검색할 지 입력 받기 
            action = input(MESSAGES['getActionAfterNoResult']) # < or r 
            if action.lower() == Command.RETURN_TO_MAIN.value: # MainMenu로 돌아가기
                return True
            elif action.lower() == Command.SEARCH_AGAIN.value: # 다시 검색하기로 가기 
                continue
            else: # < or r 이 아닌 값 입력한 경우 
                self.print_error('invalid_input')
                continue
        else: 
            # 검색어가 있는 경우 검색 목록 출력하기 
            self.print_member_list(self.search_results)   
            return False # 다음 계속 진행 하기 
       
    # [start func : update_member ] -----------------------------------------------------------------------------------
    def update_member(self, menu_no):
        """검색 키워드를 입력받아 목록 조회 후 수정 회원 번호 선택하여 해당 회원 정보 수정하기
          param : menu_no 메뉴 번호 
        """
        # 검색 후 다시 수정할 수 있어 메인 메뉴로 돌아가기 전까지 반복         
        while True:
            self.print_menu_title(menu_no) # 메뉴 타이틀 출력   

            # 검색어 입력받아 검색 목록 출력하기 호출 
            ret_value = self.search_condition() 
            if ret_value: #검색 조건에서 메인 메뉴로 돌아가기로 한 경우
               return

            # 검색한 목록에서 수정할 번호 혹은 메인 메뉴로 돌아가기 액션번호 유효한 값 입력받기
            while True:
              print() # 한줄 띠우기
              action_no = input(f"✏️ 수정할 번호를 입력하거나,  🔙 메인 메뉴로 돌아가려면 '<'을 입력하세요: ").strip()
              if action_no.lower() == Command.RETURN_TO_MAIN.value: 
                  return
              # 수정 번호 받은 경우 
              try:
                  # action_no 를 숫자로 변경
                  selected_num = int(action_no) 
                  # 입력받은 번호가 출력한 번호 안에 있는지 확인하기
                  if 1 <= selected_num <= len(self.search_results): # 출력한 범위안에 있으면
                      results_list = list(self.search_results.items()) # index 번호로 정보 찾기 위해 데이터 변환 
                      phone, member = results_list[selected_num - 1] # 출력시 1부터 시작했으니 -1 해주기 
                      # 항목 입력 받고 저장하기 
                      ret_value = self.edit_info(phone, member)
                      if ret_value : # 저장 성공시 
                        # 다음 액션 받기
                        continue_edit = False
                        while True: 
                            action = input(MESSAGES['getActionAfterEditOK']).strip() # 입력 받고 공백제거
                            if action.lower() == Command.RETURN_TO_MAIN.value: # '<' 입력받아 메인 메뉴로 
                                return
                            elif action.lower() == Command.EDIT_AGAIN.value : # 다시 수정하기 선택시 
                                continue_edit = True
                                break
                            else:  # '<', 'e' 둘다 선택하지 않은 경우 에러 메세지 출력받고 다시 입력받기
                                self.print_error("invalid_input")
                                continue  # action를 다시 입력받기
                        # // 다음 액션 받기 끝 
                        if continue_edit:  # 다시 수정 시작할때
                            break  
                      else: # 에러 발생시 
                        return
                  # 출력하지 않은 번호 입력시 에러 출력
                  else: 
                    self.print_error('invalid_number')
                    continue
              except ValueError: # 숫자가 아닌 경우
                self.print_error('input_num_only')
                continue
    # [end func: update_member ] -----------------------------------------------------------------------------------

    # [start func: edit_info ] -----------------------------------------------------------------------------------
    def edit_info(self, phone:str, member:dict)->bool:        
        '''회원정보 각 항목별로 입력받아 저장하기 
        param: phone - 전화번호(key)
               member - 수정한 한 사람의 정보가 들어 있는 dictionary data
        '''
        # 수정할 항목 입력 받기 타이틀 출력 
        self.print_menu_title('edit') # 타이틀 출력
        # 전화번호는 수정할 수 없으니 그냥 출력해 주기 
        print(f"\n{'📞 전화번호':<10}: {phone} (전화번호는 변경할 수 없습니다.)")
        # 이름, 관계, 주소 유효한 값만 입력 받기
        new_name = self.input_name(member['name'])
        new_relation = self.input_relation(member['relation'])
        new_address = self.input_address(member['address'])

        # 정상적으로 입력 받았으면 정보 수정하기
        try:
          if phone in self.members: # just in case
            self.members[phone].update({
                'name': new_name,
                'relation': new_relation,
                'address': new_address,
                'regDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            self.print_bar()
            print(f"{'👤 이름':<12}: {new_name}")
            print(f"{'📞 전화번호':<10}: {phone}")
            print(f"{'👪 관계':<12}: {RELATION_MAP[new_relation]}")
            print(f"{'🏠 주소':<12}: {new_address}")
            print(f"{'🕒 등록일':<11}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")            
            self.print_bar()
            self.save_members('수정')
            return True
        except Exception as e:
            self.print_error('something_wrong') 
            print(f"🛠️ 상세 정보: {e}")
            return False
    # [end func: edit_info ] -----------------------------------------------------------------------------------
        
    # [start func: remove_member] --------------------------------------------------------------------------------
    def remove_member(self, menu_no):
        """회원 검색한 후 삭제하기"""
        # 검색 후 다시 삭제할 수 있어 메인 메뉴로 돌아가기 전까지 반복         
        while True:
            self.print_menu_title(menu_no) # 메뉴 타이틀 출력    

            # 검색어 입력받아 검색 목록 출력하기 호출 
            ret_value = self.search_condition() 
            if ret_value: #검색 조건에서 메인 메뉴로 돌아가기로 한 경우
               return

            # 검색한 목록에서 수정할 번호 혹은 메인 메뉴로 돌아가기 액션번호 입력받기
            while True:
              print() # 한줄 띄우기 
              action_no = input(MESSAGES['inputNumber4DelOrBack2Menu']).strip()
              if action_no.lower() == Command.RETURN_TO_MAIN.value: # 메인 메뉴로 돌아가기 선택한 경우
                  return                
              
              try:
                # action_no 를 숫자로 변경
                selected_num = int(action_no) # 여기서 문자 받으면 try 로 잡아냄..

                # 입력받은 번호가 출력한 번호 안에 있는지 확인하기
                if 1 <= selected_num <= len(self.search_results): # 출력한 범위안에 있으면                 

                  # 삭제 confirm 받기 
                  while True:  
                    print() # 한 줄 띄우기                    
                    del_yn = input(MESSAGES['delete_confirm']).strip()
                    if del_yn.lower() == 'y': # 삭제하기  
                        results_list = list(self.search_results.items()) # 데이
                        phone2del, member = results_list[selected_num - 1] # 출력시 1부터 시작했으니 -1 해주기 

                        # 삭제 저장하고 메세지 출력하기 
                        del self.members[phone2del]
                        self.save_members('삭제')

                        # 다음 액션 받기
                        while True: 
                          action = input(MESSAGES['getActionAfterDelOK']).strip() # 입력 받고 공백제거
                          ret_value = False
                          if action.lower() == Command.RETURN_TO_MAIN.value: # < 입력받은 경우
                              return
                          elif action_no.lower() == Command.DEL_AGAIN.value : # 다시 삭제하기 선택시 
                            ret_value = True
                            break
                          else: # '<', 'e' 둘다 선택하지 않은 경우 에러 메세지 출력받고 다시 입력받기
                                self.print_error("invalid_input")
                                continue  # action를 다시 입력받기
                        # // while True 끝
                        if ret_value : break # 다시 검색하로 가기 
                    else: # confirm에서 'Y'가 아닌 경우 바로 메뉴로 돌아가기 
                       return
                         
                else: # 출력하지 않은 번호 입력시 에러 출력
                  self.print_error('invalid_number')
                  continue
              except ValueError: # 숫자가 아닌 경우
                  self.print_error('input_num_only')
                  continue

    # [end func : remove_member ] -----------------------------------------------------------------------------------

# [start func : main() ] -----------------------------------------------------------------------------------
def main():
    """ 메인 루프 """
    manager = MemberManager(DATA_FILE)
    while True:
        inputed_mno = manager.display_main_menu() # 입력받은 메뉴 번호 확인하기 
        if inputed_mno == '1':
            manager.list_members(inputed_mno)            
        elif inputed_mno == '2':
            manager.add_member(inputed_mno)
        elif inputed_mno == '3':
            manager.update_member(inputed_mno)
        elif inputed_mno == '4':
            manager.remove_member(inputed_mno)
        elif inputed_mno == '5':
             # print(MESSAGES['exit_confirm'] + " 상단 입력란에 입력하세요.") # for ipynb testing
             # confirm = input(MESSAGES["exit_confirm"]) # 종료 확인 여부 입력 받기
             confirm = 'y' # for  the test
             if confirm.lower() == 'y': # 최종 종료 선택
                manager.save_members()
                print("프로그램을 종료합니다.............")
                return
        else:
            manager.print_error("invalid_input")                
# [end func : main() ] -----------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
