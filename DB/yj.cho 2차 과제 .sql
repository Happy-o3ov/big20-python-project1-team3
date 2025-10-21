-- 1. 장르별 매출을 구하고 가장 많이 팔린 장르 순으로 조회
SELECT b.GENRE                          -- books 테이블에서 장르 컬럼을 선택 - books 테이블 별칭 b, GENRE: 책의 장르
      ,SUM(oi.Quantity) AS TOTAL_SOLD  -- 주문 항목의 주문 수량(oi.Quantity)을 합산하여 총 판매량(TOTAL_SOLD)으로 표시
FROM order_items oi                    -- 주문 항목 테이블(order_items)을 기준으로 조회 시작 - oi는 order_items에 별칭
JOIN books b ON oi.BOOK_ID = b.BOOK_ID -- 주문 항목과 책 테이블을 BOOK_ID 기준으로 조인
GROUP BY b.GENRE                       -- 장르별로 그룹화하여 집계
ORDER BY TOTAL_SOLD DESC             -- 총 판매량 기준으로 내림차순 정렬 (많이 팔린 순)
;
-- 2. Top 10 베스트셀러 작가와 판매총액 조회
SELECT 
    b.AUTHOR,                                 -- 책 테이블에서 작가 이름을 선택
    SUM(oi.Quantity * b.Price) AS TOTAL_REVENUE  -- 판매 수량 × 책 가격 = 총 매출액 계산 - Price :가격 , 총 매출액에 TOTAL_REVENUE 라는 이름 부여
FROM 
    order_items oi                            -- 주문 항목 테이블을 기준으로 조회 시작
JOIN 
    books b ON oi.BOOK_ID = b.BOOK_ID         -- 주문 항목(oi.BOOK_id)과 책 정보(b.BOOK_ID)를 BOOK_ID 기준으로 연결
GROUP BY 
    b.AUTHOR                                  -- 작가별로 그룹화하여 매출 집계
ORDER BY TOTAL_REVENUE DESC                        -- 총 매출액 기준으로 내림차순 정렬 (많이 번 작가 순)
FETCH FIRST 10 ROWS WITH TIES;                   -- 상위 10명의 작가 조회 / WITH TIES를 통해 동점이 있을 시 같이 출력


-- 3. 평균 가격 이상의 도서 목록 : 서브쿼리 활용
SELECT *                     -- books 테이블의 모든 열(전체 데이터는 *로 표시)을 선택
FROM books                  -- 대상 테이블은 'books'
WHERE price >= (            -- 조건: price(가격)가 평균 가격 이상인 경우만 선택
    SELECT AVG(price)       -- 서브쿼리 : books 테이블에서 price의 평균값을 계산
    FROM books              -- 평균을 계산할 대상 테이블은 동일한 'books'
);                          -- 서브쿼리 종료: 평균 가격을 기준으로 필터링

-- 4. 한 번도 주문하지 않은 고객 조회
SELECT *                      -- 고객 전체 정보 조회
FROM customers                -- 고객 테이블에서
WHERE customer_id NOT IN (    -- 서브쿼리 주문한 적 있는 고객 목록에 포함되지 않은 고객만 조회
    SELECT DISTINCT customer_id  -- 주문한 적 있는 고객 ID 목록 -> DISTINCT : 중복제외 
    FROM orders                  -- 주문 기록이 있는 테이블
);

-- 5. 2개 이상의 장르를 구매한 고객 조회 --? customer_id가 자료와 다름
SELECT *                            -- 고객 전체 정보 조회
FROM customers                      -- 고객 테이블에서
WHERE customer_id IN (              -- 아래 조건에 해당하는 고객만 조회
    SELECT customer_id              -- 2개 이상의 장르를 구매한 고객 ID만 선택
    FROM (
        SELECT o.customer_id,                        -- 주문한 고객 ID
               COUNT(DISTINCT b.genre) AS genre_count  -- 구매한 서로 다른 장르 수 (중복 제거 후 집계)
        FROM orders o                                -- 주문 테이블
        JOIN order_items oi ON o.order_id = oi.order_id   -- 주문 → 주문 항목 연결
        JOIN books b ON oi.book_id = b.book_id            -- 주문 항목 → 책 정보 연결
        GROUP BY o.customer_id                     -- 고객별로 그룹화
        HAVING COUNT(DISTINCT b.genre) >= 2        -- 서로 다른 장르가 2개 이상인 고객만 선택
    )
);


