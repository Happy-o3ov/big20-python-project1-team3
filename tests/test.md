``` mermaid
graph TD

%% 1. 검색 및 번호 입력 단계
subgraph 검색 및 번호 입력
  UpdateAItem([3.2.1 회원 정보 수정 프로세스 시작])
  UpdateAItem --> searchResultList@{ shape: doc, label: "검색 결과 목록 출력 <br> 번호 | 이름 | 전화번호 | 관계 " }
  searchResultList --> inputViewNum@{ shape: sl-rect, label: "수정할 번호 입력 혹은 <br>'<' Main Menu로 돌아가기"}
end

%% 2. 입력값 유효성 검사 및 수정 항목 처리
subgraph 수정 항목 입력 및 검사
  inputViewNum --> inputValidation{입력값 유효성 검사 통과?}
  inputValidation -- True(수정할 번호) --> inputUpdateItems@{ shape: sl-rect, label: "수정항목 입력받기: <br> 이름*, 관계*, 주소 입력"}
  inputUpdateItems --> validationItems{ 모든 입력값들 유효성 검사 통과? }
  validationItems -- True --> updateInfo@{ shape: lin-cyl, label: "회원 정보 수정 저장" }
end

%% 3. 정보 저장 후 메뉴 선택
subgraph 메뉴 선택 흐름
  inputValidation -- '<' 입력시 --> Menu((Main Menu))
  updateInfo --> subMenu@{ shape: sl-rect, label: "'<' Main Menu으로 돌아가기 <br> 'c' 수정 계속"}
  subMenu -- '<' 입력시 --> Menu((Main Menu 출력))
  subMenu -- 'c' 입력시 --> Update((3.수정 프로세스))
end

%% 4. 에러 처리 흐름
subgraph 에러 처리
  inputValidation -- False(그외) --> errorInputPrint@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"}
  errorInputPrint --> inputViewNum
  validationItems -- False --> printError@{ shape: doc, label: "항목별 에러 및 재입력 출력"}
  printError --> inputUpdateItems
  subMenu -- 그외 --> errorInputPrint2@{ shape: doc, label: "잘못 입력하셨습니다. <br> 다시 입력하세요"}
  errorInputPrint2 --> subMenu
end

```