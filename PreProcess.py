import pandas as pd

# Load the input CSV file
data = pd.read_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/books_database.csv')

#Make Sure integrity of File (Can be corrupted or with some bad entries)
def uniform_columnn(df, c_name, e_type):
    return all(isinstance(val, e_type) for val in df[c_name].dropna())
check_column = uniform_columnn(data,'average_rating', float)
print(f'All the values are numbers: {check_column}')
if check_column == False:
    print("Database has some errors please check")
    exit()

"""
IF Not all values are numbers: Run the code to identify and manually change the values of the database
def badvalues(df, c_name, e_type):
    return df[c_name][~df[c_name].dropna().map(lambda val: isinstance(val, e_type))]
if check_column == False:
    bad_values = badvalues(data,'average_rating', float)
    print("The values that are not numbers are:")
    print(bad_values)
"""  

# Generate IDs
data['Rat_ID'] = range(1, len(data) + 1)

# Split Authors Column "/"
data['authors'] = data['authors'].fillna('')
data = data.assign(authors=data['authors'].str.split('/'))
data = data.explode('authors')

# Duplicated Authors Management
data = data.reset_index(drop=True)
unique_authors = data[['authors', 'Gender']].drop_duplicates().reset_index(drop=True)
unique_authors['AuthorID'] = range(1, len(unique_authors) + 1)
data = data.merge(unique_authors, on=['authors', 'Gender'], how='left')
if 'AuthorID_x' in data.columns or 'AuthorID_y' in data.columns:
    data = data.drop(columns=['AuthorID_x'], errors='ignore')
    data = data.rename(columns={'AuthorID_y': 'AuthorID'})

#Split Publishers Column "/"
data['publisher'] = data['publisher'].fillna('')
data = data.assign(publisher=data['publisher'].str.split('/'))
data = data.explode('publisher')

#Duplicated Authors Management
data = data.reset_index(drop=True)
unique_pub = data[['publisher']].drop_duplicates().reset_index(drop=True)
unique_pub['Pub_ID'] = range(1, len(unique_pub) + 1)
data = data.merge(unique_pub, on=['publisher'], how='left')
if 'Pub_ID_x' in data.columns or 'Pub_ID_y' in data.columns:
    data = data.drop(columns=['Pub_ID_x'], errors='ignore')
    data = data.rename(columns={'Pub_ID_y': 'Pub_ID'})

# Create DataFrames for SQL tables
authors_df = unique_authors.rename(columns={'authors': 'author_name'})

#Assign Default valur to Gender (Processed Later)
authors_df['Gender'] = authors_df['Gender'].fillna('Unkown')

publisher_df = data[['Pub_ID', 'publisher']].drop_duplicates().reset_index(drop=True)
publisher_df.columns = ['Pub_ID', 'Pub_name']

book_df = pd.DataFrame({
    'BookID': data['bookID'],
    'Title': data['title'],
    'Num_Pages': data['num_pages'],
    'Isbn': data['isbn'],
    'Publication_Date': pd.to_datetime(data['publication_date'], errors='coerce'),
    'Language_Code': data['language_code'],
    'Pub_ID': data['Pub_ID']
}).drop_duplicates(subset=['BookID'])

book_authors_df = pd.DataFrame({
    'AuthorID': data['AuthorID'],
    'BookID': data['bookID']
}).drop_duplicates()

ratings_df = pd.DataFrame({
    'Rat_ID': data['Rat_ID'],
    'Text_Review_Count': data['text_reviews_count'],
    'Average_Rating': data['average_rating'],
    'Ratings_Count': data['ratings_count'],
    'BookID': data['bookID']
}).drop_duplicates(subset=['BookID'])

# Save Files
authors_df.to_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/authors.csv', sep=';', index=False)
publisher_df.to_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/publisher.csv', sep=';', index=False)
book_df.to_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/book.csv', sep=';', index=False)
book_authors_df.to_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/book_authors.csv', sep=';', index=False)
ratings_df.to_csv('C:/Users/sanvt/OneDrive/Documentos/PostgreSQL/Group_P/PythonCodes/ratings.csv', sep=';', index=False)

print("I finally Finished")
