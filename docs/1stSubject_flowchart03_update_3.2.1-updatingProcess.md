## 회원 관리 프로그램 플로우차트  : 회원정보 수정 3.2.1 수정 프로세스
```mermaid
graph LR
  %% style inputViewNum fill:#FFCC00,stroke:#999,stroke-width:2px,color:#000 
  UpdateAItem([ 3.2.1 회원 정보 수정 프로세스 시작 ]) 
    UpdateAItem --> searchResultList@{ shape: doc, label: "검색 결과 목록 출력 <br> 번호 | 이름 | 전화번호 | 관계 " }  
    searchResultList --> inputViewNum@{ shape: sl-rect, label: "수정할 번호 입력 혹은 <br>'<' Main Menu로 돌아가기"};

    inputViewNum --> inputValidation{입력값 유효성 검사 통과? };
    inputValidation -- True(수정할 번호) --> inputUpdateItems@{ shape: sl-rect, label: "수정항목 입력받기: <br> 이름*, 관계*, 주소 입력"}    
      inputUpdateItems --> validationItems{ 모든 입력값들 유효성 검사 통과? };
    inputValidation -- False(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputViewNum
    inputValidation -- '<' 입력시 --> Menu((Main Menu))          
    validationItems -- False --> printError@{ shape: doc, label: "항목별 에러 및 재입력 출력"};
      printError --> inputUpdateItems;  
    %% validationItems -- True --> checkDuplication[중복확인]
    %% checkDuplication --> duplJudge{ 입력받은 전화번호가 기 등록되어 있는가? };  
    %% duplJudge -- True --> printError2@{ shape: doc, label: "기등록 메시지 출력"};
    %%  printError2 --> subMenu;
    %% duplJudge -- False --> updateInfo@{ shape: lin-cyl, label: "회원 정보 수정 저장" };
      validationItems -- True --> updateInfo@{ shape: lin-cyl, label: "회원 정보 수정 저장" };
      updateInfo --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br> 'c' 수정 계속"};
      subMenu -- '<' 입력시 --> Menu((Main Menu 출력));
      subMenu -- 'c' 입력시 --> Update(( 3.수정 프로세스));
      subMenu -- 그외 --> errorInputPrint2@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
                          errorInputPrint2 --> subMenu;        
   
 ```
