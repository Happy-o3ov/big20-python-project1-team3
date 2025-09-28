## 회원 관리 프로그램 플로우차트  : 회원정보 삭제 4.2.1 삭제 프로세스
```mermaid
graph LR
  %% style inputViewNum fill:#FFCC00,stroke:#999,stroke-width:2px,color:#000 
  RemoveAItem([ 4.2.1 회원 정보 삭제 프로세스 시작 ]) 
    RemoveAItem --> searchResultPrint@{ shape: doc, label: "검색 결과 목록 출력 <br> 번호 | 이름 | 전화번호 | 관계 " }  
    searchResultPrint --> inputRemoveNum@{ shape: sl-rect, label: "삭제할 번호 입력 혹은 <br>'<' Main Menu로 돌아가기"};
    inputRemoveNum --> inputValidation{입력값 유효성 검사 통과? };
    inputValidation -- '<' 입력시 --> Menu((Main Menu))          
    inputValidation -- True(삭제할 번호) --> RemoveInfo[삭제]
    RemoveInfo --> saveInfo@{ shape: lin-cyl, label: "회원 정보 삭제 저장" };
      saveInfo --> RemoveResultPrint@{ shape: doc, label: "삭제 성공 메세지 출력 " }  
      RemoveResultPrint --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br> 'c' 삭제 계속"};
      subMenu -- '<' 입력시 --> Menu((Main Menu 출력));
      subMenu -- 'c' 입력시 --> Remove(( 3.삭제 프로세스));
      subMenu -- 그외 --> errorInputPrint2@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
                          errorInputPrint2 --> subMenu;        
    inputValidation -- False(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputRemoveNum
    
 ```
