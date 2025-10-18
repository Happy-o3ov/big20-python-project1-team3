-- 1. 기본 조회 및 집계
-- 1-1. 장르별 매출을 구하고 가장 많이 팔린 장르순으로 조회

SELECT b.GENRE,                         -- 책의 장르 보여달라하기 ( 예 : Fiction, Science 등 )
       SUM(oi.QUANTITY) AS TOTAL_SOLD  -- 각 장르별로 몇 권 팔렸는지 합계 구하기
  FROM BOOKS b                           -- BOOKS 테이블에서 책 정보를 가져오기
  JOIN ORDER_ITEMS oi                    -- ORDER_ITEMS 테이블에서 주문 정보를 Join
    ON b.BOOK_ID = oi.BOOK_ID            -- 두 테이블을 BOOK_ID 기준으로 연결 ( 같은 책끼리 연결 )
 GROUP BY b.GENRE                       -- 장르별로 그룹화 ( 예 : Fiction끼리 합산 )
 ORDER BY TOTAL_SOLD                    -- 많이 팔린 순서대로 내림차순 정렬
 DESC
;     -- 과제에 올리기.

-- 1-2. Top 10 베스트셀러 작가와 판매총액 조회

SELECT b.AUTHOR  							-- 책 저자 이름
     , SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS TOTAL_REVENUE  
  FROM BOOKS b  							-- 주문 내역이 담긴 order_items 테이블과 연결
  JOIN ORDER_ITEMS oi  
    ON b.BOOK_ID = oi.BOOK_ID 			    -- 두 테이블을 BOOK_ID 기준으로 연결
 GROUP BY b.AUTHOR  						-- 저자별로 그룹을 나눠서 SUM 계산 가능하게
HAVING SUM(oi.QUANTITY) > 500               -- 판매량 500권 초과 저자만  
ORDER BY TOTAL_REVENUE						-- 총 매출이 높은 순서대로 내림차순 정렬
 DESC  										
FETCH FIRST 10 ROWS ONLY
; 

-- 1-3. 평균 가격 이상의 도서 목록 : 서브쿼리 활용

SELECT TITLE       -- 책 제목
   	 , PRICE        -- 책 가격
  FROM BOOKS
 WHERE PRICE >= (
  	SELECT AVG(PRICE)  -- 전체 책의 평균 가격 계산
  	  FROM BOOKS
)
 ORDER BY PRICE
  DESC  -- 가격 높은 순으로 정렬
FETCH FIRST 10 ROWS ONLY   -- 상위 10권만 출력
;


-- 1-4. 한 번도 주문하지 않은 고객 조회

SELECT c.CUSTOMER_ID			-- 고객의 고유 ID 출력
     , c.CUSTOMER_NAME			-- 고객 이름 출력
FROM CUSTOMERS c				-- CUSTOMERS 테이블 기준으로 조회
WHERE
    NOT EXISTS (				-- 해당 고객의 주문 기록이 존재하지 않을 경우 포함
        SELECT 1				-- 단순 존재 여부만 확인하므로 1을 반환
        FROM ORDERS o			-- ORDER 테이블에서 주문 내역 확인
        WHERE o.CUSTOMER_ID = c.CUSTOMER_ID
    )							-- 고객 ID가 일치하는 주문이 있는지 확인
ORDER BY DBMS_RANDOM.VALUE  	-- 결과 랜덤 정렬 ( 100번대부터 9000번대까지 다양하게 )
FETCH FIRST 15 ROWS ONLY		-- 상위 15명 출력
;

SELECT c.CUSTOMER_ID            -- 고객의 고유 ID 출력
     , c.CUSTOMER_NAME			-- 고객 이름을 출력
  FROM CUSTOMERS c				-- CUSTOMERS 테이블 기준으로 조회
 WHERE
    NOT EXISTS (				-- 해당 고객의 주문 기록이 존재하지 않을 경우 포함
        SELECT 1				-- 단순 존재 여부만 확인하므로 1을 반환
        FROM ORDERS o			-- ORDER 테이블에서 주문 내역 확인
        WHERE o.CUSTOMER_ID = c.CUSTOMER_ID
    )							-- 고객 ID가 일치하는 주문이 있는지 확인
    AND c.CUSTOMER_ID >= 1000   -- 1000번대 이상만 포함
 ORDER BY DBMS_RANDOM.VALUE		-- 결과 무작위 랜덤
 FETCH FIRST 15 ROWS ONLY		-- 상위 15명 출력
;


-- 1-5. 2개 이상의 장르를 구매한 고객 조회

SELECT c.CUSTOMER_ID				-- 고객 고유 ID
     , c.CUSTOMER_NAME				-- 고객 이름 출력
  FROM CUSTOMERS c
  JOIN ORDERS o						-- 고객이 주문한 내역 연결
    ON o.CUSTOMER_ID = c.CUSTOMER_ID	-- 고객 주문 내역 일치 확인
  JOIN ORDER_ITEMS oi           	-- 주문상세 테이블 ( 테이블명 확인 필요 )
    ON oi.ORDER_ID = o.ORDER_ID	
  JOIN BOOKS b						-- 주문한 책 장르 정보 위해 BOOKS 연결 ( join )
    ON b.BOOK_ID = oi.BOOK_ID
 GROUP BY c.CUSTOMER_ID
        , c.CUSTOMER_NAME
