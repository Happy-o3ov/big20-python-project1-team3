"""
회원관리 프로그램
1. 목록출력 - 저장된 회원정보들 출력
2. 회원추가 - 이름(한영1~5자), 전화번호(010-****-**** | 010********)
            , 관계 (가족,친구,기타), 주소(100자 이내)
3. 회원수정 - 기존 회원 정보 수정
4. 회원삭제 - 기존 회원 삭제
5. 종료     - 데이터 저장 후 프로그램 종료
"""
import pickle
import os
import re

class Members:
    """
    멤버 관리 클래스
    
    member_dict 
        : 멤버정보 보관 딕셔너리. PK = 번호
            {
                phone_number1: {'name' : name, 'relation' : relation},
                phone_number2: {'name' : name, 'relation' : relation}
            }
    
    __init__ (self)
        : 바이너리파일 데이터로 member_dict 초기화
    get(self)
        : 멤버 반환
    add(self, 이름, 번호, 관계)
        : 멤버 추가
    set(self, 이름, 수정전 번호, 수정후 번호, 이름, 관계)
        : 멤버 정보 수정
    del_member(self, 번호)
        : 멤버 삭제, 삭제된 멤버정보 딕셔너리로 반환
    search_member
        : 멤버 검색, 검색된 멤버들을 딕셔너리로 반환
    read_data(self)
    : 파일의 데이터를 읽어 반환
    duplicate_num_check(self, num: str)
        : 번호 중복 검사
    save_data(self)
        : member_dict을 바이너리파일 데이터로 저장
    _write_data(data)
        : 넘겨받은 data를 파일에 저장
 
    """


    def __init__(self) -> None:
        """
        members.dat 파일에 저장된 데이터로 member_dict 초기화
        """
        self.member_dict = self.read_data()


    def get(self) -> dict:
        """member_dict 반환"""
        return self.member_dict


    def add(self, phone_number: str, name: str, relation: str, address: str = "") -> None:
        """
        member_dict 정보 추가
        
        phone_number : 
        PK = phone_number
        """

        # 정규식 유효성 검사
        regular_num_check(phone_number)
        self.duplicate_num_check(phone_number)
        regular_name_check(name)
        lel_check(relation)
        if address:
            regular_address_check(address)

        # 정보 추가
        self.member_dict[phone_number] = {'name' : name, 'relation' : relation, 'address': address}


    def set(self, old_num: str, new_num: str, name: str, relation: str, address: str = "") -> None:
        """
        member_dict 정보 수정
        
        이전번호를 조회하여, 기존사용자의 정보를 찾아 수정
        """
        # 정규식 유효성 검사
        regular_num_check(old_num)
        regular_num_check(new_num)
        regular_name_check(name)
        lel_check(relation)
        if address:
            regular_address_check(address)

        # 이전번호에 해당하는 번호가 없을 경우
        if old_num not in self.member_dict.keys():
            raise KeyError('해당하는 사용자를 찾을 수 없습니다')

        # 번호만 그대로면(이전번호==수정번호), 이름과 관계만 수정
        # 수정된 번호가 다른 사용자의 번호와 같으면 에러발생(duplicate_num_check 중복체크함수)
        if old_num == new_num:
            self.member_dict[new_num].update({
                'name' : name, 
                'relation' : relation, 
                'address' : address
                })
            return

        # 검색된 사용자 외 사용중인 번호인지 확인
        self.duplicate_num_check(new_num)

        #수정된 정보가 모두 다를경우, 기존 정보 삭제 후 새로 생성
        self.del_member(old_num)
        self.add(new_num,name,relation,address)


    def del_member(self,phone_num: str) -> dict:
        """ 멤버정보 삭제, 반환(pop)"""
        if phone_num in self.member_dict.keys():
            return self.member_dict.pop(phone_num)


    def search_member(self,input_str: str) -> dict:
        """
        멤버 검색
        
        input_str : 이름 혹은 전화번호 문자열
        검색된 멤버를 search_dict에 저장
        search_dict 혹은 None 반환 
        """
        # 검색과 일치하는 이름/번호 찾기, 해당하는 정보를 search_dict에 저장
        search_dict = {}
        for key, value in self.member_dict.items():
            name = value['name']
            if input_str in key or input_str in name:
                search_dict[key] = value

        # 검색결과 반환
        if search_dict:
            return search_dict
        else:
            raise KeyError('해당하는 사용자를 찾을 수 없습니다')


    def read_data(self) -> dict:
        """
        ./data 폴더와 members.dat 파일이 없으면 생성,
        있으면 파일을 읽어 딕셔너리 반환.
        """
        # 폴더생성
        if not os.path.exists('./data'):
            os.mkdir('./data')

        # 파일 있으면 로드, 없으면 빈 객체가 있는 파일생성
        if os.path.exists('./data/members.dat'):
            with open('./data/members.dat', 'rb') as data_file:
                return pickle.load(data_file)
        # 빈 파일에 빈 데이터 저장
        else:
            data = {}
            self._write_data(data)
            return data

    def duplicate_num_check(self, phone_num: str) -> None:
        """번호 중복 여부 검사
        
        phone_num : 새로 추가/수정될 번호를 받아 중복검색
        search_member 는 일부분검색, duplicate는 PK(전화번호) 일치 확인
        """

        if phone_num in self.member_dict:
            raise KeyError(f"{phone_num} 는 이미 등록된 번호입니다.")

    def save_data(self) -> None:
        """이진파일로 멤버객체 저장"""
        self._write_data(self.member_dict)


    def _write_data(self,data: dict) -> None:
        """
        데이터를 받아 파일에 저장
        
        data : 저장된 데이터(회원정보) 혹은 빈 객체(새로 생성된 빈파일 초기화)
        """
        with open('./data/members.dat','wb') as data_file:
            pickle.dump(data, data_file)


