--1 장르별 매출(개수)을 구하고 가장 많이 팔린 장르 순으로 조회
SELECT b.GENRE ,						--장르
	   SUM(oi.QUANTITY )AS TOTAL_SOLD	--매출(개수)
  FROM ORDER_ITEMS oi 					
  JOIN BOOKS b							--장르데이터에 접근하기위한 join 
    ON b.BOOK_ID = oi.BOOK_ID 			--order_items의 book_id와 books의 book_id가 동일
 GROUP BY b.GENRE 						--장르별(그룹화)
 ORDER BY TOTAL_SOLD DESC				--전체매수로 내림차순 가장 많이 팔린 컬럼이 위로
;
--2 top10 베스트셀러 작가와 판매총액 조회
WITH rankedauthor AS(										--서브쿼리
SELECT b.AUTHOR ,											--저자
	   COUNT(oi.QUANTITY) AS total_qua,						--팔린 책의개수
	   SUM(oi.PRICE_PER_UNIT *oi.QUANTITY ) AS TOTAL_REVENUE--판매 총액
  FROM ORDER_ITEMS oi										
  JOIN BOOKS b												--저자데이터에 접근하기위한 join
    ON b.BOOK_ID = oi.BOOK_ID								--order_items의 book_id와 books의 book_id가 동일
 GROUP BY b.AUTHOR 											--작가(그룹화)
 ORDER BY TOTAL_REVENUE DESC								--판매총액으로 내림차순 가장많은총액이 위로
)
SELECT ra.AUTHOR ,											--저자
	   ra.TOTAL_REVENUE 									--판매총액
  FROM rankedauthor ra
 WHERE ROWNUM <= 10											--상위 10개(top10)
;
--3 평균 가격 이상의 도서 목록
SELECT b.TITLE ,											--제목
	   b.PRICE 												--가격
  FROM books b
 WHERE (													--평균가격보다 높은 가격
 SELECT AVG(price)
   FROM books												--평균가격
 ) <= b.PRICE 												
;
--4 한번도 주문하지 않은 고객
SELECT c.CUSTOMER_ID ,										--고객id									
	   c.CUSTOMER_NAME										--고객이름
  FROM CUSTOMERS c 
  LEFT JOIN ORDERS o 										--주문데이터에 접근하기위한 join(left) 주문기록이없는(null)고객조회를위한 left join
    ON c.CUSTOMER_ID = o.CUSTOMER_ID 						--customers의 customer_id와 orders의 customer_id가 동일
 WHERE o.ORDER_ID IS NULL 									--주문id가 null인 고객조회 
;
--5 2개 이상의 장르를 구매한 고객조회
SELECT c.CUSTOMER_ID,										--고객id
       c.CUSTOMER_NAME										--고객이름
  FROM CUSTOMERS c
  JOIN ORDERS o 											--장르에접근하기위한 join
    ON c.CUSTOMER_ID = o.CUSTOMER_ID
  JOIN ORDER_ITEMS oi 										--장르에접근하기위한 join
    ON o.ORDER_ID = oi.ORDER_ID
  JOIN BOOKS b 												--장르에접근하기위한 join
    ON oi.BOOK_ID = b.BOOK_ID
 GROUP BY c.CUSTOMER_ID,									--고객id와이름(그룹화)
    	  c.CUSTOMER_NAME
 HAVING COUNT(DISTINCT b.GENRE) >= 2						--2개이상의 장르(중복제거)
;
--6 vip고객 분석(10명)조회
WITH vip_cust as(											--서브쿼리
SELECT c.CUSTOMER_NAME ,									--고객이름
	   SUM(o.TOTAL_AMOUNT)AS TOTAL_SPENT,					--총구매금액
	   dense_rank() OVER(ORDER BY SUM(o.TOTAL_AMOUNT) DESC) AS CUSTOMER_RANK --총구매금액순 순위 (내림차순)
  FROM CUSTOMERS c 
  JOIN ORDERS o 											--구매금액에 접근하기위한 join
    ON c.CUSTOMER_ID = o.CUSTOMER_ID						--customer의 customer_id와 orders의 customer_id가 동일
 GROUP BY c.CUSTOMER_NAME 									--고객이름(그룹화)
    ) 
