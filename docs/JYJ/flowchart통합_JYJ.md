```mermaid

flowchart TD
    START([프로그램 시작]) --> LOAD[바이너리 파일 읽기]
    LOAD --> MENU[/"메뉴 출력<br/>1.목록출력 2.회원추가<br/>3.회원수정 4.회원삭제 5.종료"/]
    
    MENU --> CHOICE[/메뉴 선택 입력/]
    CHOICE --> SELECT{메뉴 선택<br/>1-5?}
    
    %% 1. 목록 출력
    SELECT -->|1| LIST_DATA_CHK{저장된 데이터<br/>존재?}
    LIST_DATA_CHK -->|False| LIST_NO_DATA[/"저장된 데이터가 없습니다<br/>메시지 화면 출력"/]
    LIST_NO_DATA --> MENU
    LIST_DATA_CHK -->|True| LIST_DISPLAY[/"회원 저장된 데이터 목록 출력<br/>추가 순서대로 순번,이름,전화번호,관계,주소<br/>총 회원 데이터 개수 표시"/]
    LIST_DISPLAY --> LIST_EXIT_MSG[/"메뉴로 나가겠습니까?<br/>메시지 화면 표시"/]
    LIST_EXIT_MSG --> LIST_EXIT_INPUT[/선택 입력<br/>예 아니오/]
    LIST_EXIT_INPUT --> LIST_EXIT_CHOICE{예 or 아니오?}
    LIST_EXIT_CHOICE -->|예| MENU
    LIST_EXIT_CHOICE -->|아니오| LIST_DISPLAY
    
    %% 2. 회원 추가
    SELECT -->|2| ADD_NAME[/이름 입력<br/>나가기 입력시 메뉴 나가기/]
    ADD_NAME --> ADD_NAME_CHK{입력값 확인}
    ADD_NAME_CHK -->|나가기| ADD_EXIT_CONFIRM[/"메뉴 선택으로 나가겠습니까?<br/>예 아니오"/]
    ADD_EXIT_CONFIRM --> ADD_EXIT_INPUT[/선택 입력/]
    ADD_EXIT_INPUT --> ADD_EXIT_CHOICE{예 or 아니오?}
    ADD_EXIT_CHOICE -->|아니오| ADD_NAME
    ADD_EXIT_CHOICE -->|예| MENU
    
    ADD_NAME_CHK -->|이름| ADD_NAME_VALID{이름 유효성<br/>한영 5자 이내?}
    ADD_NAME_VALID -->|False| ADD_NAME
    ADD_NAME_VALID -->|True| ADD_PHONE[/전화번호 입력<br/>정수3자리-정수4자리-정수4자리/]
    
    ADD_PHONE --> ADD_PHONE_FORMAT{전화번호 형식<br/>000-0000-0000?}
    ADD_PHONE_FORMAT -->|False| ADD_PHONE
    ADD_PHONE_FORMAT -->|True| ADD_DUP_CHK{회원목록 데이터에<br/>똑같은 번호 있음?}
    
    ADD_DUP_CHK -->|True| ADD_DUP_MSG[/"중복된 번호입니다<br/>메시지 화면 출력"/]
    ADD_DUP_MSG --> ADD_PHONE
    ADD_DUP_CHK -->|False| ADD_REL[/관계 선택<br/>1.가족 2.친구 3.기타/]
    
    ADD_REL --> ADD_REL_CHK{관계<br/>1,2,3 중 선택?}
    ADD_REL_CHK -->|False| ADD_REL
    
    ADD_REL_CHK -->|1번| ADD_REL_1_CONFIRM[/"1번(가족)으로 선택하겠습니까?<br/>예 아니오"/]
    ADD_REL_1_CONFIRM --> ADD_REL_1_INPUT[/선택 입력/]
    ADD_REL_1_INPUT --> ADD_REL_1_CHOICE{예 or 아니오?}
    ADD_REL_1_CHOICE -->|아니오| ADD_REL
    ADD_REL_1_CHOICE -->|예| ADD_ADDR[/주소 입력<br/>100자 이내/]
    
    ADD_REL_CHK -->|2번| ADD_REL_2_CONFIRM[/"2번(친구)으로 선택하겠습니까?<br/>예 아니오"/]
    ADD_REL_2_CONFIRM --> ADD_REL_2_INPUT[/선택 입력/]
    ADD_REL_2_INPUT --> ADD_REL_2_CHOICE{예 or 아니오?}
    ADD_REL_2_CHOICE -->|아니오| ADD_REL
    ADD_REL_2_CHOICE -->|예| ADD_ADDR
    
    ADD_REL_CHK -->|3번| ADD_REL_3_CONFIRM[/"3번(기타)으로 선택하겠습니까?<br/>예 아니오"/]
    ADD_REL_3_CONFIRM --> ADD_REL_3_INPUT[/선택 입력/]
    ADD_REL_3_INPUT --> ADD_REL_3_CHOICE{예 or 아니오?}
    ADD_REL_3_CHOICE -->|아니오| ADD_REL
    ADD_REL_3_CHOICE -->|예| ADD_ADDR
    
    ADD_ADDR --> ADD_ADDR_CHK{주소<br/>100자 이내?}
    ADD_ADDR_CHK -->|False| ADD_ADDR
    ADD_ADDR_CHK -->|True| ADD_SAVE[회원 데이터 저장]
    ADD_SAVE --> ADD_COMPLETE[/"저장완료<br/>메시지 화면 표시"/]
    ADD_COMPLETE --> MENU
    
    %% 3. 회원 수정
    SELECT -->|3| EDIT_NAME[/수정할 회원 이름 입력<br/>나가기 입력시 메뉴 나가기/]
    EDIT_NAME --> EDIT_NAME_CHK{입력값 확인}
    EDIT_NAME_CHK -->|나가기| EDIT_EXIT_CONFIRM[/"메뉴 선택으로 나가겠습니까?<br/>예 아니오"/]
    EDIT_EXIT_CONFIRM --> EDIT_EXIT_INPUT[/선택 입력/]
    EDIT_EXIT_INPUT --> EDIT_EXIT_CHOICE{예 or 아니오?}
    EDIT_EXIT_CHOICE -->|아니오| EDIT_NAME
    EDIT_EXIT_CHOICE -->|예| MENU
    
    EDIT_NAME_CHK -->|이름| EDIT_NAME_VALID{이름 유효성<br/>한영 1-5자?}
    EDIT_NAME_VALID -->|False| EDIT_NAME
    EDIT_NAME_VALID -->|True| EDIT_SEARCH[이름으로 검색 처리]
    
    EDIT_SEARCH --> EDIT_FOUND{검색 결과<br/>존재?}
    EDIT_FOUND -->|False| EDIT_NOT_FOUND[/"해당 회원 없음<br/>메시지 화면 표시"/]
    EDIT_NOT_FOUND --> EDIT_NAME
    
    EDIT_FOUND -->|True| EDIT_LIST[/"검색된 목록 출력<br/>순번,이름,전화번호,관계,주소"/]
    EDIT_LIST --> EDIT_SELECT[/수정할 번호 입력/]
    EDIT_SELECT --> EDIT_NUM_CHK{번호<br/>유효?}
    EDIT_NUM_CHK -->|False| EDIT_SELECT
    
    EDIT_NUM_CHK -->|True| EDIT_INPUT[/이름,전화번호,관계,주소<br/>차례로 입력/]
    EDIT_INPUT --> EDIT_VALID{각 항목<br/>유효성 통과?}
    EDIT_VALID -->|False| EDIT_INPUT
    EDIT_VALID -->|True| EDIT_DUP_CHK{전화번호<br/>중복?}
    
    EDIT_DUP_CHK -->|True| EDIT_DUP_MSG[/"기등록 번호<br/>메시지 화면 표시"/]
    EDIT_DUP_MSG --> EDIT_SELECT
    EDIT_DUP_CHK -->|False| EDIT_SAVE[수정 데이터 저장]
    EDIT_SAVE --> EDIT_COMPLETE[/"수정완료<br/>메시지 화면 표시"/]
    EDIT_COMPLETE --> MENU
    
    %% 4. 회원 삭제
    SELECT -->|4| DEL_NAME[/삭제할 회원 이름 입력<br/>나가기 입력시 메뉴 나가기/]
    DEL_NAME --> DEL_NAME_CHK{입력값 확인}
    DEL_NAME_CHK -->|나가기| DEL_EXIT_CONFIRM[/"메뉴 선택으로 나가겠습니까?<br/>예 아니오"/]
    DEL_EXIT_CONFIRM --> DEL_EXIT_INPUT[/선택 입력/]
    DEL_EXIT_INPUT --> DEL_EXIT_CHOICE{예 or 아니오?}
    DEL_EXIT_CHOICE -->|아니오| DEL_NAME
    DEL_EXIT_CHOICE -->|예| MENU
    
    DEL_NAME_CHK -->|이름| DEL_NAME_VALID{이름 유효성<br/>한영 1-5자?}
    DEL_NAME_VALID -->|False| DEL_NAME
    DEL_NAME_VALID -->|True| DEL_SEARCH[이름으로 검색 처리]
    
    DEL_SEARCH --> DEL_FOUND{검색 결과<br/>존재?}
    DEL_FOUND -->|False| DEL_NOT_FOUND[/"해당 회원 없음<br/>메시지 화면 표시"/]
    DEL_NOT_FOUND --> DEL_NAME
    
    DEL_FOUND -->|True| DEL_LIST[/"검색된 목록 출력"/]
    DEL_LIST --> DEL_SELECT[/삭제할 번호 입력/]
    DEL_SELECT --> DEL_NUM_CHK{번호<br/>유효?}
    DEL_NUM_CHK -->|False| DEL_SELECT
    
    DEL_NUM_CHK -->|True| DEL_CONFIRM[/"삭제 확인 메시지 화면 표시<br/>삭제 취소"/]
    DEL_CONFIRM --> DEL_INPUT[/선택 입력/]
    DEL_INPUT --> DEL_CHOICE{삭제 or 취소?}
    
    DEL_CHOICE -->|취소| MENU
    DEL_CHOICE -->|삭제| DEL_EXECUTE[회원 데이터 삭제]
    DEL_EXECUTE --> DEL_COMPLETE[/"삭제완료<br/>메시지 화면 표시"/]
    DEL_COMPLETE --> MENU
    
    %% 5. 종료
    SELECT -->|5| EXIT_CONFIRM[/"종료 확인 메시지 화면 표시<br/>1예 2아니오"/]
    EXIT_CONFIRM --> EXIT_INPUT[/선택 입력/]
    EXIT_INPUT --> EXIT_CHOICE{1 or 2?}
    EXIT_CHOICE -->|2| MENU
    EXIT_CHOICE -->|1| SAVE_FILE[목록을 파일에 저장]
    SAVE_FILE --> END([프로그램 종료])
    
    %% 잘못된 메뉴 입력
    SELECT -->|1-5 외| INVALID[/"잘못된 입력<br/>메시지 화면 표시"/]
    INVALID --> MENU
    
    style START fill:#e1f5fe
    style END fill:#ffcdd2
    style MENU fill:#fff3e0
    style LIST_DISPLAY fill:#fff3e0
    style LIST_NO_DATA fill:#ffe0e0
    style ADD_SAVE fill:#e8f5e8
    style EDIT_SAVE fill:#e8f5e8
    style DEL_EXECUTE fill:#e8f5e8
    style SAVE_FILE fill:#e8f5e8
    ```