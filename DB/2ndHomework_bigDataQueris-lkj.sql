-- Part 1: 기본 조회 및 집계 
-- 1.장르별 매출을 구하고 가장 많이 팔린 장르 순으로 조회

/*
 * 대상 테이블 : 도서 + 주문항목
 * 1  from절에서 도서(BOOKS) 테이블과 와 주문항목(ORDER_ITEMS) 테이블를 도서아이디(BOOK_ID)로 INNER JOIN 한 후 
 * 2. group by절에서 장르(b.GENRE) 그룹핑하고
 * 3. select절에서 장르명과 주문항목(ORDER_ITEMS)의 주문수량(oi.QUANTITY)를 SUM() 해서 장르별 총 판매건수를 계산
 * 4. orderby절에서 TOTAL_SOLD 내림차순으로 정렬하여 조회
 */ 

SELECT b.GENRE  -- 장르
     , sum(oi.QUANTITY)  AS TOTAL_SOLD -- 장르별 판매건수 
--     , sum(oi.QUANTITY * oi.PRICE_PER_UNIT)  AS TOTAL_SOLD    -- 매출총액
  FROM BOOKS b 
  JOIN ORDER_ITEMS oi 
    ON oi.BOOK_ID = b.BOOK_ID 
 GROUP BY b.GENRE 
 ORDER BY TOTAL_SOLD desc; 
 
 
-- 2.Top 10 베스트셀러 작가와 판매총액 조회
 /*
  * 대상 테이블 : 도서+주문항목
  * 1. from절에서 도서(BOOKS) 테이블과 주문항목(ORDER_ITEMS)테이블을 BOOK_ID 로 INNER JOIN 하고
  * 2. group by절에서 b.author 별로 그룹핑한 후 
  * 3. select절에서 b.author와  order_items 테이블에서 주문수량과 단가를 곱해서 sum 해서 작가별 판매총액(revenu) 를 구한 후
  * 4. order by절에서 작가별 판매총액(revenue)를 내림차순으로 정렬하고 
  * 5. 첫 10개의 행을 가져오는데 동점이 있는 경우를 위해 WITH TIES로 출력함
  */
 
SELECT b.author -- 작가
     , SUM(oi.QUANTITY * oi.PRICE_PER_UNIT)  AS Revenue -- 작가별 판매총액
  FROM BOOKS b 
  JOIN ORDER_ITEMS oi ON oi.BOOK_ID = b.BOOK_ID 
 GROUP BY b.author 
 ORDER BY Revenue DESC
FETCH FIRST 10 ROWS WITH TIES
;

-- ranking 찍을 때 

-- 3. 평균 가격 이상의 도서 목록: 서브쿼리 활용
/* 
 * 대상 테이블 : BOOKS
 * 1. from절에서 테이블 BOOKS 선택 한 후
 * 2. where절에서 테이블 BOOKS 에서 전체 도서의 평균값을 구하는 scalar subquery를 작성 한 후
 *                책 가격(price)이 subquery 보다 큰 row 들만 선택
 * 3. select절에서 BOOK_ID와 PRICE 컬럼을 가져와
 * 4. order by절에서 PRICE 내림차순으로 조회
 */
SELECT b.BOOK_ID -- 도서아이디
     , b.PRICE   -- 가격
  FROM BOOKS b
 WHERE b.PRICE >= (    
    SELECT AVG(price) AS avg_price FROM BOOKS  -- 평균값 구하는 SCALA SUBQUERY
    ) 
 ORDER BY b.PRICE desc
  ;
 
  /*
   * 위와 같이 처리하면 매번 서브쿼리를 타니까... 
   * CTE 사용해서 cross join 한 후  where 조건에서 비교
   */
WITH avgPriceBook AS ( 
    SELECT AVG(price) AS avg_price FROM BOOKS  
)
SELECT b.BOOK_ID
     , b.PRICE
  FROM BOOKS b, avgPriceBook apb
 WHERE b.PRICE >= apb.avg_price
 ORDER BY b.PRICE desc
  ;


 

-- 4. 한 번도 주문하지 않은 고객 조회
/*
 * 대상 테이블 : 고객+주문
 * 1. from절에서 고객(CUSTOMERS)과 주문(ORDERS) 테이블를 고객ID(CUSTOMER_ID)로 LEFT JOIN 한 후
 * 2. where절에서 주문테이블의 고객ID 가 NULL 인, 주문 내역이 없는 행을 가져와 
 * 3. select절에서 고객아이디와 고객명을 SELECT 한 후
 * 4. order by절에서 고객아이디 순으로 정렬하여 조회 
 */  