-- 6. VIP 고객 분석(10명) 조회 - 고객명, 고객별 전체 금액, 순위 조회
-- [CTE] 고객별 총 구매 금액 계산
WITH customer_totals AS (
    SELECT
        cu.customer_id,                          -- 고객의 고유 ID
        cu.customer_name,                        -- 고객 이름
        SUM(oi.price_per_unit * oi.quantity) AS total_amount  
        -- 고객이 구매한 총 금액: 주문 항목별 단가 × 수량을 모두 합산
    FROM customers cu
    JOIN orders o ON cu.customer_id = o.customer_id           
        -- 고객 테이블과 주문 테이블을 고객 ID 기준으로 연결
    JOIN order_items oi ON o.order_id = oi.order_id           
        -- 주문 테이블과 주문 항목 테이블을 주문 ID 기준으로 연결
    GROUP BY cu.customer_id, cu.customer_name                 
        -- 고객별로 그룹화하여 총 구매 금액을 계산
),
-- [CTE] 고객별 총 구매 금액 기준으로 순위를 매기는 임시 테이블 정의
ranked_customers AS (
    SELECT
        ct.customer_name,                          -- 고객 이름
        ct.total_amount,                           -- 고객의 총 구매 금액
        RANK() OVER (ORDER BY ct.total_amount DESC) AS customer_rank 
        -- RANK() 분석 함수 사용: 총 구매 금액 기준으로 내림차순 순위 부여
        -- 동일 금액일 경우 같은 순위를 부여하고 다음 순위는 건너뜀 (예: 1, 2, 2, 4)
    FROM customer_totals ct
)
-- 최종 출력: 상위 10명의 VIP 고객 정보 조회
SELECT 
    rc.customer_name,                             -- 고객 이름
    rc.total_amount,  	                          -- 총 구매 금액
    RANK() OVER (ORDER BY rc.TOTAL_AMOUNT DESC) AS customer_rank                               -- 순위
FROM ranked_customers rc
WHERE customer_rank <= 10
;                      -- 순위가 10 이하인 고객만 필터링 (상위 10명)


-- 7. 월별 매출 성장률 분석 - 월별, 월별 매출, 이전달 매출, 성장율 조회
-- [CTE] 월별 매출 집계
WITH monthly_sales AS (
    SELECT
        TO_CHAR(o.order_date, 'YYYY-MM') AS SALES_MONTH,  -- 주문 날짜를 'YYYY-MM' 형식으로 변환
        SUM(oi.price_per_unit * oi.quantity) AS MONTHLY_REVENUE  -- 월별 총 매출 계산
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')  -- 월별로 그룹화
)
-- [CTE] 월별 매출 + 이전달 매출 연결
    SELECT
        ms.SALES_MONTH,                      -- 현재 월
        ms.MONTHLY_REVENUE,                   -- 현재 월 매출
        LAG(ms.MONTHLY_REVENUE,1,0) OVER (ORDER BY ms.SALES_MONTH) AS prev_MONTHLY_REVENUE,  
        -- LAG(): 바로 이전 행의 매출 → 이전달 매출
        ROUND(
            CASE 
                WHEN LAG(ms.MONTHLY_REVENUE) OVER (ORDER BY ms.SALES_MONTH) = 0 THEN NULL
                ELSE ((ms.MONTHLY_REVENUE - LAG(ms.MONTHLY_REVENUE,1,0) OVER (ORDER BY ms.SALES_MONTH)) 
                      / LAG(ms.MONTHLY_REVENUE,1,1) OVER (ORDER BY ms.SALES_MONTH)) * 100
            END, 2
        ) AS growth_rate  -- 성장률 계산 (% 단위, 소수점 2자리)
    FROM monthly_sales ms;

 -- 8. 장르별 매출 기여도
SELECT 
    b.GENRE,  -- books 테이블 장르
    SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) AS REVENUE,  -- (단가 x 수량) 매출합계 -> AS로 REVENUE로 이름 지정
    ROUND(  -- 소수점 2자리 반올림
        (SUM(oi.PRICE_PER_UNIT * oi.QUANTITY) / 
         SUM(SUM(oi.PRICE_PER_UNIT * oi.QUANTITY)) OVER ()) * 100, 
        2
    ) AS CONTRIBUTION_PCT  -- 전체 매출 대비 각 장르의 비율(%) 
FROM BOOKS b  -- BOOKS 테이블 (책 정보)
JOIN ORDER_ITEMS oi  -- ORDER_ITEMS 테이블 (주문 상세)
    ON b.BOOK_ID = oi.BOOK_ID  -- 공통키 BOOK_ID로 연결
GROUP BY b.GENRE  -- 장르별로 묶어서 합계 계산
ORDER BY REVENUE DESC;  -- 매출이 높은 순으로 정렬


-- 9. 각 장르 내 가장 비싼 책 TOP3
 WITH ranked_price AS (   -- ① CTE 정의: 'ranked_price' 라는 가상 테이블 생성
    SELECT
        b.title,         -- 책 제목 (출력용)
        b.genre,         -- 장르 (파티셔닝 기준 & 출력용)
        b.price,         -- 가격 (정렬 및 출력용)
        -- RANK(): 각 파티션(장르) 내에서 price 기준으로 순위 부여
        -- PARTITION BY b.genre : 장르별로 순위를 다시 시작하도록 지정
        -- ORDER BY b.price DESC : 가격이 높은 순서대로 1, 2, 3... 순위를 매김
        RANK() OVER (PARTITION BY b.genre ORDER BY b.price DESC) AS price_rank
    FROM books b    
)
-- ② CTE 사용: 위에서 만든 ranked_price(가상 테이블)에서 조건 필터링
SELECT
    title,             -- 최종 출력 컬럼: 책 제목
    genre,             -- 최종 출력 컬럼: 장르
    price              -- 최종 출력 컬럼: 가격