HAVING COUNT(DISTINCT b.GENRE) >= 2  -- 서로 다른 장르를 2개 이상 구매한 고객
ORDER BY DBMS_RANDOM.VALUE            -- 실행할 때마다 랜덤 추출
FETCH FIRST 6 ROWS ONLY         -- 상위 6명만
;



-- 2. 중급 쿼리 (CTE, 분석 함수 기초)
-- 6. VIP 고객 분석 (10명) 조회 - 고객명, 고객별 전체 금액, 순위 조회

WITH CustomerSpending AS (
  SELECT c.CUSTOMER_ID
       , c.CUSTOMER_NAME,			-- 고객의 고유 ID와 이름 가져오기
    SUM(b.PRICE * oi.QUANTITY) AS TOTAL_SPENT	-- 책 가격 × 수량을 곱해서 주문별 금액 계산해서 고객별로 총합을 구함
    FROM CUSTOMERS c
    JOIN ORDERS o					-- 고객과 주문 테이블 연결 ( 어떤 고객이 어떤 책을 주문했는지 이해하기 )
      ON o.CUSTOMER_ID = c.CUSTOMER_ID
    JOIN ORDER_ITEMS oi				-- 주문과 주문 항목 연결해서 주문 안에 어떤 책이 몇 권 있는지 확인
      ON oi.ORDER_ID = o.ORDER_ID
    JOIN BOOKS b
      ON b.BOOK_ID = oi.BOOK_ID		-- 주문 항목과 책 정보 연결.
  GROUP BY c.CUSTOMER_ID
         , c.CUSTOMER_NAME
),		/* 고객별로 묶어서 총 지출 금액 계산. 한 고객이 여러번 주문 했을 가능성도 있음
		그리고 이로써 첫 CTE 완성. */
		/* 아래는 고객별로 순위를 매기기 위해 두번째 CTE 시작. */
RankedCustomers AS (
  SELECT CUSTOMER_NAME
       , TOTAL_SPENT, /* RANK() 함수로 총 지출 금액 기준으로 순위. 고객 이름과 총 지출금액 가져오기 */
    RANK() OVER (ORDER BY TOTAL_SPENT DESC) AS CUSTOMER_RANK		-- 지출 금액이 큰 고객이 1등.
    FROM CustomerSpending				-- 앞서 만든 CustomerSpending CTE 사용. ( 계산되어있는 고객별 총 지출금액 )
)									-- 두번째 CTE 끝.
SELECT CUSTOMER_NAME				-- VIP 고객 이름
  	 , TOTAL_SPENT					-- VIP 고객이 쓴 총 지출 금액
     , CUSTOMER_RANK				-- 순위 이어서 보여주기
FROM RankedCustomers				-- 두번째 CTE에서 순위가 매겨진 고객 리스트 가져오기 ?
WHERE CUSTOMER_RANK <= 10			-- VIP 상위 10명만 나오게끔 출력.
ORDER BY CUSTOMER_RANK				-- 순위 기준으로 정렬
;



-- 7. 월별 매출 성장률 분석 - 월별, 월별 매출, 이전달 매출, 성장율 조회

WITH MonthlyRevenue AS (							-- CTE(common Table Expression) 시작하는 키워드.
  /* [1] 월별 총매출 계산 (월 첫날 00:00:00 DATE) */		-- MonthlyRevenue 라는 이름의 임시 테이블을 만듦.
  SELECT TRUNC(o.ORDER_DATE, 'MM') AS SALES_MONTH,		-- 주문 일자를 월 단위로 잘라서 월 매출을 기준으로 함
    	 SUM(b.PRICE * oi.QUANTITY) AS MONTHLY_REVENUE	-- 책 가격 x 책 수량을 월별로 합산해 월매출 계산해서 MONTHLY_REVENUE로 저장
    FROM ORDERS o									-- from 기입후 ORDER 주문정보
    JOIN ORDER_ITEMS oi								-- 주문 항목
      ON oi.ORDER_ID = o.ORDER_ID					-- 주문 ID 매칭
    JOIN BOOKS b									-- 책 정보 테이블 세 가지 테이블 연결
      ON b.BOOK_ID   = oi.BOOK_ID					-- 책 ID 매칭 ( 책 정보 )
  GROUP BY TRUNC(o.ORDER_DATE, 'MM')				-- 월별로 결과 묶기
)
	/* 월별로 묶어서 매출을 계산하면 MonthlyRevenue라는 CTE 완성. */
	 , RevenueWithPrevious AS (
  SELECT
    SALES_MONTH,
    MONTHLY_REVENUE,			-- 앞에서 만든 MonthlyRevenue에서 월과 매출을 가져오기
    LAG(MONTHLY_REVENUE) OVER (ORDER BY SALES_MONTH) AS PREVIOUS_MONTH_REVENUE
  FROM MonthlyRevenue
) /* [2] 이전 달 매출을 월, 매출 가져오기.
  그 다음 이전 달 매출을 PREVIOUS_MONTH_REVENUE로 저장. */
