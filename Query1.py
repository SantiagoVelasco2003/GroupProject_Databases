import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

#Database CHANGE ACCORDING TO SETUP
DATABASE_CONFIG = {
    "dbname": "Goodreads",
    "user": "postgres",
    "password": "Boom",
    "host": "localhost",
    "port": 5432,
}

with psycopg2.connect(**DATABASE_CONFIG) as conn:
    print("Connection successful!")

cur = conn.cursor()

query = """
WITH popularity_calculation AS (
    SELECT
        b.bookid,
        b.num_pages,
        r.average_rating,
        r.ratings_count,
        (CAST (r.ratings_count AS FLOAT) / (SELECT AVG(ratings_count) FROM ratings)) * r.average_rating AS Popularity_Score
    FROM
        book b
    JOIN
        ratings r
    ON
        b.bookid = r.bookid
    WHERE 
        b.num_pages > 0 AND r.ratings_count > 0 AND r.average_rating > 0.5
)
Select 
	Popularity_Score,
	num_pages,
	bookid	 
from 
	popularity_calculation
order by
	popularity_score DESC
    """

try:
    cur.execute(query)
    results = cur.fetchall()
    
    if not results:
        print("No data returned from the query.")
    else:
        df = pd.DataFrame(results, columns=['popularity_score', 'num_pages', 'bookid'])
        print("Query results:")
        print(df.head())
        
        #Get correlation
        correlation = df.corr(method='pearson').loc['popularity_score', 'num_pages']
        print(f"Correlation between num_pages and Popularity: {correlation}")
except Exception as e:
    print("Error executing the query or processing results:", e)

cur.close()
conn.close()

#Plot
plt.figure(figsize=(10,6))
plt.scatter(df['num_pages'],df['popularity_score'],alpha=0.6,label='Books')
z = np.polyfit(df['num_pages'],df['popularity_score'],1)
p = np.poly1d(z)
plt.plot(df['num_pages'],p(df['popularity_score']),color='red',label='Trendline')
plt.title('Correlation between Number of Pages and Popularity')
plt.xlabel('Number of Pages')
plt.ylabel('Popularity Score')
plt.legend()
plt.grid(True)
plt.show()