SELECT c.CUSTOMER_ID    -- 고객아이디
     , c.CUSTOMER_NAME  -- 고객명
  FROM CUSTOMERS c 
  LEFT JOIN ORDERS o
    ON c.CUSTOMER_ID = o.CUSTOMER_ID 
  WHERE o.CUSTOMER_ID IS null -- 주문테이블에 없는 고객
  ORDER BY c.CUSTOMER_ID 
  ;
  



-- 5. 2개 이상의 장르를 구매한 고객 조회

/*
 * 테이블 선정 : 고객, 주문(고객과 주문항목 정보), 주문항목(구매한 책 정보)
 * 
 * 1. from절에서 고객테이블과 주문 테이블을 고객아이디로 INNER JOIN : 구매한 이력이 있는 고객를 가져온다.
 * 1. from절에서 주문항목 테이블과 주문 테이블을 주문아이디로 조인 : 구매 고객이 어떤 책을 구매했는지 알 수 있다.  
 * 1. from절에서 거기에 도서 테이블을 주문항목 테이블과 도서아이디로 조인 : 구매 항목 도서의 장르 정보를 알 수 있다.
 * 2. group by절에서 이제 고객아이디와 고객명 2개로 그룹핑한 후
 * 3. HAVING 절로 GENRE를 DISTICT 해서 2 이상인 ROW만 선택하고
 * 4. select 절에서 고객아이디와 고객명 컬럼을 가져와 
 * 5. order by 절에서 고객아이디별로 정렬해서 출력
 */

SELECT C.CUSTOMER_ID    -- 고객아이디
     , C.CUSTOMER_NAME  -- 고객명
--     , O.ORDER_ID       -- 주문아이디(주문번호)
--     , OI.BOOK_ID       -- 구매한 도서아이디
--     , B.GENRE          -- 구매한 도서의 장르 
  FROM CUSTOMERS C
  JOIN ORDERS O       ON C.CUSTOMER_ID = O.CUSTOMER_ID
  JOIN ORDER_ITEMS OI ON O.ORDER_ID = OI.ORDER_ID
  JOIN BOOKS B        ON OI.BOOK_ID = B.BOOK_ID
 GROUP BY C.CUSTOMER_ID
       , C.CUSTOMER_NAME -- 고객별로 그룹화
HAVING COUNT(DISTINCT B.GENRE) >= 2 -- 고유한(DISTINCT) 장르의 수가 2개 이상인 그룹만 선택
 ORDER BY C.CUSTOMER_ID;  
  
/*
 * mq : main query, cte : cte query
 * cte 사용 방법
 * 
 * 우선 2개 이상 장르를 구매한 정보를 구하기 위해
 * cte1. form절에서 도서 테이블과 주문항목 테이블을 BOOK_ID로 조인한 후
 * cte1.1 select절에서 주문항목 테이블에 있는 BOOK_ID에 해당하는 도서의 장르 목록을 구해 확인 해 본다.
 * cte1.2 select절에서 해당 건에서 BOOK_ID와 B.GENRE 컬럼을 주석 처리한 후
 * cte2. group절에서 ORDER_ID 별로 GROUP BY 하고 
 * cte3. having절에서 2개 이상의 장르를 구매한 조건을 생성하고
 * cte4. select절에서 ORDER_ID와 구매한 장르를 DISTINCT로 COUNT 해서 컬럼을 선택 하는 CTE 를 생성한다.
 * 
 * mq1. from절에서 고객 테이블과 주문 항목 테이블을 고객ID로 JOIN 하고
 * mq1-1.          다시 주문 항목 테이블과 CTE로 생성한 테이블을 주문ID 로 조인해서 
 * mq2. group by절에서 고객 테이블의 고객아이디와, 고객명으로 GROUP BY 해서
 * mq3. select절에서 고객이이디와 고객명을 조회한다 
 *  
 */  
WITH multyGenreBuyer AS (
    SELECT oi.ORDER_id
--         , oi.BOOK_ID # 확인용 (GROUP BY 하기전)
--         , B.GENRE    # 확인용 (GROUP BY 하기전)
         , count(DISTINCT b.GENRE) AS cnt_genre          
      FROM BOOKS b
      JOIN ORDER_ITEMS oi ON b.BOOK_ID = oi.BOOK_ID 
     GROUP BY oi.order_id  
    HAVING count(DISTINCT b.GENRE) >= 2
)  
SELECT c.CUSTOMER_ID 
     , c.CUSTOMER_NAME 
  FROM CUSTOMERS c 
  JOIN ORDERS o  
    ON c.CUSTOMER_ID = o.CUSTOMER_ID 
  JOIN multyGenreBuyer mgb
    ON o.ORDER_ID = mgb.ORDER_ID
 GROUP BY c.CUSTOMER_ID, c.CUSTOMER_NAME 
