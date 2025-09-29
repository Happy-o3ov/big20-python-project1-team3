

import pickle # 데이터(예: 리스트, 딕셔너리, 클래스 등)를 저장하거나 불러올 때 사용
import os # 파일이 존재하는지 확인, 디렉토리 만들기, 파일 삭제 작업
import re # 전화번호, 이름 등 입력 검사하기

DATA_FILE = '../data/members.dat' # 데이터 파일 경로 설정 - 상수 적용

class MemberManagementSystem: # 클래스 선언
    
    def __init__(self, filename=DATA_FILE): # 생성자, 자기 자신을 참조 매개변수(데이터 받는놈)
        """클래스 초기화 - 회원 데이터를 딕셔너리로 관리"""
        self.members = {}  # 회원 데이터 저장 딕셔너리 (key: 전화번호, value: 회원정보)
        self.filename = filename # 바이너리 파일명
        
        # 디렉토리가 없으면 자동 생성
        directory = os.path.dirname(self.filename) # 파일 경로에서 디렉토리 부분 추출
        if directory and not os.path.exists(directory): # 디렉토리가 존재하지 않으면
            os.makedirs(directory) # 디렉토리 생성
    
    # ============================================================================
    # 메인 시스템 및 파일 관리 기능
    # ============================================================================
    
    def load_data(self):
        """프로그램 시작 시 바이너리 파일에서 데이터 읽기"""
        try: # 예외 처리 시작
            if os.path.exists(self.filename): # 파일이 존재하는지 확인
                with open(self.filename, 'rb') as file: # 파일을 바이너리 읽기 모드로 열기
                    data = pickle.load(file) # pickle로 데이터 로드
                    
                    # 이전 리스트 버전과의 호환성을 위한 데이터 변환
                    if isinstance(data, list): # 기존 리스트 형태의 데이터인 경우
                        self.members = {} # 딕셔너리로 초기화
                        for member in data: # 리스트의 각 회원 데이터를 순회
                            phone = member['phone'] # 전화번호를 키로 사용
                            self.members[phone] = member # 딕셔너리에 저장
                    else: # 이미 딕셔너리 형태인 경우
                        self.members = data # 그대로 사용
                        
                print(f"기존 데이터 {len(self.members)}개를 불러왔습니다.") # 로드 완료 메시지
            else: # 파일이 존재하지 않는 경우
                print("새로운 데이터 파일을 생성합니다.") # 새 파일 생성 메시지
                self.members = {} # 빈 딕셔너리로 초기화
        except Exception as e: # 예외가 발생한 경우
            print(f"데이터 읽기 오류: {e}") # 오류 메시지 출력
            self.members = {} # 빈 딕셔너리로 초기화
    
    def save_data(self):
        """프로그램 종료 시 바이너리 파일로 데이터 저장"""
        try: # 예외 처리 시작
            with open(self.filename, 'wb') as file: # 파일을 바이너리 쓰기 모드로 열기
                pickle.dump(self.members, file) # 딕셔너리를 pickle로 저장
            print("데이터가 저장되었습니다.") # 저장 완료 메시지
            return True # 성공 반환
        except Exception as e: # 예외가 발생한 경우
            print(f"데이터 저장 오류: {e}") # 오류 메시지 출력
            return False # 실패 반환
    
    def show_menu(self):
        """메인 메뉴 출력"""
        print("\n" + "="*50) # 구분선 출력
        print("           회원관리 시스템") # 시스템 제목
        print("="*50) # 구분선 출력
        print("1. 목록 출력") # 메뉴 항목 1
        print("2. 회원 추가") # 메뉴 항목 2
        print("3. 회원 수정") # 메뉴 항목 3
        print("4. 회원 삭제") # 메뉴 항목 4
        print("5. 종료") # 메뉴 항목 5
        print("="*50) # 구분선 출력
    
    def get_menu_choice(self):
        """메뉴 선택 입력 및 검증"""
        while True: # 올바른 선택을 할 때까지 반복
            try: # 예외 처리 시작
                choice = input("메뉴를 선택하세요 (1-5): ").strip() # 사용자 입력 받기
                if choice in ['1', '2', '3', '4', '5']: # 유효한 선택인지 확인
                    return int(choice) # 정수로 변환하여 반환
                else: # 유효하지 않은 선택인 경우
                    print("1-5 사이의 번호를 입력해주세요.") # 안내 메시지
            except: # 예외가 발생한 경우
                print("올바른 번호를 입력해주세요.") # 오류 메시지
    
    # ============================================================================
    # 1. 목록 출력 기능
    # ============================================================================
    
    def display_members(self):
        """1번 - 목록 출력 기능"""
        # 저장된 데이터 존재 여부 확인
        if not self.members: # 회원 딕셔너리가 비어있는 경우
            print("\n저장된 데이터가 없습니다.") # 데이터 없음 메시지
            input("엔터를 눌러 메뉴로 돌아가세요...") # 사용자 입력 대기
            return # 함수 종료
        
        while True: # 메뉴로 나갈 때까지 반복
            # 회원 목록 출력
            print(f"\n{'='*80}") # 상단 구분선
            print("                           회원 목록") # 제목
            print(f"{'='*80}") # 구분선
            print(f"{'순번':<4} {'이름':<10} {'전화번호':<15} {'관계':<8} {'주소':<30}") # 테이블 헤더
            print(f"{'-'*80}") # 테이블 구분선
            
            # 딕셔너리 순회하여 회원 정보 출력 (추가 순서대로)
            for i, (phone, member) in enumerate(self.members.items(), 1): # 딕셔너리 항목 순회
                relation_name = self.get_relation_name(member['relation']) # 관계 코드를 이름으로 변환
                # 주소가 너무 길면 잘라서 표시
                address_display = member['address'][:27] + "..." if len(member['address']) > 30 else member['address']
                # 각 회원 정보를 한 줄씩 출력
                print(f"{i:<4} {member['name']:<10} {member['phone']:<15} "
                      f"{relation_name:<8} {address_display:<30}")
            
            print(f"{'-'*80}") # 하단 구분선
            print(f"총 회원 수: {len(self.members)}명") # 총 회원 수 표시
            print(f"{'='*80}") # 마지막 구분선
            
            # 메뉴로 나가기 확인
            print("\n메뉴로 나가겠습니까?") # 나가기 확인 메시지
            choice = input("선택하세요 (예/아니오): ").strip() # 사용자 입력 받기
            
            if choice == "예": # 예 선택시
                break # 반복문 종료하여 메뉴로 복귀
            elif choice == "아니오": # 아니오 선택시
                continue # 반복하여 다시 목록 표시
            else: # 잘못된 입력인 경우
                print("'예' 또는 '아니오'를 입력해주세요.") # 안내 메시지
    
    def get_relation_name(self, relation_code):
        """관계 코드를 관계명으로 변환"""
        relation_map = {1: "가족", 2: "친구", 3: "기타"} # 관계 코드 매핑 딕셔너리
        return relation_map.get(relation_code, "기타") # 코드에 해당하는 이름 반환, 없으면 "기타"
    
    # ============================================================================
    # 2. 회원 추가 기능
    # ============================================================================
    
    def add_member(self):
        """2번 - 회원 추가 기능"""
        print("\n=== 회원 추가 ===") # 기능 제목 출력
        
        # 이름 입력 (나가기 기능 포함)
        name = self.get_name_input("추가") # 이름 입력 함수 호출
        if name is None:  # 나가기 선택한 경우
            return # 함수 종료
        
        # 전화번호 입력 및 중복 검사
        phone = self.get_phone_input() # 전화번호 입력 함수 호출
        if phone is None:  # 오류 발생한 경우
            return # 함수 종료
        
        # 관계 선택 (확인 단계 포함)
        relation = self.get_relation_input() # 관계 선택 함수 호출
        if relation is None:  # 오류 발생한 경우
            return # 함수 종료
        
        # 주소 입력 (선택사항)
        address = self.get_address_input() # 주소 입력 함수 호출
        
        # 회원 데이터를 딕셔너리로 생성
        member = {
            'name': name, # 이름
            'phone': phone, # 전화번호  
            'relation': relation, # 관계
            'address': address # 주소
        }
        
        # 딕셔너리에 추가 (전화번호를 키로 사용)
        self.members[phone] = member # 전화번호를 키로 하여 회원 정보 저장
        print("\n저장완료 - 회원이 성공적으로 추가되었습니다!") # 완료 메시지
        input("엔터를 눌러 메뉴로 돌아가세요...") # 사용자 입력 대기
    
    def get_name_input(self, action="입력"):
        """이름 입력 및 검증 (나가기 기능 포함)"""
        while True: # 올바른 이름을 입력할 때까지 반복
            # 사용자에게 이름 입력 요청
            name = input(f"\n{action}할 회원의 이름을 입력하세요 (나가기: 메뉴로 돌아가기): ").strip()
            
            # 나가기 기능 처리
            if name == "나가기": # 나가기 입력한 경우
                choice = input("메뉴 선택으로 나가겠습니까? (예/아니오): ").strip() # 나가기 확인
                if choice == "예": # 예 선택시
                    return None # None 반환하여 나가기 표시
                elif choice == "아니오": # 아니오 선택시
                    continue # 반복하여 다시 이름 입력
                else: # 잘못된 입력인 경우
                    print("'예' 또는 '아니오'를 입력해주세요.") # 안내 메시지
                    continue # 반복
            
            # 이름 유효성 검사 (한영 5자 이내)
            if self.validate_name(name): # 이름이 유효한 경우
                return name # 이름 반환
            else: # 이름이 유효하지 않은 경우
                print("이름은 한글/영문으로 5자 이내로 입력해주세요.") # 안내 메시지
    
    def validate_name(self, name):
        """이름 유효성 검사"""
        if not name: # 이름이 비어있는 경우
            return False # 유효하지 않음
        # 정규식 패턴: 한글 또는 영문 1-5자
        pattern = r'^[가-힣a-zA-Z]{1,5}$'
        return bool(re.match(pattern, name)) # 패턴 매칭 결과 반환
    
    def get_phone_input(self):
        """전화번호 입력 및 검증"""
        while True: # 올바른 전화번호를 입력할 때까지 반복
            phone = input("전화번호를 입력하세요 (010-0000-0000 형식): ").strip() # 사용자 입력
            
            # 전화번호 형식 검증
            if not self.validate_phone_format(phone): # 형식이 올바르지 않은 경우
                print("전화번호 형식이 올바르지 않습니다. (예: 010-1234-5678)") # 오류 메시지
                continue # 다시 입력
            
            # 중복 검사 (딕셔너리 키 확인)
            if phone in self.members: # 이미 존재하는 전화번호인 경우
                print("중복된 번호입니다. 다른 번호를 입력해주세요.") # 중복 메시지
                continue # 다시 입력
            
            return phone # 유효한 전화번호 반환
    
    def validate_phone_format(self, phone):
        """전화번호 형식 검증 (010-0000-0000)"""
        # 정규식 패턴: 숫자3자리-숫자4자리-숫자4자리
        pattern = r'^010-\d{4}-\d{4}$'
        return bool(re.match(pattern, phone)) # 패턴 매칭 결과 반환
    
    def get_relation_input(self):
        """관계 선택 (확인 단계 포함)"""
        while True: # 올바른 관계를 선택할 때까지 반복
            print("\n관계를 선택하세요:") # 관계 선택 안내
            print("1. 가족") # 선택지 1
            print("2. 친구") # 선택지 2
            print("3. 기타") # 선택지 3
            
            choice = input("번호를 선택하세요 (1-3): ").strip() # 사용자 선택 입력
            
            if choice not in ['1', '2', '3']: # 유효하지 않은 선택인 경우
                print("1, 2, 3 중에서 선택해주세요.") # 안내 메시지
                continue # 다시 선택
            
            # 선택 확인 단계
            relation_names = {'1': '가족', '2': '친구', '3': '기타'} # 선택지 매핑
            relation_name = relation_names[choice] # 선택한 관계 이름
            
            confirm = input(f"{choice}번({relation_name})으로 선택하겠습니까? (예/아니오): ").strip() # 확인 입력
            
            if confirm == "예": # 예 선택시
                return int(choice) # 선택한 번호를 정수로 반환
            elif confirm == "아니오": # 아니오 선택시
                continue # 반복하여 다시 선택
            else: # 잘못된 입력인 경우
                print("'예' 또는 '아니오'를 입력해주세요.") # 안내 메시지
    
    def get_address_input(self):
        """주소 입력 및 검증"""
        while True: # 올바른 주소를 입력할 때까지 반복
            address = input("주소를 입력하세요 (100자 이내, 선택사항): ").strip() # 사용자 입력
            
            if len(address) <= 100: # 100자 이내인 경우
                return address if address else "주소 미입력" # 입력값 또는 기본값 반환
            else: # 100자 초과인 경우
                print("주소는 100자 이내로 입력해주세요.") # 안내 메시지
    
    # ============================================================================
    # 3. 회원 수정 기능
    # ============================================================================
    
    def edit_member(self):
        """3번 - 회원 수정 기능"""
        print("\n=== 회원 수정 ===") # 기능 제목 출력
        
        while True: # 수정 작업이 완료될 때까지 반복
            # 수정할 회원 이름 입력
            name = self.get_name_input("수정") # 이름 입력 함수 호출
            if name is None:  # 나가기 선택한 경우
                return # 함수 종료
            
            # 이름으로 회원 검색 (딕셔너리에서 값 검색)
            found_members = self.search_members_by_name(name) # 이름으로 검색
            
            if not found_members: # 검색 결과가 없는 경우
                print("해당 회원이 없습니다.") # 없음 메시지
                continue # 반복하여 다시 이름 입력
            
            # 검색된 목록 출력
            self.display_search_results(found_members) # 검색 결과 출력
            
            # 수정할 번호 선택
            selected_phone = self.select_member_from_list(found_members) # 회원 선택
            if selected_phone is None: # 선택 취소한 경우
                continue # 반복하여 다시 검색
            
            # 회원 정보 수정
            if self.update_member_info(selected_phone): # 수정 함수 호출
                print("수정완료 - 회원 정보가 성공적으로 수정되었습니다!") # 완료 메시지
                input("엔터를 눌러 메뉴로 돌아가세요...") # 사용자 입력 대기
                return # 함수 종료
    
    def search_members_by_name(self, name):
        """이름으로 회원 검색"""
        found = [] # 검색 결과를 저장할 리스트
        # 딕셔너리의 모든 값을 검사
        for phone, member in self.members.items(): # 딕셔너리 순회
            if name in member['name']: # 이름이 포함된 경우 (부분 검색)
                found.append((phone, member)) # (전화번호, 회원정보) 튜플로 저장
        return found # 검색 결과 반환
    
    def display_search_results(self, found_members):
        """검색 결과 출력"""
        print(f"\n{'='*60}") # 상단 구분선
        print("                 검색 결과") # 제목
        print(f"{'='*60}") # 구분선
        print(f"{'순번':<4} {'이름':<10} {'전화번호':<15} {'관계':<8} {'주소':<15}") # 테이블 헤더
        print(f"{'-'*60}") # 테이블 구분선
        
        # 검색된 회원들 출력
        for i, (phone, member) in enumerate(found_members, 1): # 검색 결과 순회
            relation_name = self.get_relation_name(member['relation']) # 관계명 변환
            # 주소가 길면 잘라서 표시
            address_short = member['address'][:12] + "..." if len(member['address']) > 15 else member['address']
            # 각 회원 정보 출력
            print(f"{i:<4} {member['name']:<10} {member['phone']:<15} "
                  f"{relation_name:<8} {address_short:<15}")
        
        print(f"{'-'*60}") # 하단 구분선
        print(f"총 {len(found_members)}명 검색됨") # 검색 결과 수
    
    def select_member_from_list(self, found_members):
        """목록에서 회원 선택"""
        while True: # 올바른 선택을 할 때까지 반복
            try: # 예외 처리
                choice = input(f"\n수정할 번호를 선택하세요 (1-{len(found_members)}): ").strip()
                choice_num = int(choice) # 문자열을 정수로 변환
                if 1 <= choice_num <= len(found_members): # 유효한 범위인지 확인
                    return found_members[choice_num - 1][0]  # 선택된 회원의 전화번호 반환
                else: # 범위를 벗어난 경우
                    print(f"1-{len(found_members)} 사이의 번호를 입력해주세요.") # 안내 메시지
            except ValueError: # 숫자가 아닌 입력인 경우
                print("올바른 번호를 입력해주세요.") # 오류 메시지
    
    def update_member_info(self, phone):
        """회원 정보 수정"""
        print("\n현재 정보를 수정합니다. (변경하지 않으려면 엔터를 누르세요)") # 안내 메시지
        
        current_member = self.members[phone].copy() # 현재 회원 정보 복사
        
        # 이름 수정
        print(f"현재 이름: {current_member['name']}") # 현재 이름 표시
        new_name = input("새 이름: ").strip() # 새 이름 입력
        if new_name and self.validate_name(new_name): # 새 이름이 유효한 경우
            current_member['name'] = new_name # 이름 업데이트
        elif new_name: # 새 이름이 있지만 유효하지 않은 경우
            print("이름 형식이 올바르지 않습니다. 기존 이름을 유지합니다.") # 오류 메시지
        
        # 전화번호 수정
        print(f"현재 전화번호: {current_member['phone']}") # 현재 전화번호 표시
        new_phone = input("새 전화번호: ").strip() # 새 전화번호 입력
        if new_phone: # 새 전화번호가 입력된 경우
            if not self.validate_phone_format(new_phone): # 형식이 올바르지 않은 경우
                print("전화번호 형식이 올바르지 않습니다. 기존 전화번호를 유지합니다.") # 오류 메시지
            elif new_phone in self.members and new_phone != phone: # 중복인 경우 (자기 자신 제외)
                print("기등록된 번호입니다.") # 중복 메시지
                return False  # 수정 실패 반환 (번호 재선택을 위해)
            else: # 새 전화번호가 유효한 경우
                # 딕셔너리에서 기존 키 삭제 후 새 키로 추가
                del self.members[phone] # 기존 전화번호 키 삭제
                current_member['phone'] = new_phone # 새 전화번호로 업데이트
                self.members[new_phone] = current_member # 새 키로 딕셔너리에 추가
                phone = new_phone # 현재 전화번호 변수 업데이트
        
        # 관계 수정
        print(f"현재 관계: {self.get_relation_name(current_member['relation'])}") # 현재 관계 표시
        print("새 관계 (1:가족, 2:친구, 3:기타, 엔터:유지)") # 안내 메시지
        new_relation = input("선택: ").strip() # 새 관계 입력
        if new_relation in ['1', '2', '3']: # 유효한 선택인 경우
            current_member['relation'] = int(new_relation) # 관계 업데이트
        
        # 주소 수정
        print(f"현재 주소: {current_member['address']}") # 현재 주소 표시
        new_address = input("새 주소: ").strip() # 새 주소 입력
        if new_address and len(new_address) <= 100: # 새 주소가 유효한 경우
            current_member['address'] = new_address # 주소 업데이트
        elif new_address: # 새 주소가 있지만 너무 긴 경우
            print("주소가 너무 깁니다. 기존 주소를 유지합니다.") # 오류 메시지
        
        # 수정된 정보를 딕셔너리에 저장
        self.members[phone] = current_member # 딕셔너리 업데이트
        return True # 수정 성공 반환
    
    # ============================================================================
    # 4. 회원 삭제 기능
    # ============================================================================
    
    def delete_member(self):
        """4번 - 회원 삭제 기능"""
        print("\n=== 회원 삭제 ===") # 기능 제목 출력
        
        while True: # 삭제 작업이 완료될 때까지 반복
            # 삭제할 회원 이름 입력
            name = self.get_name_input("삭제") # 이름 입력 함수 호출
            if name is None:  # 나가기 선택한 경우
                return # 함수 종료
            
            # 이름으로 회원 검색
            found_members = self.search_members_by_name(name) # 이름으로 검색
            
            if not found_members: # 검색 결과가 없는 경우
                print("해당 회원이 없습니다.") # 없음 메시지
                continue # 반복하여 다시 이름 입력
            
            # 검색된 목록 출력
            self.display_search_results(found_members) # 검색 결과 출력
            
            # 삭제할 번호 선택
            selected_phone = self.select_member_from_list(found_members) # 회원 선택
            if selected_phone is None: # 선택 취소한 경우
                continue # 반복하여 다시 검색
            
            # 삭제 확인
            selected_member = self.members[selected_phone] # 선택된 회원 정보
            print(f"\n선택된 회원: {selected_member['name']} ({selected_member['phone']})") # 선택된 회원 표시
            
            choice = input("정말 삭제하시겠습니까? (삭제/취소): ").strip() # 삭제 확인 입력
            
            if choice == "삭제": # 삭제 선택시
                # 딕셔너리에서 삭제
                del self.members[selected_phone] # 전화번호 키로 회원 삭제
                print("삭제완료 - 회원이 성공적으로 삭제되었습니다!") # 완료 메시지
                input("엔터를 눌러 메뉴로 돌아가세요...") # 사용자 입력 대기
                return # 함수 종료
            elif choice == "취소": # 취소 선택시
                return # 삭제 취소하고 함수 종료
            else: # 잘못된 입력인 경우
                print("'삭제' 또는 '취소'를 입력해주세요.") # 안내 메시지
    
    # ============================================================================
    # 5. 종료 기능
    # ============================================================================
    
    def exit_program(self):
        """5번 - 프로그램 종료"""
        print("\n종료하시겠습니까?") # 종료 확인 메시지
        choice = input("선택하세요 (예/아니오): ").strip() # 사용자 입력
        
        if choice == "예": # 예 선택시
            # 데이터 저장
            if self.save_data(): # 저장 성공한 경우
                print("프로그램을 종료합니다.") # 종료 메시지
                return True # 종료 신호 반환
            else: # 저장 실패한 경우
                print("데이터 저장에 실패했습니다. 그래도 종료하시겠습니까?") # 실패 메시지
                confirm = input("(예/아니오): ").strip().lower() # 강제 종료 확인
                return confirm == '예' # 예인 경우 강제 종료
        elif choice == "아니오": # 아니오 선택시
            return False # 종료 취소
        else: # 잘못된 입력인 경우
            print("(예/아니오)를 입력해주세요.") # 안내 메시지
            return False # 종료 취소
    
    # ============================================================================
    # 메인 실행 함수
    # ============================================================================
    
    def run(self):
        """메인 프로그램 실행"""
        print("회원관리 시스템을 시작합니다...") # 시작 메시지
        
        # 바이너리 파일에서 데이터 읽기
        self.load_data() # 데이터 로드 함수 호출
        
        while True: # 프로그램이 종료될 때까지 무한 반복
            # 메뉴 출력
            self.show_menu() # 메뉴 화면 출력
            
            # 메뉴 선택
            choice = self.get_menu_choice() # 사용자 메뉴 선택 입력
            
            # 기능 실행 (선택된 메뉴에 따라 분기)
            if choice == 1: # 1번 목록 출력 선택
                self.display_members() # 목록 출력 함수 호출
            elif choice == 2: # 2번 회원 추가 선택
                self.add_member() # 회원 추가 함수 호출
            elif choice == 3: # 3번 회원 수정 선택
                self.edit_member() # 회원 수정 함수 호출
            elif choice == 4: # 4번 회원 삭제 선택
                self.delete_member() # 회원 삭제 함수 호출
            elif choice == 5: # 5번 종료 선택
                if self.exit_program(): # 종료 함수 호출하여 종료 확인
                    break # 반복문 종료 (프로그램 종료)

# ============================================================================
# 프로그램 실행
# ============================================================================

if __name__ == "__main__": # 스크립트가 직접 실행되는 경우
    system = MemberManagementSystem() # 회원관리시스템 객체 생성
    system.run() # 프로그램 실행