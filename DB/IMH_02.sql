--문제1. 장르별 매출을 구하고 가장 많이 팔린 장르 순으로 조회
-- 1. 책과 주문품목을 내부조인, 장르별로 그룹화
-- 2. SUM(구매량)으로 총 판매량 계산, 높은순으로 정렬
SELECT b.GENRE
	 , SUM(oi.QUANTITY) AS TOTAL_SOLD
  FROM BOOKS b
  JOIN ORDER_ITEMS oi 
  	ON b.BOOK_ID = oi.BOOK_ID
 GROUP BY b.GENRE
 ORDER BY TOTAL_SOLD DESC
;

--문제2. Top 10 베스트셀러 작가와 판매총액 조회
-- 1. 책과 주문품목을 내부조인, 작가별로 그룹화
-- 2. SUM(가격*구매량)으로 작가별 총 판매수익 계산, 높은순 정렬
-- 3. FETCH 로 상위 10행 출력, 동순위 포함(WITH_TIES)
SELECT b.AUTHOR
	 , SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS TOTAL_REVENUE
  FROM BOOKS b
  JOIN ORDER_ITEMS oi ON b.BOOK_ID = oi.BOOK_ID
 GROUP BY b.AUTHOR
 ORDER BY TOTAL_REVENUE DESC
 FETCH FIRST 10 ROWS WITH TIES;
;

--문제3. 평균 가격 이상의 도서 목록: 서브쿼리 활용

SELECT b.TITLE
	 , b.PRICE
  FROM BOOKS b
 WHERE b.PRICE >= (
	   SELECT AVG(PRICE)
		 FROM BOOKS
	 )
 ORDER BY b.PRICE
;

--문제4. 한 번도 주문하지 않은 고객 조회
-- 1. 고객(기준)에 ORDERS를 LEFT 외부조인
-- 2. WHERE절에서 주문ID가 NULL인 고객만 조회 
SELECT c.CUSTOMER_ID
	 , c.CUSTOMER_NAME
  FROM CUSTOMERS c
  LEFT JOIN ORDERS o 
  	ON c.CUSTOMER_ID = o.CUSTOMER_ID
 WHERE o.ORDER_ID IS NULL;

--문제5. 2개 이상의 장르를 구매한 고객 조회
-- 1. 고객,주문,주문품목,책 조인
-- 2. 고객ID,고객명으로 그룹화
-- 3. COUNT(DISTINCT 장르) >= 2 중복되지 않는 장르 수를 계산
SELECT c.CUSTOMER_ID
	 , c.CUSTOMER_NAME
  FROM CUSTOMERS c
  JOIN ORDERS o 
  	ON c.CUSTOMER_ID = o.CUSTOMER_ID
  JOIN ORDER_ITEMS oi 
  	ON o.ORDER_ID = oi.ORDER_ID
  JOIN BOOKS b 
  	ON b.BOOK_ID = oi.BOOK_ID
 group BY c.CUSTOMER_ID, c.CUSTOMER_NAME
HAVING COUNT(DISTINCT b.GENRE) >= 2
 ORDER BY c.CUSTOMER_ID
;

-- 고객이 구매한 책(장르) 확인
SELECT o.CUSTOMER_ID
	 , b.GENRE
  FROM ORDERS o
  JOIN ORDER_ITEMS oi 
  	ON o.ORDER_ID = oi.ORDER_ID
  JOIN BOOKS b 
  	ON b.BOOK_ID = oi.BOOK_ID
 WHERE o.CUSTOMER_ID IN (38, 78, 250) -- 1종류의 장르만 구매한 고객 일부
 ORDER BY o.CUSTOMER_ID, b.GENRE
;

--문제6. VIP 고객 분석(10명) 조회 : 고객명, 고객별 전체 금액, 순위 조회
-- 1. WITH로 전체금액(c_total), 금액순위(c_rank) 테이블 생성
-- 1.1 전체금액 테이블에서 고객별로 그룹화, 고객별 전체금액(TOTAL_SPENT) 계산
-- 1.2 금액순위 테이블에서 DENSE_RANK로 전체금액 높은순 순위화 (CUSTOMER_RANK)
-- 2. 메인쿼리에서 c_rank와 고객 내부 조인, 10순위까지 출력 
WITH 
c_total AS (
	SELECT o.CUSTOMER_ID
		 , SUM(o.TOTAL_AMOUNT) AS TOTAL_SPENT
	  FROM ORDERS o
	 GROUP BY o.CUSTOMER_ID
),
c_rank AS (
	SELECT CUSTOMER_ID
		 , TOTAL_SPENT
		 , DENSE_RANK() OVER (ORDER BY TOTAL_SPENT DESC
		 ) AS CUSTOMER_RANK
	  FROM c_total
)
SELECT c.CUSTOMER_NAME
	 , r.TOTAL_SPENT
	 , r.CUSTOMER_RANK
  FROM c_rank r
  JOIN CUSTOMERS c 
  	ON c.CUSTOMER_ID = r.CUSTOMER_ID
 WHERE r.CUSTOMER_RANK <= 10