SELECT vc.CUSTOMER_NAME ,									--고객이름
	   vc.TOTAL_SPENT ,										--총구매금액
	   vc.CUSTOMER_RANK 									--순위
  FROM vip_cust vc
 WHERE CUSTOMER_RANK <= 10									--순위가 10이내
;    
--7 월별 매출 성장률 분석
WITH month_order as(										--서브쿼리
SELECT TRUNC(o.ORDER_DATE, 'MM') AS SALES_MONTH,			--판매월
	   SUM(o.TOTAL_AMOUNT ) AS MONTHLY_REVENUE				--매출
  FROM ORDERS o 
 GROUP BY TRUNC(o.ORDER_DATE, 'MM')							--판매월(그룹화)
)
SELECT TRUNC(SALES_MONTH, 'MM') ,							--판매월
	   mo.MONTHLY_REVENUE ,									--판매액
	   LAG(mo.MONTHLY_REVENUE,1,0)OVER(ORDER BY mo.SALES_MONTH ASC) AS PREVIOUS_MONTHLY_REVENUE, --이전달매출
	   ROUND(												--성장률(%) (판매월매출-전월매출)/전월매출*100 
	   	(mo.MONTHLY_REVENUE - LAG(mo.MONTHLY_REVENUE,1,0)OVER(ORDER BY mo.SALES_MONTH))
	   	/LAG(mo.MONTHLY_REVENUE,1,1)OVER(ORDER BY mo.SALES_MONTH)*100
	   ,2)||'%' AS GROWTH_RATE
  FROM month_order mo
;
--8 장르 별 매출 기여도
WITH genre_revenue as(										--서브쿼리
	SELECT b.GENRE ,										--장르
	   	   SUM(oi.PRICE_PER_UNIT) AS REVENUE				--매수
  	  FROM ORDERS o 
  	  JOIN ORDER_ITEMS oi									--장르에 접근하기위한 join 
    	ON o.ORDER_ID = oi.ORDER_ID 
  	  JOIN BOOKS b 											--장르에 접근하기위한 join
    	ON oi.BOOK_ID = b.BOOK_ID 
 	 GROUP BY b.GENRE 										--장르(그룹화)
 )
SELECT gr.GENRE ,											--장르
	   gr.REVENUE ,											--매수
	   ROUND(
	   (RATIO_TO_REPORT(gr.REVENUE)OVER())*100
	   ,2)||'%'AS CONTRIBUTION_PCT							--매출기여도
  FROM genre_revenue gr
 ORDER BY CONTRIBUTION_PCT DESC
;
--9 각 장르 내 가장 비싼 책
WITH ranked_price AS(										--서브쿼리
	SELECT b.TITLE ,										--제목
	   b.GENRE ,											--장르
	   b.PRICE ,											--가격
	   DENSE_RANK()OVER(PARTITION BY b.GENRE ORDER BY b.PRICE DESC)AS ranked_genre --장르별 가격 순위
  	  FROM BOOKS b
)
SELECT rp.TITLE ,											--제목
	   rp.GENRE ,											--장르
	   rp.PRICE 											--가격
  FROM ranked_price rp
 WHERE rp.ranked_genre <= 3									--순위3이내(top3)
;
--10 고객별 누적 구매액 100번 고객
SELECT o.ORDER_DATE ,										--주문날짜
	   o.TOTAL_AMOUNT ,										--구매액
	   SUM(o.TOTAL_AMOUNT)over(PARTITION BY o.CUSTOMER_ID ORDER BY o.TOTAL_AMOUNT DESC)AS CUMULATIVE_SPENT--누적구매액
  FROM ORDERS o 
 WHERE o.CUSTOMER_ID = 100									--100번 고객
