select count(*) from genre g 
select * from genre 
 
select count(*) from artist a
select * from artist

select count(*) from album a
select * from album 
 
select a."artistname", a2."collectionname"
from artist a 
inner join album a2 
on a.artist_id = a2.artist_id 
order by a.artistname 

select count(*) from track t
select * from track t
 
select g."primarygenrename", t."trackname"
from genre g 
left join track t  
on g.genre_id = t.genre_id 
order by t.trackname
 
select count(*) from album_prices
select * from album_prices
 
select a."collectionname", ap."id", ap."checked_at", a.collectionprice 
from album a  
inner join album_prices ap   
on a.collection_id = ap.collection_id 
order by ap.checked_at desc
 
select count(*) from track_prices
select * from track_prices
