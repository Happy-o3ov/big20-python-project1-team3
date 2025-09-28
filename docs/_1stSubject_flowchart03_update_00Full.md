## 회원 관리 프로그램 플로우차트  : 회원정보 수정
```mermaid
graph LR
    %% 3.회원 수정 처리
   Update(3.회원 수정 처리 시작) --> searchCondition
   subgraph searchCondition
     inputSearchKeyword@{ shape: sl-rect, label: "검색 항목입력받기 : <br> 이름 혹은 전화번호"};    
      inputSearchKeyword --> validationSearchKeyword{입력값 유효성 검사 통과?};
      validationSearchKeyword -- False --> errorInputPrint1@{ shape: doc, label: "잘못입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint1 --> inputSearchKeyword;
   end 
   subgraph searchResult   
      validationSearchKeyword -- True --> searching[저장된 목록에서 검색];
      searching --> searchCount{ 검색결과 길이 > 0 ? }
      searchCount -- False --> printNoSearch@{ shape: doc, label: "검색된 목록이 없습니다."};
      printNoSearch --> inputAction@{ shape: sl-rect, label: "'<'.Main Menu로 돌아가기 <br> 'r' 다시 검색하기 "}
      inputAction -- 'a' 입력시 --> inputSearchKeyword
      inputAction -- '<' 입력시 --> Menu((Main Menu))
      inputAction -- 그외 입력시 --> errorInputPrint2@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
        errorInputPrint2 --> inputAction    
      searchCount -- True --> printList@{ shape: doc, label: "검색결과 총 개수 및 목록 출력 <br>번호|이름|전화번호"};
   end
   subgraph UpdateAItem
    printList --> inputViewNum@{ shape: sl-rect, label: "수정할 번호 입력 혹은 <br> '<' Main Menu로 돌아가기"};
    inputViewNum --> inputValidation{입력값 유효성 검사 통과? };
    inputValidation -- '<' 입력시 --> Menu((Main Menu))          
    inputValidation -- False(그외) --> errorInputPrint3@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint3 --> inputViewNum
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
      printSaved --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br>'e' 수정 계속"};
      subMenu -- '<' 입력시 --> MainMenu((Main Menu 출력));
      subMenu -- 'c' 입력시 --> Update
      subMenu -- 그외 --> errorInputPrint3;
                          errorInputPrint3 --> subMenu;    
    end

 ```
