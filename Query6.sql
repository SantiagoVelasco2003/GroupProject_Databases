-- undo 
SELECT 
	b.title,
	b.language_code,
	r.average_rating,
	r.ratings_count, 
	((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop_score
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid); 

SELECT  
	p.pub_name, 
	((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop_score
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid)
JOIN publisher AS p ON b.pub_id=p.pub_id; 

-- publishers of 10 most popular books

SELECT  
	p.pub_name, 
	((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop_score
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid)
JOIN publisher AS p ON b.pub_id=p.pub_id 
ORDER BY pop_score DESC
LIMIT 10;


-- ranking bASed ON average popularity score 

SELECT  
	x.pub_name ,
	( AVG(x.pop_score)) AS avg_pop
FROM (SELECT  p.pub_name, ((r.ratings_count*r.average_rating)/(SELECT avg(ratings_count) FROM ratings)) AS pop_score
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid)
JOIN publisher AS p ON b.pub_id=p.pub_id ) AS x
GROUP BY x.pub_name
ORDER BY avg_pop DESC
