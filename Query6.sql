-- undo 
 /*select b.title,b.language_code,r.average_rating,r.ratings_count, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop_score
from (ratings as r join book as b on r.bookid=b.bookid) 

select  p.pub_name, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop_score
from (ratings as r join book as b on r.bookid=b.bookid)
join publisher as p on b.pub_id=p.pub_id 

-- undo end
*/

-- publishers of 10 most popular books
/*

select  p.pub_name, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop_score
from (ratings as r join book as b on r.bookid=b.bookid)
join publisher as p on b.pub_id=p.pub_id 
order by pop_score desc
limit 10
*/

-- ranking based on average popularity score 
/*
select  x.pub_name ,( avg(x.pop_score)) as avg_pop
from (select  p.pub_name, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop_score
	from (ratings as r join book as b on r.bookid=b.bookid)
	join publisher as p on b.pub_id=p.pub_id ) as x
group by x.pub_name
order by avg_pop desc

*/