;


-- Part 2: 중급 쿼리 (CTE, 분석 함수 기초) 
-- 6. VIP 고객 분석(10명) 조회- 고객명, 고객별 전체 금액, 순위 조회
/*
 * VIP 고객 : 구매 금액이 많은 고객으로 산정 
 * 
 * 대상 테이블 : 주문+고개 테이블
 * CTE를 써서
 * cte1. 주문 테이블에서 
 * cte2. 고객아이디로 그룹핑해서
 * cte3. 고객아이디와 총 구매금액, DENSE_RANK()  함수 사용 하여 총 구매금액별 내림차순으로 순위를 구한다. (동점자 처리)
 * 1. from절에서 고객명을 알기 위해 CTE와 고객 테이블을 고객아이디로 조인
 * 2. where절에서 순위가 10보다 작거나 같은 행들 가져오기
 * 3. select절에서 고객명, 총 구매금액, 순위 컬럼을 가져오고
 * 4. order by절에서 순위 컬럼 순으로 정렬한다.
 */

WITH RankedCustomers AS (
    SELECT O.CUSTOMER_ID  -- 고객아이디
         , SUM(O.TOTAL_AMOUNT) AS TOTAL_SPENT -- 고객아이디별 구매 총액
         , DENSE_RANK() OVER (ORDER BY SUM(O.TOTAL_AMOUNT) DESC) AS CUSTOMER_RANK -- 고객순위
      FROM ORDERS O          
     GROUP BY O.CUSTOMER_ID 
)
SELECT C.CUSTOMER_NAME -- 고객명
     , RC.TOTAL_SPENT  -- 고객별 구매총액
     , RC.CUSTOMER_RANK -- 순위
  FROM RankedCustomers RC
  JOIN CUSTOMERS C ON RC.CUSTOMER_ID = C.CUSTOMER_ID -- #4
 WHERE RC.CUSTOMER_RANK <= 10
 ORDER BY RC.CUSTOMER_RANK 
 ;
 
 
 

-- 7\. **월별 매출 성장률 분석** - 월별, 월별 매출, 이전달 매출, 성장율 조회
/*
 * 대상 데이블 : 주문(ORDERS)
 * 
 * 우선 CTE 로 월별 매출(Monthly_Revenue)을 집계한다.
 * cte1. from절에서 주문 테이블을 선택하고
 * cte2. group by절에서 TRUNK()함수를 사용해서 날짜를 해당 월의 1일로 잘라 월별로 그룹핑하고
 * cte3. select절에서 역시 TRUNK()함수를 사용해서 해당월을,
 *                    SUM(TOTAL_AMOUNT)를 통해서 월별 매출 총액을 집계한 후
 * cte4. order by절에서 해당 월별로 정렬한다. (이전 달 대비 성장율을 구하기 위해 반드시 오름차순으로 정렬해야 함)
 * mq1. from절에서 CTE 에서 생성한 테이블을 선택 한 후 
 * mq2. selec절에서 월별, 월별 매출, 이전달 매출, 성장율를 조회
 *         LAG() 함수를 이용해서현재 행의 바로 이전 행의 Monthly_Revenue 값을 가져옴. 이때 이전 달이 없으면 0을 기본값으로 준다.
 *         성장율은 (현재 매출 - 이전 달 매출) / 이전 달 매출 로 계산 
 *                  이때 이전 달 매출이 분모에 들어감으로 case end문을 사용해서 이전 달이 없는 경우는 현재 월의 매출액을 그냥 전달하고
 *                  이전 달 매출이 있는 경우는 위 식을 이용해 값을 구한 후 * 100 으로 % 화 시키고, round() 함수를 사용해 소숫점 2자리까지 구하고
 *                  뒤에 % 를 붙여 준다. 
 * mq3. 월 별 오름차순으로 정렬하여 조회한다.
*/
 