def regular_name_check(name: str) -> None:
    """
    이름 유효성 검사
    
    name : 입력받은 사용자이름 문자열
    """
    if not re.fullmatch(r'[가-힣a-zA-Z]{1,5}', name):
        raise ValueError('이름 형식이 올바르지 않습니다.')

def regular_num_check(num: str) -> str:
    """
    번호 유효성 검사
    
    num : 입력받은 전화번호 문자열
    010 고정, 번호만 있을 시 '-' 추가
    [-]가 포함된 전화번호 문자열 반환
    """
    if re.fullmatch(r'010\d{8}',num):
        return f'{num[0:3]}-{num[3:7]}-{num[7:]}'
    if not re.fullmatch(r'010-\d{4}-\d{4}', num):
        raise ValueError('번호 형식이 올바르지 않습니다.')
    return num

def lel_check(rel: str) -> str:
    """관계 유효성 검사
    rel : 입력받은 관계 문자열
    번호 입력시 관게이름으로 대체
    가족, 친구, 기타 중 해당되는 문자열로 반환
    """
    if rel in('1','가족'):
        return '가족'
    if rel in('2','친구'):
        return '친구'
    if rel in('3','기타'):
        return '기타'
    raise ValueError('관계 형식이 올바르지 않습니다.')

def regular_address_check(address: str) -> None:
    """
    주소 유효성 검사
    address : 입력받은 주소 문자열, 100자이내
    """
    if not re.fullmatch(r'^.{1,100}$', address):
        raise ValueError('주소 형식이 올바르지 않습니다.')

def show_menu() -> None:
    """메뉴출력"""

    prompt = """
    1. 연락처 목록
    2. 연락처 추가
    3. 연락처 수정
    4. 연락처 삭제
    5. 종료
    """
    print('=' * 30)
    print(prompt)
    print('=' * 30)


def list_member(members: dict) -> None:
    """
    멤버데이터 딕셔너리를 받아 정보 출력
    dict = {전화번호 : {'name':'사용자이름', 'relation':'관계}}
    한글 간격 조절
    """
    if not members:
        print('저장된 사용자가 없습니다.')
        input_member('[<]버튼을 눌러 종료')
        return
    
    print(f"{'No.'}| {'이름':<8} | {'전화번호':<11} | {'관계':<3} | {'주소'}")
    print("-" * 80)
    list_number = 0
    for key,value in members.items():
        list_number += 1
        if re.fullmatch(r'[가-힣]+', value['name']):
            name_width = 10 - len(value['name'])
        else:
            name_width = 10
        print(
            f"{list_number:>2} | "
            f"{value['name']:<{name_width}} | "
            f"{key:<15} | "
            f"{value['relation']:<3} | "
            f"{value['address']}"
        )
    print("-" * 80)

def is_return_menu(user_input: str) -> bool:
    """입력 중단 체크"""
    return user_input == "<"

