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
 
SELECT 
    a.collectionname,
    ap.checked_at::date AS fecha,
    ap.collectionprice
FROM album_prices ap
JOIN Album a ON ap.collection_id = a.collection_id
WHERE a.collectionname ILIKE '%Thriller%'  -- Cambia por el nombre que quieras analizar
ORDER BY fecha;
 
 
--Canciones con más variación de precio (diferencia entre mínimo y máximo)
SELECT 
    t.trackname,
    ar.artistname,
    MAX(tp.trackprice) - MIN(tp.trackprice) AS price_variation
FROM track_prices tp
JOIN track t ON tp.track_id = t.track_id
JOIN album a ON t.collection_id = a.collection_id
JOIN artist ar ON a.artist_id = ar.artist_id
GROUP BY t.trackname, ar.artistname
HAVING COUNT(*) > 1
ORDER BY price_variation DESC
LIMIT 10;
 
--Último precio registrado para cada álbum
SELECT 
    a.collectionname,
    ap.collectionprice,
    ap.checked_at
FROM album_prices ap
JOIN album a ON ap.collection_id = a.collection_id
WHERE (ap.collection_id, ap.checked_at) IN (
    SELECT collection_id, MAX(checked_at)
    FROM album_prices
    GROUP BY collection_id
)
ORDER BY ap.checked_at DESC;
 
-- Canciones cuyo precio ha bajado en los últimos días
SELECT *,
       max_price - min_price AS price_diff
FROM (
    SELECT 
        t.trackName,
        ar.artistName,
        MIN(tp.trackPrice) AS min_price,
        MAX(tp.trackPrice) AS max_price
    FROM track_prices tp
    JOIN Track t ON tp.track_Id = t.track_Id
    JOIN Album a ON t.collection_Id = a.collection_Id
    JOIN Artist ar ON a.artist_Id = ar.artist_Id
    GROUP BY t.trackName, ar.artistName
    HAVING MAX(tp.trackPrice) > MIN(tp.trackPrice)
) sub
ORDER BY price_diff DESC;
 
-- Canciones con duración mayor a 5 minutos
SELECT 
    t.trackName,
    ar.artistName,
    t.trackTimeMillis / 60000.0 AS duration_minutes
FROM Track t
JOIN Album a ON t.collection_Id = a.collection_Id
JOIN Artist ar ON a.artist_Id = ar.artist_Id
WHERE t.trackTimeMillis > 300000
ORDER BY duration_minutes DESC;
 
SELECT 
    tp.track_Id,
    COUNT(DISTINCT tp.trackPrice) AS num_precios_diferentes,
    COUNT(*) AS total_registros
FROM track_prices tp
GROUP BY tp.track_Id
HAVING COUNT(DISTINCT tp.trackPrice) > 1
ORDER BY num_precios_diferentes DESC;
 
SELECT 
    ap.collection_Id,
    COUNT(DISTINCT ap.collectionPrice) AS num_precios_diferentes,
    COUNT(*) AS total_registros
FROM album_prices ap
GROUP BY ap.collection_Id
HAVING COUNT(DISTINCT ap.collectionPrice) > 1
ORDER BY num_precios_diferentes DESC;
 
SELECT 
    ap.collection_Id,
    a.collectionname,
    ap.checked_at::date AS fecha,
    ap.collectionprice
FROM album_prices ap
JOIN Album a ON ap.collection_Id = a.collection_Id
WHERE ap.collection_Id = 78989263
ORDER BY fecha;