WITH MonthlySales AS (
    SELECT TRUNC(o.ORDER_DATE, 'MM') AS Sales_Month_Date -- 월
         , SUM(o.TOTAL_AMOUNT) AS Monthly_Revenue        -- 월별 매출 총액
      FROM ORDERS o
     GROUP BY TRUNC(ORDER_DATE, 'MM')
     ORDER BY Sales_Month_Date 
)
SELECT Sales_Month_Date -- 월
     , Monthly_Revenue  -- 월별 매출
     , LAG(Monthly_Revenue, 1, 0) OVER (ORDER BY Sales_Month_Date) AS previous_revenue -- 이전달 매출액
     , CASE 
         WHEN LAG(Monthly_Revenue, 1, 0) OVER (ORDER BY Sales_Month_Date) = 0 THEN Monthly_Revenue -- 이전달이 없는 경우 현재 월을 그냥 전달
         ELSE ROUND(
                (Monthly_Revenue - LAG(Monthly_Revenue, 1, 0) OVER (ORDER BY Sales_Month_Date)) 
                / LAG(Monthly_Revenue, 1, 0) OVER (ORDER BY Sales_Month_Date) * 100
                , 2
               )
       END || '%'  AS growth_rate -- 이전달 대비 성장율 
  FROM MonthlySales
 ORDER BY Sales_Month_Date
 ;
 
 

-- 8\. **장르별 매출 기여도** 장르, 매출액, 기여도
/*
 * 대상 테이블 : 도서+주문항목 테이블
 * 장르별 기여도는 ratio_to_report()함수 사용
 * 
 * 1. from절 : inline view를 사용해서 
 *    1.1.from : 도서+주문항목 테이블을 book_id 로 join 
 *    1.2.group by절 : 장르로 그룹핑
 *    1.3.select절 : 장르,
 *               주문항목의 구매수량*단가를 곱한 후 sum()함수로 집계해서 장르별 매출액 구하고
 *               ratio_to_report(장르별 매출금액) 를 구해서 round()함수로 소숫점 4자리까지 구한 후 * 100 하고 % 문자 붙여서 장르별 기여도 구해
 * 2. select절 : inline view 에서 나온 장르, 장르별 매출액, 장르별 기여도 컬럼을 뽑아
 * 3. order by절 : 장르별 기여도 내림차순으로 조회
 */
SELECT  gp.GENRE  -- 장르 
      , gp.REVENUE -- 장르별 매출액
      , gp.contribution_pct -- 장르별 기여도 
  FROM (
        SELECT b.genre  -- 장르 
             , SUM(oi.quantity * oi.price_per_unit) AS REVENUE -- 장르별 매출액
    --       , RATIO_TO_REPORT(sum(oi.quantity * oi.price_per_unit)) OVER () -- 기여도 구하기
             , ROUND(
                    RATIO_TO_REPORT(sum(oi.quantity * oi.price_per_unit)) OVER ()
                    , 4
               ) * 100 || '%' AS contribution_pct -- 장르별 기여도
         FROM BOOKS b
         JOIN ORDER_ITEMS oi ON b.BOOK_ID = oi.BOOK_ID 
        GROUP BY b.GENRE 
       ) AS GenrePCT gp
 ORDER BY gp.REVENUE DESC
 ;
 
 
  

-- 9\. **각 장르 내 가장 비싼 책 Top 3** 타이틀, 장르, 가격
/*
 * 대상 테이블 : 도서 
 * 
 * cte를 사용해서 우선 도서테이블에서 장르별 가격별 순위를 매김
 * cte1. from 절: 도서 테이블 선택
 * cte2. select 절: 타이틀, 장르, 가격,
 *                  DENSE_RANK()함수를 이용해서 장르별(PARTITION BY) 가격 내림차순 순위(PRICE DESC)를 매김 
 * mq1.From절 : CTE에서 생성한 테이블 선택
 * mq2.Where절: 순위를 조건(<=3)으로 row 뽑아서
 * mq3.Order By절: 장르, 가격은 역순으로 정렬해서 조회
* 
 */ 
WITH RankedBooks AS (
    SELECT TITLE -- 제목
         , GENRE -- 장르
         , PRICE -- 가격       
         , DENSE_RANK() OVER (PARTITION BY GENRE ORDER BY PRICE DESC) as D_RANK -- 장르별 가격 역순 순위
      FROM BOOKS
)
SELECT rb.TITLE -- 제목
     , rb.GENRE -- 장르 
     , rb.PRICE -- 가격       
  FROM RankedBooks rb
 WHERE rb.D_RANK <= 3 
 ORDER BY GENRE, PRICE DESC
 ;

     


