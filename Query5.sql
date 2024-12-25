-- undo 
 /*select b.title,b.language_code,r.average_rating,r.ratings_count, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop_score
from (ratings as r join book as b on r.bookid=b.bookid) */

-- ordering by average popularity score

/*select b.language_code, avg ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) ) as pop_avg
from (ratings as r join book as b on r.bookid=b.bookid)
group by b.language_code
order by pop_avg desc*/

-- looking at the x most popular's language

/*select b.language_code, ((r.ratings_count*r.average_rating)/(select avg(ratings_count) from ratings)) as pop
from (ratings as r join book as b on r.bookid=b.bookid)

order by pop desc
limit 10
*/
