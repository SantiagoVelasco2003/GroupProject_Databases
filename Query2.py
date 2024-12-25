import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Database CHANGE ACCORDING TO SETUP
conn = psycopg2.connect(
    dbname="Goodreads",
    user="postgres",
    password="Boom",
    host="localhost",
    port=5432,
)

query = """
WITH mean_ratings_count AS (
    SELECT AVG(ratings_count) AS mean_count
    FROM ratings
),
book_popularity AS (
    SELECT 
        b.bookid,
        b.title,
        r.text_review_count,
        r.average_rating,
        r.ratings_count,
        (r.ratings_count / (SELECT mean_count FROM mean_ratings_count) * r.average_rating) AS popularity_score
    FROM book b
    JOIN ratings r ON b.bookid = r.bookid
),
author_book_count AS (
    SELECT ba.authorid, COUNT(ba.bookid) AS book_count
    FROM book_authors ba
    GROUP BY ba.authorid
),
author_popularity AS (
    SELECT 
        a.authorid,
        a.author_name,
        ab.book_count,
        AVG(bp.popularity_score) AS avg_popularity_score
    FROM authors a
    JOIN author_book_count ab ON a.authorid = ab.authorid
    JOIN book_authors ba ON ab.authorid = ba.authorid
    JOIN book_popularity bp ON ba.bookid = bp.bookid
    GROUP BY a.authorid, a.author_name, ab.book_count
)
SELECT 
    authorid,
    author_name,
    book_count,
    avg_popularity_score
FROM author_popularity
ORDER BY avg_popularity_score DESC;
"""
df = pd.read_sql_query(query, conn)
print(df.head(10))

conn.close()

#Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='book_count', y='avg_popularity_score', data=df,alpha=0.2, color='red')
plt.title('Books Popularity Score vs. Number of Books by Author')
plt.xlabel('Number of Books by Author')
plt.ylabel('Average Book Popularity Score/Author')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