;
--11 함꼐 가장 많이 팔린 도서 조합 10개
SELECT b1.TITLE ,											--1권 제목
	   b2.TITLE ,											--2권 제목
	   COUNT(*)AS PAIR_COUNT								--조합횟수	
  FROM ORDER_ITEMS oi1 
  JOIN ORDER_ITEMS oi2										--조합횟수확인을위한 join
    ON oi1.ORDER_ID = oi2.ORDER_ID 							--oi1의 order_id와 oi2의 order_id가동일
   AND oi1.BOOK_ID < oi2.BOOK_ID							--oi1&oi2, oi2&oi1간 중복제거
  JOIN BOOKS b1												--제목데이터에 접근하기 위한 join
    ON b1.BOOK_ID = oi1.BOOK_ID 							--b1의book_id와 oi1의 book_id가동일
  JOIN BOOKS b2												--제목데이터에 접근하기 위한 join
    ON b2.BOOK_ID = oi2.BOOK_ID 							--b2의book_id와oi2의book_id가동일
 GROUP BY b1.TITLE ,b2.TITLE 								--1권 제목,2권 제목(그룹화)
 ORDER BY PAIR_COUNT DESC									--조합횟수 내림차순
 FETCH FIRST 10 ROW ONLY									--10개행출력
;
--12 휴면가능성 vip고객 총구매액500000이상,6개월 이상 구매x  
WITH ranked_date AS (										--서브쿼리
	SELECT c.CUSTOMER_NAME ,								--고객이름
	   min(o.ORDER_DATE)keep(DENSE_RANK LAST ORDER BY o.ORDER_DATE)
	   OVER(PARTITION BY c.CUSTOMER_ID)AS last_order_date,	--최근구매날짜
	   SUM(o.TOTAL_AMOUNT)OVER(PARTITION BY c.CUSTOMER_ID)AS lifetime_spent--총구매액
  	  FROM ORDERS o 
  	  JOIN CUSTOMERS c 										--고객이름에접근하기위한 join
    	ON o.CUSTOMER_ID = c.CUSTOMER_ID					--orders의 customer_id와 customers의 customer_id가동일
)
SELECT DISTINCT rd.CUSTOMER_NAME ,							--고객이름(중복제거)
	  rd.last_order_date,									--최근구매날짜
	  rd.LIFETIME_SPENT 									--총구매액
  FROM ranked_date rd
 WHERE MONTHS_BETWEEN(sysdate,rd.last_order_date) >= 6 AND	--6개월이상 구매이력x
 rd.LIFETIME_SPENT >= 500000								--총구매액 500000이상
 ;
 --13 고객등급분류
WITH sum_ranked as(											--서브쿼리
	SELECT c.CUSTOMER_NAME ,								--고객이름
	   	   SUM(o.TOTAL_AMOUNT) AS TOTAL_SPENT				--총구매액
  	  FROM ORDERS o 
  	  JOIN CUSTOMERS c 										--고객데이터접근을위한 join
    	ON o.CUSTOMER_ID =c.CUSTOMER_ID						--orders의 customer_id와 customers의 customer_id가동일
   	 GROUP BY c.CUSTOMER_ID ,c.CUSTOMER_NAME 				--고객id,고객이름 그룹화
)
SELECT sr.CUSTOMER_NAME ,									--고객이름
	   sr.TOTAL_SPENT ,										--총구매액
	   CASE													--구매순위(%)에따른등급분류
	   	WHEN ROUND(PERCENT_RANK()OVER(ORDER BY sr.TOTAL_SPENT desc)*100,2) <= 20 THEN '1'
	   	WHEN ROUND(PERCENT_RANK()OVER(ORDER BY sr.TOTAL_SPENT desc)*100,2) <= 40 THEN '2'
	    WHEN ROUND(PERCENT_RANK()OVER(ORDER BY sr.TOTAL_SPENT desc)*100,2) <= 60 THEN '3'
	    WHEN ROUND(PERCENT_RANK()OVER(ORDER BY sr.TOTAL_SPENT desc)*100,2) <= 80 THEN '4'
	    ELSE '5'
	   END AS CUSTOMER_RANK	
  FROM sum_ranked sr
;
--13 개선 ntile
SELECT c.CUSTOMER_NAME,
       SUM(o.TOTAL_AMOUNT) AS TOTAL_SPENT,
       NTILE(5) OVER(ORDER BY SUM(o.TOTAL_AMOUNT) DESC) AS CUSTOMER_RANK
FROM ORDERS o
JOIN CUSTOMERS c ON o.CUSTOMER_ID = c.CUSTOMER_ID
GROUP BY c.CUSTOMER_ID, c.CUSTOMER_NAME;
