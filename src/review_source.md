## source reviewed by LKJ

1. Member.set() 이 한 레코드를 수정하는 것으로 되어 있는데 .get()과 맞지 않음. 
   getter/setter 만들데 헷갈리게 됨. 따라서 .set()은 update_info 등으로 바꾸는 것이 어떨까?

1. raise KeyError('해당하는 사용자를 찾을 수 없습니다') 이런식으로 try: except: 를 사용하지 않고 단독으로 사용됨.  같이 사용해야 함.
   단독 사용하려면 그냥 print(msg) 를 사용하는 것이 낳을 듯.

1. y, n 등 문자를 입력받았는데 input_num.lower() == 'y' 이런식으로 처리해야..

1. 함수명과 설명에 아래와 같이 되어 있는데..
   이건 메뉴 자체를 add 하라는 것 같은 명칭처럼 오해할 수 있음.

    def add_member_menu(members: Members) -> bool:
        """
        사용자 추가 메뉴

    def input_member 도 input_member_info 라던가 input_data, get_member_info 가 어떨지?

    def set_member_menu 도 ... edit_member_info
    def del_member_menu 도 ... del_member_info

1. 유효성 검사도 패턴만 return 하는데 None 과 중복 처리도 같이 하는 게 좋을 듯.     

1. if add_num in members.member_dict.keys(): ==> if add_num in members.member_dict 까지만 해도 됨..  in 자체가 keys() 에서 처리함
   if old_num not in self.member_dict.keys(): ==> 위와 동일
    raise KeyError('해당하는 사용자를 찾을 수 없습니다') ==> 위에 언급했던 부분.. 


1. relation lel_check 시에도 아래 처럼 하는 것이 아니라
   relation_map = {'1': "가족", '2' : "", '3': ""} 으로 dict 로 만들어서 한줄로 표시하는 게 어떻까?
    if rel not in RELATION_MAP and input_data not in RELATION_MAP.values():
        print("관계 형식이 올바르지 않습니다.")   
    else: #처리 코드

  하지만 입력은 숫자/한글 중 하나만 입력받는 것이 더 좋을 듯..  
  그리고 저장은 숫자로 하고 출력은 문자로 하는 것이 좋아요. 
  실제 db에는 주로 코드가 들어가고 출력은 코드명으로 합니다~
   
    if rel in('1','가족'):
        return '가족'
    if rel in('2','친구'):
        return '친구'
    if rel in('3','기타'):
        return '기타'
    raise ValueError('관계 형식이 올바르지 않습니다.') 

1.과제에서 선생님이 기본 가이드가 "회원관리"라고 하셨고 아래와 같이 주셨으니
  아래 단어를 사용하는 것이 맞을 듯요... 왜냐면 make up 하는 것과 단어 자체를 달리 사용하는 건
  나중 실제 프로젝트에서는 있어서는 안돼요 ^^;; 기획자의 의도와 디자이너가 해준 걸로 프로그램해야해요 ^^ 
    • 회원 목록
    • 회원 추가
    • 회원 수정
    • 회원 삭제
    • 종료

 1. 같이 언급했던 것처럼 self..update() 하고 나서 save_date() 해줘도 됐을 듯...
    