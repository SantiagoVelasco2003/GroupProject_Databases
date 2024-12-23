import gender_guesser.detector as gender
import pandas as pd
import psycopg2


#Gender guesser
d = gender.Detector()

#Connect to database

DATABASE_CONFIG = {
    "dbname": "WhateverIwant",
    "user": "postgres",
    "password": "Josef2804!",
    "host": "localhost",
    "port": 5433,
}


with psycopg2.connect(**DATABASE_CONFIG) as conn:
    print("Connection successful!")

with conn.cursor() as cur:
    query = """SELECT A.authorid, A.author_name
        FROM authors AS A"""
    
    cur.execute(query)

    # Fetch all the rows
    rows = cur.fetchall()
    author_ids = [row[0] for row in rows]
    author_names = [row[1] for row in rows]


    result=[]
    first_words = [name.split()[0] for name in author_names]

    for text in first_words:
    # Pass it as Unicode
        result_gender = d.get_gender(u"{}".format(text))
        result.append(result_gender)

    print(result)

    update_query = "UPDATE authors SET gender = %s WHERE authorid = %s"
    for author_id, gender_value in zip(author_ids, result):
        cur.execute(update_query, (gender_value, author_id))

# Commit the changes
    conn.commit()
    print("Gender information updated in the authors table.")


#cur.close()
#conn.close()