## 회원 관리 프로그램 플로우차트  : 4. 회원 삭제 처리
```mermaid
graph TD
   %% 4.회원 삭제 처리
   Remove([4.회원 삭제 처리 시작]) --> searchCondition@{ shape: div-rect, label: "4.1 키워드 검색 입력 프로세스" } 
   searchCondition --> searching[4.2 검색]
   searching --> searchResult{ 검색 결과 데이터 길이 > 0 ? }
   searchResult -- True --> deleteItems@{ shape: div-rect, label: "4.2.1 삭제 프로세스"}
   searchResult -- False --> searchResultFailed@{ shape: div-rect, label: "4.2.2 검색 실패 프로세스"}
  
 ```
