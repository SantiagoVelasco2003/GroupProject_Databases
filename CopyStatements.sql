COPY authors FROM 'C:\Program Files\PostgreSQL\authors.csv' DELIMITER ';' HEADER CSV;
COPY publisher FROM 'C:\Program Files\PostgreSQL\publisher.csv' DELIMITER ';' HEADER CSV;
COPY book FROM 'C:\Program Files\PostgreSQL\book.csv' DELIMITER ';' HEADER CSV;
COPY book_authors FROM 'C:\Program Files\PostgreSQL\book_authors.csv' DELIMITER ';' HEADER CSV;
COPY ratings FROM 'C:\Program Files\PostgreSQL\ratings.csv' DELIMITER ';' HEADER CSV;