;

--문제7. 월별 매출 성장률 분석: 월별, 월별 매출, 이전달 매출, 성장율 조회
-- 1. WITH로 sal_month 월별 매출 테이블 테이블 생성
-- 1.1 TRUNC로 월별 그룹화
-- 1.2 LAG로 월별로 정렬, 이전 월별매출 조회
-- 2. 메인쿼리에서 성장률 게산
-- 성장률	: CASE 이전달없음 THEN 월별매출
--		  ELSE    	      (월별매출 - 이전달매출)/이전달매출 * 100			   
WITH 
sal_month AS (
	SELECT TRUNC (o.ORDER_DATE, 'Month') AS SALES_MONTH
		 , SUM(o.TOTAL_AMOUNT) AS MONTHLY_REVENUE
		 , LAG (SUM(o.TOTAL_AMOUNT), 1, 0) OVER
		 	   (ORDER BY TRUNC (o.ORDER_DATE, 'Month')
		 ) AS PREVIOUS_MONTH_REVENUE
	  FROM ORDERS o
	 GROUP BY TRUNC(o.ORDER_DATE, 'Month')
)
SELECT sm.SALES_MONTH
	 , sm.MONTHLY_REVENUE
	 , sm.PREVIOUS_MONTH_REVENUE
	 , CASE
		 WHEN PREVIOUS_MONTH_REVENUE = 0 THEN TO_CHAR (MONTHLY_REVENUE) || '%'
		 ELSE TO_CHAR(ROUND(
		 	(MONTHLY_REVENUE - PREVIOUS_MONTH_REVENUE) / 
		 	 PREVIOUS_MONTH_REVENUE * 100,2)) || '%' 
	    END AS GROWTH_RATE
  FROM sal_month sm
 ORDER BY sm.SALES_MONTH
;

--문제8.장르별 매출 기여도
-- 1. WITH GENRE_REV 장르별 수익 테이블 조회
-- 1.1 주문품목,책 내부조인, 장르별 그룹화, 수익으로 
-- 2. 메인쿼리에서 RATIO_TO_REPORT로 전체 대비 장르별 비율 계산
WITH
GENRE_REV AS (
	SELECT b.GENRE
		 , SUM(oi.QUANTITY * oi.PRICE_PER_UNIT) AS REVENUE
	  FROM ORDER_ITEMS oi 
	  JOIN BOOKS b 
	  	ON b.BOOK_ID = oi.BOOK_ID
	 GROUP BY b.GENRE
)
SELECT gr.GENRE
	 , gr.REVENUE
	 , TO_CHAR(
	 	 ROUND(RATIO_TO_REPORT(gr.REVENUE) OVER () * 100, 2)
	 ) || '%' AS CONTRIBUTION_PCT
  FROM GENRE_REV gr
 ORDER BY gr.REVENUE DESC
;

--문제9. 각 장르 내 가장 비싼 책 Top 3
-- 1. FROM b : 장르,책제목,가격, 장르별 비싼책 순위(PRICE_RANK) << RANK()
-- 2. PRICE_RANK <=3 까지만 조회
SELECT b.TITLE
	 , b.GENRE
	 , b.PRICE
  FROM (
		SELECT GENRE
			 , TITLE
			 , PRICE
			 , RANK() OVER (PARTITION BY GENRE ORDER BY PRICE DESC
			 ) AS PRICE_RANK
		 FROM BOOKS
	 ) b
 WHERE b.PRICE_RANK <= 3
 ORDER BY b.GENRE
;

--문제10. 고객별 누적 구매액 : 100번 고객만 조회
-- 1. 고객기준 외부조인, 구매하지 않은 고객까지 조회
-- 2. 누적 구매액(CUMULATIVE_SUM) << SUM() : 주문마다 구매액 누적합
-- 3. 100번 고객 날짜별 누적금액 조회
SELECT o.ORDER_DATE
	 , nvl(o.TOTAL_AMOUNT, 0)
	 , SUM(nvl(o.TOTAL_AMOUNT, 0)) OVER 
	 	  (PARTITION BY c.CUSTOMER_ID ORDER BY o.ORDER_DATE
	 ) AS CUMULATIVE_SUM
  FROM ORDERS o
 RIGHT JOIN CUSTOMERS c 
 	ON o.CUSTOMER_ID = c.CUSTOMER_ID
 WHERE c.CUSTOMER_ID = 100
 ORDER BY o.ORDER_DATE
;