SELECT
  /* [3] 최종 출력: 날짜+시간, 매출, 이전 매출, 성장률(문자열) */
  TO_CHAR(SALES_MONTH, 'YYYY-MM-DD HH24:MI:SS') AS SALES_MONTH,
  MONTHLY_REVENUE,
  NVL(PREVIOUS_MONTH_REVENUE, 0) AS PREVIOUS_MONTH_REVENUE,
  /* 첫 달(PREVIOUS_MONTH_REVENUE)은 비교 대상이 없으므로 월매출 x 100( 과장된 수치지만 예외처리 )
   - 이후 달 : ( 이번 달 매출 - 지난 달 매출 ) ÷ 지난 달 매출 x 100 -> 전월 대비 증감률 계산
   결과는 소수점 둘째 자리까지 반올림 -> 숫자를 문자열로 변환한 뒤, '%' 기호를 붙여서 표시 */
  CAST(
    CASE
      WHEN PREVIOUS_MONTH_REVENUE IS NULL THEN
        ROUND(MONTHLY_REVENUE * 100, 2)
      ELSE ROUND(
          (MONTHLY_REVENUE - PREVIOUS_MONTH_REVENUE)
            / PREVIOUS_MONTH_REVENUE * 100, 2
        )				-- 이후 달은 전월 대비 증감률 계산
    END
  AS VARCHAR2(20)			-- 숫자를 문자열로 바꾸되 20글자까지 저장할 수 있는 문자열로 바꿔달라는 것.
  ) || '%' AS GROWTH_RATE		-- 계산 결과를 문자열로 변환 후 '%' 기호 붙여서 표시
   /* 성장률은 원래 숫자지만 뒤에 '%' 라는 기호가 붙은 형태. 이건 문자열.
    * 숫자 타입은 계산용이기에 기호를 붙이면 오류가 발생. SQL에서는 숫자에 '%' 붙일 수 없음. */
FROM RevenueWithPrevious	-- 단계 CTE 사용
ORDER BY SALES_MONTH				-- 월 오름차순 정렬
;

-------------------
-----------------
---------------------





-- 8. 장르별 매출 기여도

WITH GenreRevenue AS (
  SELECT b.GENRE,  -- 책의 장르
    SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS REVENUE  -- 장르별 총 매출
  FROM ORDER_ITEMS oi
  JOIN BOOKS b
    ON b.BOOK_ID = oi.BOOK_ID
 GROUP BY b.GENRE
),
TotalRevenue AS (
  SELECT SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS TOTAL_REVENUE
  FROM ORDER_ITEMS oi
)
SELECT gr.GENRE         -- 장르 이름
  	 , gr.REVENUE,       -- 해당 장르의 총 매출
  -- 전체 매출 대비 비율 계산 → 소수점 둘째 자리까지 반올림 후 % 표시
  ROUND(gr.REVENUE / tr.TOTAL_REVENUE * 100, 2) || '%' AS CONTRIBUTION_PCT
FROM GenreRevenue gr
  CROSS JOIN TotalRevenue tr  -- 전체 매출을 모든 장르에 붙이기
ORDER BY gr.REVENUE
 DESC
;

SELECT b.GENRE					-- 책의 장르 불러오기
     , SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS REVENUE	-- 해당 장르의 총 매출 : 책 가격 수량을 모두 더함
  	 , ROUND(SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) /
    (SELECT SUM(PRICE_PER_UNIT * QUANTITY)
       FROM ORDER_ITEMS) * 100,2) || '%' AS CONTRIBUTION_PCT -- 장르별 매출 ÷ 전체 매출 × 100 → 소수점 둘째 자리까지 반올림
       -- 결과를 문자열로 바꾼 뒤 '%' 기호 붙이기
  FROM ORDER_ITEMS oi
  JOIN BOOKS b
    ON b.BOOK_ID = oi.BOOK_ID	-- 주문 항목과 책 정보 연결
GROUP BY b.GENRE				-- 장르별로 묶어서 매출 계산
ORDER BY REVENUE DESC			-- 매출 높은 순으로 정렬
;

-- 9. 각 장르 내 가장 비싼 책 Top 3

-- 10. 고객별 누적 구매액 : 100번 고객만 조회

-- 11. 함께 가장 많이 팔린 도서 조합 : 10개만 조회

-- 12. 휴면 가능성 VIP 고객
-- 총구매액 : 500,000 이상, 6개월 이상 구매 안한 고객 조회

-- Part 3: 고급 분석 및 데이터 변환
-- 13. 고객 등급 분류:  5개 등급으로 분리