def show_member_menu(members: dict):
    """
    목록출력 메뉴
    list_member에서 데이터 출력, [<]를 눌러 종료
    """
    list_member(members)
    while True:
        try:
            return_menu = input('메뉴돌아가기[<] : ')
            if not is_return_menu(return_menu):
                raise ValueError('잘못된 입력입니다.')
            return
        except ValueError as e:
            print(e)

def input_member(prompt: str, check_func = None, empty_pass = False):
    """
    회원추가/수정에 사용되는 정보입력함수
    pormpt: input시 출력될 안내메시지
    check_func : 유효성 검사 함수(정규식:(이름, 번호, 주소), 비정규식: 관계)
    empty_pass : 미 입력시(엔터), 이전정보 유지기능 활성화
    """
    while True:
        try:
            user_input = input(prompt)
            if is_return_menu(user_input):      #[<] 키 입력시 종료
                return None
            if empty_pass and user_input == "": # 이전정보 유지 활성화, 엔터키 입력시 그대로 반환
                return ""
            if check_func:                      # 유효성 검사 실행함수가 있으면 문자열 검사
                checked_data = check_func(user_input)
                if checked_data is not None:
                    return checked_data
            return user_input
        except (ValueError, KeyError) as e:     # 잘못된 입력 시 메시지 출력 후 재실행
            print(e)

def add_member_menu(members: Members) -> bool:
    """
    사용자 추가 메뉴
    
    input_member함수로 정보를 입력받음
    """


    add_name = input_member(                    # 이름 입력, 유효성검사 (검사: regular_name_check)
        '이름 입력: 한/영 1자이상 5자 이내 (메뉴돌아가기[<]) : ',
        check_func = regular_name_check
    )
    if add_name is None:                        # [<] 입력시 종료
        return False

    add_num = input_member(                     # 전화번호 입력, 유효성검사 (검사: regular_num_check)
        '번호 입력: 010-0000-0000 (메뉴돌아가기[<]) : ',
        check_func=regular_num_check
    )
    if add_num is None:                         # [<] 입력시 종료
        return False
    if add_num in members.member_dict.keys():   # 전화번호 중복검사
        print("이미 추가되어 있는 번호입니다.")
        return True

    add_rel = input_member(                     # 관계 입력, 유효성검사 (검사: lel_check)
        '관계 입력 선택(1.가족 2.친구 3.기타) (메뉴돌아가기[<]) : ',
        check_func=lel_check
    )
    if add_rel is None:                         # [<] 입력시 종료
        return False

    add_address = input_member(
        '주소 입력 (100자 이내, 생략 가능, 메뉴돌아가기[<]) : ',
        check_func = regular_address_check,
        empty_pass = True
    )
    if add_address is None:
        return False
    if add_address == "":
        add_address = ""

    members.add(add_num,add_name,add_rel,add_address)       # 입력받은 정보 추가
    print("\n추가 완료!")
    list_member({add_num: {'name': add_name, 'relation': add_rel, 'address': add_address}})
    return True

def set_member_menu(members:Members) -> bool:
    """
    사용자 수정 메뉴
    
    input_member함수로 정보를 입력받음
    미입력 상태로 엔터 시 정보 유지
    """
    searched_dict = {}    # 검색된 정보를 담을 객체 생성
    while True:
        # 번호입력, [<] : 종료
        search = input_member('수정할 사용자 이름/전화번호 검색, (메뉴돌아가기[<1]) : ')
        if search is None:
            return False
        try:
            searched_dict = members.search_member(search)       # 사용자 검색
            break
        except KeyError as e:
            print(e)

    old_num, old_name, old_rel = None, None, None                 # 사용자 이전정보
    while True:
        # 수정할 정보 선택
        list_member(searched_dict)                          # 검색된 목록 출력
        select_num = input_member('수정할 사용자 번호(No.) 입력 (메뉴돌아가기[<]) : ')
        if select_num is None:
            return False
        count = 0

        # 번호에 해당하는 정보 저장
        for key, value in searched_dict.items():
            count += 1
            if select_num == str(count):
                old_num = key
                old_name = value['name']
                old_rel = value['relation']
                old_address = value['address']

                break
        # 검색 정보가 저장되면 검색/선택 종료
        if old_num:
            break
        print(f'해당하는 번호(1~{count})를 입력해주세요')


    # 수정할 이름 입력
    new_name = input_member(
        f'새 이름 입력 (현재: {old_name}) 엔터=유지, 메뉴돌아가기[<]) : ',
        check_func=regular_name_check,
        empty_pass=True
    )
    if new_name is None:
        return False
    if new_name == "":
        new_name = old_name

    # 수정할 전화번호 입력
    while True:
        new_num = input_member(
            f'새 번호 입력 (현재: {old_num}) 예: 010-0000-0000, 엔터=유지, 메뉴돌아가기[<]) : ',
            check_func = regular_num_check,
            empty_pass = True
        )
        if new_num is None:
            return False
        if new_num == "":
            new_num = old_num
            break

        try:
            if new_num != old_num:      # 새 번호가 다른 사용자의 번호인지 확인
                members.duplicate_num_check(new_num)
            break
        except KeyError as e:
            print(e)

    # 수정할 관계 입력
    new_rel = input_member(
        f'새 관계 입력 (현재: {old_rel}) 1.가족 2.친구 3.기타, 엔터=유지, 메뉴돌아가기[<]) : ',
        check_func = lel_check,
        empty_pass = True
    )
    if new_rel is None:
        return False
    if new_rel == "":
        new_rel = old_rel

    new_address = input_member(
        f'새 주소 입력 (현재: {old_address}) 엔터=유지, 메뉴돌아가기[<]) : ',
        check_func = regular_address_check,
        empty_pass = True
    )
    if new_address is None:
        return False
    if new_address == "":
        new_address = old_address

    # 입력받은 정보로 수정
    try:
        members.set(old_num, new_num, new_name, new_rel, new_address)
        print("\n수정 완료!")
        list_member({new_num: {'name': new_name, 'relation': new_rel, 'address': new_address}})
    except (ValueError, KeyError) as e:
        print(e)

    return True

