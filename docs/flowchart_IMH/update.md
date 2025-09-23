# 사용자 업데이트(수정)

```mermaid
flowchart TD

    %%사용자 검색
    search_update_message[수정할 사용자 이름 검색]
    search_name@{ shape: manual-input, label: "이름 입력"}
    check_search_name{이름 유효성 검사}
    failed_search[해당 이름이 없습니다<br>메뉴로 돌아갑니다]
    success_search[검색된 사용자 정보 출력]

    %%사용자 선택
    select@{ shape: manual-input, label: "수정할 사용자번호 입력"}
    check_select{번호 검사}
    failed_select[유효하지 않은 번호입니다<br>메뉴로 이동]

    %%사용자 정보 수정
    update_message[사용자 정보 수정]
    update_input@{ shape: manual-input, label: "수정정보 입력"}
    check_update_input{유효성검사}
    save_file[(회원 데이터 파일 저장)]
    failed_update[잘못된 입력<br>메뉴로 이동]
    success_update[수정 완료<br>메뉴로 이동]
    return_menu[메뉴 이동]


    search_update_message --> search_name
    search_name --> check_search_name
    check_search_name --> |No| failed_search --> return_menu
    check_search_name --> |Yes| success_search

    success_search --> select
    select --> check_select
    check_select --> |No| failed_select --> return_menu
    check_select --> |Yes| update_message
    update_message --> update_input
    update_input --> check_update_input
    check_update_input --> |No| failed_update --> return_menu
    check_update_input --> |Yes| success_update --> return_menu
    success_update --> save_file
    






```