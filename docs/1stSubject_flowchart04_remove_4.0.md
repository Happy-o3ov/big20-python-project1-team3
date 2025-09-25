## 회원 관리 프로그램 플로우차트  : 4. 회원 삭제 처리
```mermaid
graph TD
   %% 4.회원 삭제 처리
   %% Remove([4.회원 삭제 처리 시작]) --> searchCondition@{ shape: div-rect, label: "4.1 키워드 검색 입력 프로세스" } 
   Remove([4.회원 삭제 처리 시작]) --> searchCondition
      subgraph searchCondition
      inputSearchKeyword@{ shape: sl-rect, label: "검색 항목입력받기 : <br> 이름 혹은 전화번호"};    
      inputSearchKeyword --> validationSearchKeyword{입력값 유효성 검사 통과?};
      validationSearchKeyword -- False --> errorInputPrint@{ shape: doc, label: "잘못입력하셨습니다. <br> 다시 입력하세요"};
      errorInputPrint --> inputSearchKeyword;   
   end
   %% searchCondition --> searching[4.2 검색]
   subgraph searching 
      validationSearchKeyword -- True --> searching[4.2 검색]
      searching --> searchResult{ 검색 결과 데이터 길이 > 0 ? }
      searchResult -- True --> deleteItems@{ shape: div-rect, label: "4.2.1 삭제 프로세스"}
      searchResult -- False --> printNoSearch@{ shape: doc, label: "검색된 목록이 없습니다."};
         printNoSearch --> inputAction@{ shape: sl-rect, label: "'<' Main Menu로 돌아가기 <br> 'a' 다시 검색하기 "}
         inputAction -- 'a' 입력시 --> searchCondition
         inputAction -- '<' 입력시 --> MainMenu((Main Menu))
         inputAction -- 그외 입력시 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"};
         errorInputPrint --> inputAction    
   end
 ```
