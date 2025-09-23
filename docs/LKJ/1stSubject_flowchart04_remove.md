## 회원 관리 프로그램 플로우차트  : 회원정보 수정
```mermaid
graph TD
    %% 4.회원 삭제 처리
    Remove(4.회원 삭제 처리) --> inputSearchKeyword[\검색 항목입력받기:  이름 혹은 전화번호\];    
    inputSearchKeyword --> validationSearchKeyword{유효성 검사};
    validationSearchKeyword -- 실패 --> errorInputPrint[/잘못입력하셨습니다. 다시 입력하세요/];
                                        errorInputPrint --> inputSearchKeyword;
    validationSearchKeyword -- 성공 --> search[(저장된 목록에서 검색)];
    search -- 실패 --> printNoSearch[/검색된 목록이 없습니다./];
      printNoSearch --> inputAction[\1.다시 검색하기 back.Main Menu로 돌아가기\]
      inputAction -- 1 입력시 --> inputSearchKeyword
      inputAction -- back 입력시 --> Menu((Main Menu))
      inputAction -- 그외 입력시 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. 다시 입력하세요"};
        errorInputPrint --> inputAction    
    search -- 성공 --> printList[/총 개수 및 목록 출력/];
    printList --> inputViewNum[\삭제할 번호 입력 혹은 back:Main Menu로 돌아가기\];
    inputViewNum --> inputValidation{유효성 검사};
    inputValidation -- back 입력시 --> Menu((Main Menu))          
    inputValidation -- 실패(그외) --> errorInputPrint[/잘못입력하셨습니다. 다시 입력하세요/];
      errorInputPrint --> inputViewNum
    inputValidation -- 성공(삭제 번호) --> delConfirm[\정말 삭제하시겠습니까? 1.삭제 2.취소하고 Main Menu로 돌아가기\]
    delConfirm -- 1 입력 --> deleteItem[삭제하기]
      deleteItem --> printSucces[/삭제되었습니다. 출력/]
      printSuccess --> Main((Main Menu 출력))
    delConfirm -- 그외 --> Main((Main Menu 출력))
 ```
