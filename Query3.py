import pandas as pd
import psycopg2
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns


#Connecting to SQL

db_config = {
    'dbname': 'GoodReadsDatabase',
    'user': 'postgres',
    'password': 'Josef2804!',
    'host': 'localhost',
    'port': 5433,
}

try:
    conn = psycopg2.connect(**db_config)
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")


#Fetching data about the gender of the author and the popularity score ((amount of reviews/mean amount of reviews)*specific rating value)

query = """
WITH mean_reviews AS (
    SELECT AVG(ratings_count) AS mean_ratings_count
    FROM ratings
)
SELECT 
    a.gender,
    r.ratings_count,
    r.average_rating,
    r.ratings_count / mr.mean_ratings_count * r.average_rating AS popularity_score
FROM 
    authors a
JOIN 
    book_authors ba ON a.authorid = ba.authorid
JOIN 
    ratings r ON ba.bookid = r.bookid
CROSS JOIN 
    mean_reviews mr;
"""

# Execute the query and fetch data into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

print(df)

# Replace 'mostly male' with 'male' and 'mostly female' with 'female' and remove rows where gender is 'unknown'/'andy'
df['gender'] = df['gender'].replace({
    'mostly_male': 'male',
    'mostly_female': 'female'
})
df = df[df['gender'] != 'unknown']
df = df[df['gender'] != 'andy']

# Print the cleaned DataFrame
print(df)
print("Genders after replacement:", df['gender'].unique())







# Independent t-test

male_scores = df[df['gender'] == 'male']['popularity_score']
female_scores = df[df['gender'] == 'female']['popularity_score']
t_stat, p_value = stats.ttest_ind(male_scores, female_scores, equal_var=False)  

# Print the results
print(f"T-statistic: {t_stat:.2f}")
print(f"P-value: {p_value:.3f}")


def plot_gender_scores(df, y_limit=5, title="Mean Popularity Score by Gender"):
    
    # Calculate mean and standard error for each gender
    grouped = df.groupby('gender')['popularity_score']
    mean_scores = grouped.mean()  # This is a pandas Series
    stderr_scores = grouped.sem()  # This is also a pandas Series
    

    # Plotting the bar chart
    plt.figure(figsize=(8, 6))
    plt.ylim(0, y_limit)
    
    plot = sns.barplot(
        x=mean_scores.index, 
        y=mean_scores, 
        palette=['white', 'white']
    )
    
    # Borders
    for bar in plot.patches:
        x, y, width, height = bar.get_bbox().bounds
        plot.add_patch(patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='black', facecolor='none'))
    
    # Error Bars
    plt.errorbar(
        x=range(len(mean_scores.index)), 
        y=mean_scores, 
        yerr=stderr_scores, 
        fmt='none', 
        ecolor='black', 
        capsize=5
    )
    
    for i, mean in enumerate(mean_scores):
        plt.text(i, mean - 2, f"M = {mean:.2f}", ha='center', va='baseline', fontsize=10, fontweight='bold')

    plt.title(title)
    plt.xlabel("Gender")
    plt.ylabel("Mean Popularity Score")
    plt.show()

plot_gender_scores(df, y_limit=5, title=f"Popularity Scores by Gender: T-statistic = {t_stat:.2f}, P-value = {p_value:.3f}")