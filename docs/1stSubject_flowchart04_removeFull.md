## 회원 관리 프로그램 플로우차트  : 4.회원정보 삭제
```mermaid
graph TD
    %% 4.회원 삭제 처리
    Remove([4.회원 삭제 처리 시작]) --> inputViewNum@{ shape: sl-rect, label: "삭제할 번호 입력 혹은 <br> '<' Main Menu로 돌아가기"};
    inputViewNum --> inputValidation{입력값 유효성 검사 통과? };
    inputValidation -- '<' 입력시 --> Menu((Main Menu))          
    inputValidation -- False(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputViewNum
    inputValidation -- 성공(삭제 번호) --> delConfirm@{ shape: sl-rect, label: "정말 삭제하시겠습니까? 'y'.삭제 '<'취소하고 Main Menu로 돌아가기"}
    delConfirm -- 'y' 입력 --> deleteItem[삭제하기]
      deleteItem --> removeInfo@{ shape: lin-cyl, label: "회원 정보 삭제 저장" };
      removeInfo --> printSucces@{ shape: doc, label : "삭제 완료 메세지 출력"}
      printSaved --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br>'c' 삭제 계속"};
      subMenu -- '<' 입력시 --> MainMenu
      subMenu -- 'c' 입력시 --> Remove
      subMenu -- 그외 --> errorInputPrint;
                          errorInputPrint --> subMenu;    

    delConfirm -- 그외 --> MainMain

   
 ```