-- **10\. 고객별 누적 구매액** : 100번 고객만 조회 : 주문일자, 주문금액, 주문 누적액
 /*
  * 대상테이블 : 주문(Orders)
  * 1.From절: 주문 테이블 선택
  * 2.Where절: 고객아이디 = 100번인 고객만 선택
  * 3.Select절: 주문일자, 주문금액, 누적금액을 계산
      3.1 SUM() 함수를 사용하여 누적 합계를 계산
          이때 parition by를 고객아이디를 줘서 고객별 그룹핑하고
          그런데 where 조건이 들어갔으니 주석처러
          order by를 주문일자(ORDER_DATE) 순서대로 정렬한 후 SUM() 계산
  */
SELECT ORDER_DATE        -- 주문일자
     , TOTAL_AMOUNT      -- 해당 주문 총액
     , SUM(TOTAL_AMOUNT) OVER (
--        PARTITION BY CUSTOMER_ID  
        ORDER BY ORDER_DATE       
      ) AS CUMULATIVE_SPENT -- 누적금액
  FROM ORDERS
 WHERE CUSTOMER_ID = 100 -- CUSTOMER_ID가 100인 고객만 필터링
 ORDER BY ORDER_DATE;
 


-- 11. **함께 가장 많이 팔린 도서 조합** : 10개만 조회 - BOOK1, BOOK2, PAIR_COUNT
/*
 * 대상 테이블 : 주문항목 (SELF)
 * 
 * 함께 팔린 책이란 한 주문(order_id)안에서 서로 다른 책을 판매한 경우라고 산정
    SELECT oi1.ORDER_ID 
         , oi1.BOOK_ID AS BOOK_ID1 -- 판매 책 ID
         , oi2.BOOK_ID AS BOOK_ID2 -- 함께 판매한 책 ID
      FROM ORDER_ITEMS oi1
      JOIN ORDER_ITEMS oi2
        ON oi1.ORDER_ID = oi2.ORDER_ID  -- 주문번호가 같은 것중에서
       AND oi1.BOOK_ID < oi2.BOOK_ID    -- 도서ID가 서로 다른 책
 * 같이 판매된 횟수를 카운트 하기 위해 group by book1, boo2      
    
 * 1. From절 : 주문항목 테이블을 주문ID는 같지만 판매한 도서는 다른 것으로 self join 한다. 
 *             이때 Book_ID 가 숫자형이므로 자기 자신이 아닌 다른 책을 찾을때 "<" 비교 연산자 사용.
 *             "!=" 비교연산자 사용했을때는 (1,2) vs (2,1)이 둘다 나옴 
 *             도서명을 출력하기 위해 테이블 BOOK 를 oi1.book_id 와 oi2.book_id 두번 다시 조인한다 *             
 * 2. GroupBy절: 판매책 제목과 같이 판매된 책 제목으로 그룹핑
 * 3. Select절: 판매책 제목, 함께 판매된 책 제목, 판매횟수를 count(*)로 집계 (그룹핑했으니까)
 * 4. OrderBy절: 판매횟수 큰순으로, 책 제목1, 책 제목2는 제목순을로 정렬 한 후 
 * 5. 전체 결과중에 상위 10위 동률 포함하여 가져오기    
 */

SELECT b1.TITLE AS Book1            -- 판매 책 제목
     , b2.TITLE AS Book2            -- 함께 판매된 책 제목
     , COUNT(DISTINCT oi1.order_id) AS PAIR_COUNT       -- 함께 판매된 횟수 이때 주문번호를 distinct 를 준다
--     , COUNT(*) AS PAIR_COUNT
  FROM ORDER_ITEMS oi1              -- 주문항목 테이블1
  JOIN ORDER_ITEMS oi2              -- self join되는 주문항목 테이블2 
       ON oi1.ORDER_ID = oi2.ORDER_ID       -- 주문번호가 같은 것중에서
       AND oi1.BOOK_ID < oi2.BOOK_ID        -- 도서ID가 서로 다른 책
  JOIN BOOKS b1 ON oi1.BOOK_ID = b1.BOOK_ID -- 첫 번째 도서의 이름 조회
  JOIN BOOKS b2 ON oi2.BOOK_ID = b2.BOOK_ID -- 두 번째 도서의 이름 조회
WHERE oi1.ORDER_id = 587
 GROUP BY b1.TITLE, b2.TITLE                -- 카운트를 하기 위해 그룹핑
 ORDER BY PAIR_COUNT DESC, Book1, Book2
 FETCH FIRST 10 ROWS WITH TIES
 ;
