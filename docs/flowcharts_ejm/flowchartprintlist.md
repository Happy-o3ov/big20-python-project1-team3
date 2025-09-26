```mermaid
graph TD
Select1{메뉴 출력} -->|True| PrintList[[목록 출력]] --> PrintMenu
Select1 -->|False| Select2{회원 추가}
```