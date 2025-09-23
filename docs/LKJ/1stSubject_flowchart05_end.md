## 회원 관리 프로그램 플로우차트 종료 
```mermaid
graph TD
    %% 프로그램 종료
    Menu[/메인 메뉴 출력/] --> finish[5 프로그램 종료 선택시]; 
    finish --> finish1[\종료하시겠습니까? 1. 예, 2. 아니오\];
    finish1 --> finish2{입력값 유효성 검사};
    finish2 -- 1 입력 --> finish21[(목록을 파일에 저장)] --> END ;
    finish2 -- 2 입력 --> END([프로그램 종료]); 
    finish2 -- 그외 --> finish3@{ shape: doc, label: "잘못 입력하셨습니다. 다시 입력하세요"};
    finish3 --> finish1
    
```