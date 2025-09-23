## 회원 관리 프로그램 플로우차트  : 회원정보 수정
```mermaid
graph TD
    %% 3.회원 수정 처리
   Update(3.회원 수정 처리) --> searchCondition@{ shape: div-rect, label: "키워드 검색 입력 프로세스" } 
   searchCondition --> searching[검색]
   searching --> searchResult{ 검색 결과 성공 여부 }
   searchResult -- 성공 --> searchResultList@{ shape: doc, label: "검색 결과 목록 출력" }  
   searchResult -- 실패 --> searchResultFailed@{ shape:div-rect, label: "검색 실패 프로세스"}
   searchResultList --> updateItemNoChoice@{ shape: div-rect, label: "수정 프로세스" } 
   searchResultFailed --> searchCondition
 ```