--11. 함께 가장 많이 팔린 도서 조합 : 10개만 조회
-- *다음부터는 DISTINCT보다, 그룹화 된 테이블을 셀프조인하기 << 효율 더 좋음
-- with PAIR_BOOKS:
--			셀프조인: ORDER_ITEMS oi1,oi2
--			  한 쌍의 책ID 조합
--			  같은 주문 내, 중복되지 않는 모든 쌍 조회
-- with PAIR_RANKS:
--			  조인: 책조합(PAIR_BOOKS), BOOKS b1,b2
--			 그룹화: 조합된 책 제목1,2 (b1.TITLE, b2.TITLE)
--			  모든 주문 내 특정 책조합의 수(PAIR_COUNT) << 함꼐 팔린 도서조합의 수
--			  수에 따른 ROW_NUMBER 랭크 부여(RNKS) << 가장 많이 팔린 조합 순위
-- 순위(RNKS) 10위까지 조회
WITH
PAIR_BOOKS AS (
	SELECT oi1.BOOK_ID AS p1
		 , oi2.BOOK_ID AS p2
	  FROM (SELECT DISTINCT ORDER_ID, BOOK_ID
			  FROM ORDER_ITEMS
		 ) oi1
	  JOIN (SELECT DISTINCT ORDER_ID, BOOK_ID
			  FROM ORDER_ITEMS
		 ) oi2 
		ON oi1.ORDER_ID = oi2.ORDER_ID 
	   AND oi1.BOOK_ID < oi2.BOOK_ID
),
PAIR_RANKS AS (
	SELECT b1.TITLE AS BOOK_1
		 , b2.TITLE AS BOOK_2
		 , COUNT(*) AS PAIR_COUNT
		 , ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, b1.TITLE, b2.TITLE
		 ) AS RNKS
	  FROM PAIR_BOOKS pb
	  JOIN BOOKS b1 ON b1.BOOK_ID = pb.P1
	  JOIN BOOKS b2 ON b2.BOOK_ID = pb.P2
	 GROUP BY b1.TITLE, b2.TITLE
)
SELECT pr.BOOK_1
	 , pr.BOOK_2
	 , pr.PAIR_COUNT
  FROM PAIR_RANKS pr
 WHERE pr.RNKS <= 10
;

--문제12. 휴면 가능성 VIP 고객 : 총구매액 : 500,000 이상, 6개월 이상 구매 안한 고객 조회
-- 1. WITH로 DORMANCY_VIP 조회 (휴면 VIP고객 조회)
-- 1.1 고객별로 그룹화
-- 1.2 MONTHS_BETWEEN으로 휴면 고객 조회
-- 2.1 고객과 VIP휴면고객 내부조인, VIP소비비용으로 정렬
WITH DORMANCY_VIP AS (
	SELECT o.CUSTOMER_ID
		 , SUM(o.TOTAL_AMOUNT) AS LIFETIME_SPENT
		 , MAX(o.ORDER_DATE) AS LAST_ORDER_DATE
	  FROM ORDERS o
	 GROUP BY o.CUSTOMER_ID
	HAVING MONTHS_BETWEEN(SYSDATE, MAX(o.ORDER_DATE)) > 6
	   AND SUM(o.TOTAL_AMOUNT) > 500000
)
SELECT c.CUSTOMER_NAME
	 , dv.LAST_ORDER_DATE
	 , dv.LIFETIME_SPENT
  FROM CUSTOMERS c
  JOIN DORMANCY_VIP dv 
  	ON c.CUSTOMER_ID = dv.CUSTOMER_ID
 ORDER BY dv.LIFETIME_SPENT DESC
;

-------------------------------------------------------------
--Part 3: 고급 분석 및 데이터 변환
--문제13.	고객 등급 분류:  5개 등급으로 분리
-- *구매x 2001명이었으면 1명 4등급?
-- 
-- 1. with로 c_total 테이블 생성
-- 1.1 고객을 기준으로 주문과 외부조인, 고객ID와 이름으로 그룹화
-- 1.2 고객별 총소비비용 계산
-- 1.3 PERCENT_RANK로 순위화, 구매x 고객은 0
-- 2. case별로 등급부여 
WITH c_rank AS (
	SELECT c.CUSTOMER_NAME
		 , NVL(SUM(o.TOTAL_AMOUNT), 0) AS TOTAL_SPENT
		 , PERCENT_RANK() OVER (ORDER BY NVL(SUM(o.TOTAL_AMOUNT), 0)) AS PR
      FROM CUSTOMERS c
      LEFT JOIN ORDERS o 
    	ON o.CUSTOMER_ID = c.CUSTOMER_ID
  GROUP BY c.CUSTOMER_ID, c.CUSTOMER_NAME
)
SELECT CUSTOMER_NAME
	 , TOTAL_SPENT
	 , CASE 
		 WHEN PR < 0.2 THEN 1
         WHEN PR < 0.4 THEN 2
         WHEN PR < 0.6 THEN 3
         WHEN PR < 0.8 THEN 4
         ELSE 5
   END AS CUSTOMER_TIER
  FROM c_rank
 ORDER BY CUSTOMER_TIER DESC, TOTAL_SPENT DESC
;

--
--EXPLAIN PLAN FOR
--SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);