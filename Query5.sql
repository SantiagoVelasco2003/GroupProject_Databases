-- undo 
SELECT
	b.title,
	b.language_code,
	r.average_rating,r.ratings_count, 
	((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop_score
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid);

-- ordering by average popularity score

SELECT 
	b.language_code, 
	AVG ((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop_avg
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid)
GROUP BY b.language_code
ORDER BY pop_avg DESC;

-- looking at the x most popular's language

SELECT 
	b.language_code, 
	((r.ratings_count*r.average_rating)/(SELECT AVG(ratings_count) FROM ratings)) AS pop
FROM (ratings AS r JOIN book AS b ON r.bookid=b.bookid)
ORDER BY pop DESC
LIMIT 10
