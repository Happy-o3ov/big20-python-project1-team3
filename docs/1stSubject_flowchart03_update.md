## 회원 관리 프로그램 플로우차트  : 회원정보 수정
```mermaid
graph TD
    %% 3.회원 수정 처리
   Update(3.회원 수정 처리) --> searchCondition@{ shape: div-rect, label: "검색 프로세스" }
   subgraph searchCondition
     inputSearchKeyword@{ shape: sl-rect, label: "검색 항목입력받기<br>: 이름 혹은 전화번호"};    
      inputSearchKeyword --> validationSearchKeyword{입력값 유효성 검사};
      validationSearchKeyword -- 실패 --> errorInputPrint@{ shape: doc, label: "잘못입력하셨습니다. 다시 입력하세요"};
      errorInputPrint --> inputSearchKeyword;
   end 
   subgraph searchResult   
      validationSearchKeyword -- 성공 --> search[저장된 목록에서 검색];
      search -- 실패 --> printNoSearch@{ shape: doc, label: "검색된 목록이 없습니다."};
      printNoSearch --> inputAction@{ shape: sl-rect, label: "'<'.Main Menu로 돌아가기 'a' 다시 검색하기 "}
      inputAction -- 'a' 입력시 --> inputSearchKeyword
      inputAction -- '<' 입력시 --> Menu((Main Menu))
      inputAction -- 그외 입력시 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. 다시 입력하세요"};
        errorInputPrint --> inputAction    
      search -- 성공 --> printList@{ shape: doc, label: "총 개수 및 목록 출력"};
   end
   subgraph UpdateAItem
    printList --> inputViewNum@{ shape: sl-rect, label: "수정할 번호 입력 혹은 '<' Main Menu로 돌아가기"};
    inputViewNum --> inputValidation{입력값 유효성 검사};
    inputValidation -- back 입력시 --> Menu((Main Menu))          
    inputValidation -- 실패(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. 다시 입력하세요"};
      errorInputPrint --> inputViewNum
    inputValidation -- 성공(수정할 번호) --> inputUpdateItems@{ shape: sl-rect, label: "수정항목 입력받기<br>: 이름, 전화번호, 관계, 주소 입력"}    
    inputUpdateItems --> validationItems{유효성 검사};
    validationItems -- 실패 --> printError@{ shape: doc, label: "항목별 에러 및 재입력 출력"};
      printError --> inputUpdateItems;
    validationItems -- 성공 --> checkDuplication{ 기 등록 전화번호 중복 체크 };
      checkDuplication -- 중복 --> printError2@{ shape: doc, label: "기등록 메시지 출력"};
        printError2 --> subMenu;
      checkDuplication -- 중복 아님 --> saveInfo[(회원 정보 저장)];
      saveInfo --> printSaved[/수정 저장 완료 메시지 출력/];
      printSaved --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 'c'수정 계속"};
      subMenu -- '<' 입력시 --> Menu((Main Menu 출력));
      subMenu -- 'c' 입력시 --> inputSearchKeyword;
      subMenu -- 그외 --> errorInputPrint;
                          errorInputPrint --> subMenu;    
    end

 ```