FROM ranked_price
-- price_rank 컬럼은 CTE 내부에서 계산된 장르별 순위값
WHERE price_rank <= 3   -- 각 장르별로 상위 3위(1,2,3)까지만 선택
ORDER BY genre, price DESC;  -- 결과 정렬: 장르별로 묶고, 같은 장르 내에서는 가격 내림차순


  -- 10. 고객별 누적 구매액 : 100번 고객만 조회
SELECT 
    c.customer_id,               -- 고객 ID
    c.customer_name,             -- 고객 이름
    o.order_date,                -- 주문 일자
    o.total_amount,              -- 각 주문의 금액
    -- 누적합 계산: 고객별(order by 주문일자 순)
    SUM(o.total_amount) 
        OVER (PARTITION BY c.customer_id ORDER BY o.order_date) AS CUMULATIVE_SPENT
        -- PARTITION BY: 고객별로 계산 분리
        -- ORDER BY: 주문일자 순서대로 누적 합계 계산
FROM customers c                 -- 고객 테이블
JOIN orders o                    -- 주문 테이블과 조인
    ON c.customer_id = o.customer_id  -- 공통키(customer_id)로 연결
WHERE c.customer_id = 100        -- 100번 고객만 조회
ORDER BY o.order_date;           -- 주문일자 순으로 정렬
   

-- 11. 함께 가장 많이 팔린 도서 조합 : 10개만 조회
SELECT 
    b1.title AS book_1,             -- 첫 번째 책 제목
    b2.title AS book_2,             -- 두 번째 책 제목
    COUNT(*) AS pair_count          -- 두 책이 함께 팔린 횟수
FROM order_items oi1                -- 첫 번째 주문 항목
JOIN order_items oi2                -- 두 번째 주문 항목
    ON oi1.order_id = oi2.order_id  -- 같은 주문 내에서
   AND oi1.book_id < oi2.book_id    -- (A,B)와 (B,A) 중복 제거
JOIN books b1 ON oi1.book_id = b1.book_id   -- 첫 번째 책 정보 연결
JOIN books b2 ON oi2.book_id = b2.book_id   -- 두 번째 책 정보 연결
GROUP BY b1.title, b2.title         -- 책 제목 쌍으로 그룹화
ORDER BY pair_count DESC            -- 가장 자주 팔린 조합부터 정렬
FETCH FIRST 10 ROWS ONLY;           -- 상위 10개만 출력 (Oracle 기준)


    
-- 12. 휴면 가능성 VIP 고객 조회 
SELECT 
    c.customer_name AS CUSTOMER_NAME,       -- 고객 이름
    MAX(o.order_date) AS LAST_ORDER_DATE,   -- 가장 최근 주문일
    SUM(o.total_amount) AS LIFETIME_SPENT   -- 총 구매액
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING 
    SUM(o.total_amount) >= 500000           -- 총 구매액이 500,000 이상인 고객만
    AND MAX(o.order_date) <= ADD_MONTHS(SYSDATE, -6) -- 최근 6개월 내 주문 없는 고객
ORDER BY LIFETIME_SPENT DESC;               -- 총 구매액 높은 순으로 정렬
    

    
-- 13. 고객 등급 분류: 5개 등급으로 분리
-- [1단계] 고객별 총 구매액을 구하는 가상 테이블(CTE: Common Table Expression)
WITH customer_total AS (
    SELECT 
        c.customer_name,                       -- 고객 이름
        SUM(o.total_amount) AS total_spent      -- 각 고객이 주문한 금액(total_amount)의 총합
    FROM customers c                           -- 고객 정보 테이블
    JOIN orders o                              -- 주문 정보 테이블
        ON c.customer_id = o.customer_id        -- 두 테이블을 공통키(customer_id)로 연결 (고객-주문 매칭)
    GROUP BY c.customer_name                    -- 고객별로 묶어서 합계 계산
)

-- [2단계] 고객 총 구매액을 기준으로 등급 분류
SELECT
    customer_name AS CUSTOMER_NAME,             -- 고객 이름 (컬럼명 포맷 맞춤)
    total_spent AS TOTAL_SPENT,                 -- 총 구매액
    NTILE(5) OVER (ORDER BY total_spent DESC) AS CUSTOMER_TIER
    -- NTILE(5): 전체 데이터를 5개의 그룹(등급)으로 자동 분할
    -- ORDER BY total_spent DESC → 구매액이 높은 순으로 나눔
    -- 예: 1등급 = 상위 20%, 5등급 = 하위 20%
FROM customer_total                             -- 위에서 만든 가상 테이블 사용
ORDER BY total_spent DESC;                      -- 총 구매액이 높은 순으로 정렬


    
-- 중복 확인 코드
SELECT *
FROM ORDER_ITEMS
WHERE (ORDER_ID, BOOK_ID) IN (
    SELECT ORDER_ID, BOOK_ID
    FROM ORDER_ITEMS
    GROUP BY ORDER_ID, BOOK_ID
    HAVING COUNT(*) > 1
);






