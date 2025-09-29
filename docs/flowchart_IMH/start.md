```mermaid
flowchart TD
    start((시작))
    read_binary_file@{ shape: database, label: "members.dat<br>회원 파일 읽기" }
    create_binary_file@{ shape: database, label: "members.dat<br>파일 생성,빈데이터 저장" }
    save_binary_file@{ shape: database, label: "members.dat<br>회원 파일 저장" }
    check_file{파일/폴더 유무 확인}
    menu[메뉴 출력<br/>
            1.목록 출력  2.회원 추가<br/>  
            3.회원 수정  4. 회원 삭제<br/>
            5. 종료]
    input_name@{ shape: manual-input, label: "1~5 입력받기"}
    check_input_menu{메뉴입력<br>유효성검사}


    start --> check_file
    check_file --> |True| read_binary_file --> menu
    check_file --> |False| create_binary_file --> menu
    
    menu --> input_name
    input_name --> check_input_menu

    check_input_menu -->|입력 == 1| list[목록 출력]
    check_input_menu -->|입력 == 2| add[회원 추가]
    check_input_menu -->|입력 == 3| update[회원 수정]
    check_input_menu -->|입력 == 4| remove[회원 삭제]
    check_input_menu -->|입력 == 5| save_binary_file --> finish((종료))
    check_input_menu -->|그 외| menu[메뉴 출력]
    
```
