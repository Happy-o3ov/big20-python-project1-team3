## 회원 관리 프로그램 플로우차트 : 회원 신규 등록
```mermaid
graph TD
    %% 회원 추가 
    Add([2.회원 신규등록 처리 시작]);
    Add --> inputItems@{ shape: sl-rect, label: "항목입력받기: <br>이름*, 전화번호*, 관계*, 주소"};
    inputItems --> validationItems{입력값 모두 유효성 검사 통과?};
    validationItems -- False --> printError@{ shape: doc, label: "항목별 에러 및 재입력 출력"};
    printError --> inputItems;
    validationItems -- True --> checkDuplication[입력받은 전화번호 중복확인]
    checkDuplication --> duplJudge{ 중복인가? };
    duplJudge -- True --> printError2@{ shape: doc, label: "기 등록 메시지 출력"};
    printError2 --> subMenu;
    duplJudge -- False --> saveInfo@{ shape: lin-cyl, label: "회원 정보 저장" };
    saveInfo --> printSaved@{ shape: doc, label: "저장 완료 메시지 출력"};
    printSaved --> subMenu@{ shape: sl-rect, label: "'<' 목록으로 돌아가기 <br> '+' 새로운 추가"};
    subMenu -- '<' 입력시 --> Menu((Main Menu));
    subMenu -- '+' 입력시 --> inputItems;
    subMenu -- 그외 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
    errorInputPrint --> subMenu;
 ```

       