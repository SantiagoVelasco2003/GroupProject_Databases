/*Here we want to check if the popularity of a book is influenced
by the number of it's authors.*/ 
/*First we get the number of authors per book*/
SELECT ba.BookID, COUNT(ba.AuthorID) AS author_count
FROM Book_Authors ba
GROUP BY ba.BookID;

/*Using the formula ((specific amount of reviews/mean of amount of reviews)*specific rating 
value) to get popularity score, we compute popularity score for books*/

WITH review_stats AS (
    SELECT AVG(Ratings_Count) AS mean_reviews
    FROM Ratings
)
SELECT 
    r.BookID,
    (r.Ratings_Count / rs.mean_reviews) * r.Average_Rating AS popularity_score
FROM Ratings r
CROSS JOIN review_stats rs;

/*Combine calculated popularity score with number of authors for each book*/

WITH review_stats AS (
    SELECT AVG(Ratings_Count) AS mean_reviews
    FROM Ratings
),
popularity_calculated AS (
    SELECT 
        r.BookID,
        (r.Ratings_Count / rs.mean_reviews) * r.Average_Rating AS popularity_score
    FROM Ratings r
    CROSS JOIN review_stats rs
)
SELECT 
    pc.BookID,
    b.Title,
    COUNT(ba.AuthorID) AS author_count,
    pc.popularity_score
FROM popularity_calculated pc
JOIN Book_Authors ba ON pc.BookID = ba.BookID
JOIN Book b ON pc.BookID = b.BookID
GROUP BY pc.BookID, b.Title, pc.popularity_score
ORDER BY pc.popularity_score DESC;

/*Group results by author count to make analisis*/

WITH review_stats AS (
    SELECT AVG(Ratings_Count) AS mean_reviews
    FROM Ratings
),
popularity_calculated AS (
    SELECT 
        r.BookID,
        (r.Ratings_Count / rs.mean_reviews) * r.Average_Rating AS popularity_score
    FROM Ratings r
    CROSS JOIN review_stats rs
)
SELECT 
    author_count,
    AVG(popularity_score) AS avg_popularity_score,
    COUNT(BookID) AS num_books
FROM (
    SELECT 
        pc.BookID,
        COUNT(ba.AuthorID) AS author_count,
        pc.popularity_score
    FROM popularity_calculated pc
    JOIN Book_Authors ba ON pc.BookID = ba.BookID
    GROUP BY pc.BookID, pc.popularity_score
) subquery
GROUP BY author_count
ORDER BY author_count;

/*Query to view top 10 most popular books with multiple authors*/

WITH review_stats AS (
    SELECT AVG(Ratings_Count) AS mean_reviews
    FROM Ratings
),
popularity_calculated AS (
    SELECT 
        r.BookID,
        (r.Ratings_Count / rs.mean_reviews) * r.Average_Rating AS popularity_score
    FROM Ratings r
    CROSS JOIN review_stats rs
)
SELECT 
    b.Title,
    COUNT(ba.AuthorID) AS author_count,
    pc.popularity_score
FROM popularity_calculated pc
JOIN Book b ON pc.BookID = b.BookID
JOIN Book_Authors ba ON b.BookID = ba.BookID
GROUP BY b.Title, pc.popularity_score
HAVING COUNT(ba.AuthorID) > 1
ORDER BY pc.popularity_score DESC
LIMIT 10;

/*result of query with colums- bookid, author_count, popularity score is exported*/
COPY (
    WITH review_stats AS (
        SELECT AVG(Ratings_Count) AS mean_reviews
        FROM Ratings
    )
    SELECT 
        r.BookID,
        COUNT(ba.AuthorID) AS author_count,
        (r.Ratings_Count / rs.mean_reviews) * r.Average_Rating AS popularity_score
    FROM Ratings r
    CROSS JOIN review_stats rs
    JOIN Book_Authors ba ON r.BookID = ba.BookID
    GROUP BY r.BookID, r.Ratings_Count, r.Average_Rating, rs.mean_reviews
    ORDER BY popularity_score DESC
) TO 'C:/Users/HP/Downloads/databases group project github materials/q5_code/output.csv' CSV HEADER;
--CHANGE HERE TO YOUR DESIRED PATH







