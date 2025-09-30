import os                      # 운영체제 기능 사용 (파일 존재 확인 등)
import pickle                  # 파이썬 객체를 바이너리로 저장/불러오기
import re                      # 정규식 사용

FILE_NAME = "../data/member.dat"      # 회원 데이터 파일 경로

# 전화번호를 key로, 값은 이름, 관계, 주소를 담는 딕셔너리
members = {}   
# 구조 예시: {"010-1234-5678": {"name": "홍길동", "rel": "가족", "addr": "서울시"}}

# --- 파일 로드/저장 ---
def load_file():               
    global members
    if os.path.exists(FILE_NAME):                  # 파일이 존재하면
        with open(FILE_NAME, "rb") as f:
            members = pickle.load(f)              # pickle로 불러오기
    else:
        members = {}                               # 파일 없으면 빈 딕셔너리

def save_file():
    with open(FILE_NAME, "wb") as f:
        pickle.dump(members, f)                    # members 딕셔너리 저장

# --- 유효성 검사 ---
def valid_name(name):          
    return 1 <= len(name) <= 5 and name.isalnum()   # 1~5자, 영문/한글/숫자

def valid_phone(phone):        
    return re.match(r"^010-\d{4}-\d{4}$", phone) is not None  # 010-0000-0000 형태

def valid_rel(rel):            
    return rel in ["1", "2", "3"]   # 허용값 1,2,3

def valid_addr(addr):          
    return len(addr) <= 100        # 주소 100자 이내

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
    if phone in members:                       # 전화번호 중복 검사
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

    members[phone] = {"name": name, "rel": rel, "addr": addr}  # 추가
    print("저장 완료!")                         

def modify_member():           
    phone = input("수정할 회원 전화번호 입력: ")     
    if phone not in members:                      
        print("해당 번호의 회원이 없습니다.")      
        return                                     

    name = input("새 이름 (1~5자): ")             
    if not valid_name(name):                      
        print("이름 오류")                        
        return                                     

    new_phone = input("새 전화번호 (010-0000-0000): ")  
    if not valid_phone(new_phone) or (new_phone != phone and new_phone in members):
        print("전화번호 오류 또는 중복")            
        return                                    

    rel = input("새 관계 (1,2,3): ")              
    if not valid_rel(rel):                        
        print("관계 오류")                         
        return                                     

    addr = input("새 주소 (100자 이내): ")         
    if not valid_addr(addr):                       
        print("주소 오류")                          
        return                                     

    if new_phone != phone:                           # 전화번호 key 변경 시
        members[new_phone] = members.pop(phone)     # 기존 데이터 이동
    members[new_phone].update({"name": name, "rel": rel, "addr": addr})  # 값 갱신
    print("수정 완료!")

def delete_member():           
    phone = input("삭제할 회원 전화번호 입력: ")     
    if phone in members:                            
        del members[phone]                           
        print("삭제 완료!")                          
    else:                                           
        print("해당 번호의 회원이 없습니다.")        

# --- 메인 루프 ---
def main():                   
    load_file()               
    while True:               
        print("\n[메뉴] 1.목록 2.추가 3.수정 4.삭제 5.종료")  
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
