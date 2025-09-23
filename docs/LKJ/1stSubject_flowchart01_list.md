## 회원 관리 프로그램 플로우차트 : 목록 출력 
```mermaid
graph TD
    %% 회원 목록 출력
    List([1.회원 목록 출력 처리]) --> printList@{ shape: doc, label: "총 개수 및 목록 출력"};
    printList --> inputViewNum@{ shape: sl-rect, label: "상세조회할 번호 입력 혹은 '<' 메인메뉴로 돌아가기" };
    inputViewNum --> inputValidation{ 입력값 유효성 검사 후 }
    inputValidation -- '<' 입력시 --> Menu((Main Menu));
    inputValidation -- 목록에 있는 번호 --> viewDetail@{ shape: doc, label: "한명의 정보 상세 출력"}
    inputValidation -- 목록에 없는 경우 --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. 다시 입력하세요"};
    errorInputPrint -- 재입력하기 --> inputViewNum
    viewDetail -- 출력 후 --> inptGotoList@{ shape: sl-rect, label: "목록으로 돌아가기 1.예 2.아니오" }
    inptGotoList --> validation{입력값 유효성 검사}
    validation -- 1 입력시 --> printList
    validation -- 그외 --> inptGotoList

```
 