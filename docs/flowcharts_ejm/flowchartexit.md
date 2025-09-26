```mermaid
graph TD
Select5{프로그램 종료} --> CheckAsk{정말로 종료할지 체크}
CheckAsk -->|True| SaveFile[파일 저장] --> End((종료))
CheckAsk -->|False| PrintMenu
SaveFile -->|error| PrintMenu
```