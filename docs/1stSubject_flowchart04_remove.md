## 회원 관리 프로그램 플로우차트  : 4.회원정보 삭제
```mermaid
graph TD
    %% 4.회원 삭제 처리
    Remove([4.회원 삭제 처리 시작]) --> inputViewNum@{ shape: sl-rect, label: "삭제할 번호 입력 혹은 <br> '<' Main Menu로 돌아가기"};
    inputViewNum --> inputValidation{입력값 유효성 검사 통과? };
    inputValidation -- '<' 입력시 --> Menu((Main Menu))          
    inputValidation -- False(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputViewNum
    inputValidation -- True(수정할 번호) --> inputUpdateItems@{ shape: sl-rect, label: "수정항목 입력받기: <br> 이름*, 관계*, 주소 입력"}    
    inputUpdateItems --> validationItems{ 모든 입력값들 유효성 검사 통과? };
    validationItems -- False --> printError@{ shape: doc, label: "항목별 에러 및 재입력 출력"};
      printError --> inputUpdateItems;
    %% validationItems -- True --> checkDuplication[중복확인]
    %% checkDuplication --> duplJudge{ 입력받은 전화번호가 기 등록되어 있는가? };  
    %% duplJudge -- True --> printError2@{ shape: doc, label: "기등록 메시지 출력"};
    %%  printError2 --> subMenu;
    %% duplJudge -- False --> updateInfo@{ shape: lin-cyl, label: "회원 정보 수정 저장" };
      validationItems -- True --> updateInfo@{ shape: lin-cyl, label: "회원 정보 수정 저장" };
      updateInfo --> printSaved@{ shape: doc, label: "수정 저장 완료 메시지 출력"};
      printSaved --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br>'c' 수정 계속"};
      subMenu -- '<' 입력시 --> MainMenu((Main Menu 출력));
      subMenu -- 'c' 입력시 --> Update
      subMenu -- 그외 --> errorInputPrint;
                          errorInputPrint --> subMenu;    


    inputValidation -- 성공(삭제 번호) --> delConfirm[\정말 삭제하시겠습니까? 1.삭제 2.취소하고 Main Menu로 돌아가기\]
    delConfirm -- 1 입력 --> deleteItem[삭제하기]
      deleteItem --> printSucces[/삭제되었습니다. 출력/]
      printSuccess --> Main((Main Menu 출력))
    delConfirm -- 그외 --> Main((Main Menu 출력))
 ```