def del_member_menu(members: Members) -> bool:
    """
    사용자 삭제 메뉴
    
    """
    searched_dict={}    # 검색된 정보를 담을 객체 생성
    while True:
        # 번호입력, [<] : 종료
        search = input_member('삭제할 사용자 이름/전화번호 검색, (메뉴돌아가기[<]) : ')
        if search is None:
            return False
        try:
            searched_dict = members.search_member(search)       # 사용자 검색
            break
        except KeyError as e:
            print(e)

    while True:
        # 삭제할 정보 선택
        list_member(searched_dict)                          # 검색된 목록 출력
        select_num = input_member('삭제할 사용자 번호(No.) 입력 (메뉴돌아가기[<]) : ')
        if select_num is None:
            return False
        count = 0
        deleted_data = None
        # 번호에 해당하는 정보 저장
        for key in searched_dict.keys():
            count += 1
            if select_num == str(count):
                check_again = input("정말로 삭제하시겠습니까? (삭제:y 취소: any key) ")
                if check_again != 'y':
                    break
                deleted_data = members.del_member(key)
                print('삭제완료')
                list_member({key: deleted_data})

        # 삭제된 데이터가 있으면 번호입력 종료
        if deleted_data:
            break
        print(f'해당하는 번호(1~{count})를 입력해주세요')

    return True


def main():
    """메인메뉴 실행"""
    member_dict = Members()
    # 테스트 코드
    # member_dict.add('010-1111-2222','홍길동','가족','서울 강남구 강남대로 78길 8')
    # member_dict.add('010-3333-4444','짱구','친구')
    # member_dict.add('010-9876-9876','일론머스크','기타','미국,캐나다,남아공')
    # member_dict.add('010-1234-1234','리사수','친구','대만')
    # member_dict.add('010-4646-4646','고길동','기타')
    # member_dict.add('010-1579-3131','Im','가족')

    while True:
        show_menu()
        input_number = input('1~5 버튼입력: ')

        # 연락처 목록
        if input_number == '1':
            show_member_menu(member_dict.get())

        # 연락처 추가
        elif input_number == '2':
            while True:
                if not add_member_menu(member_dict):
                    break
                cont = input("\n다른 연락처도 추가하시겠습니까? (확인:y 취소:any key): ")
                if cont != 'y':
                    break

        # 연락처 수정
        elif input_number == '3':
            while True:
                if not set_member_menu(member_dict):
                    break
                cont = input("\n다른 연락처도 수정하시겠습니까? (확인:y 취소:any key): ")
                if cont != 'y':
                    break

        # 연락처 삭제
        elif input_number == '4':
            while True:
                if not del_member_menu(member_dict):
                    break
                cont = input("\n다른 연락처도 삭제하시겠습니까? (확인:y 취소:any key): ")
                if cont != 'y':
                    break

        # 종료
        elif input_number == '5':
            member_dict.save_data()   # 종료 전에 저장
            break

if __name__ == "__main__":
    main()
