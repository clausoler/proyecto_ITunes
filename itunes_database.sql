CREATE TABLE IF NOT EXISTS Artist (
    artist_Id INTEGER PRIMARY KEY,
    artistName TEXT,
    artistViewUrl TEXT
);


CREATE TABLE IF NOT EXISTS Genre (
    genre_Id SERIAL PRIMARY KEY,
    primaryGenreName TEXT
);


CREATE TABLE IF NOT EXISTS Album (
    collection_Id INTEGER PRIMARY KEY,
    collectionName TEXT,
    collectionCensoredName TEXT,
    release_Date DATE,
    collectionExplicitness TEXT,
    contentAdvisoryRating TEXT,
    collectionPrice FLOAT CHECK (collectionPrice >= 0),
    currency TEXT,
    trackCount INTEGER,
    discCount INTEGER,
    collectionViewUrl TEXT,
    collectionArtistName TEXT,
    collectionArtistViewUrl TEXT,
    artist_Id INT REFERENCES Artist(artist_Id)
);


CREATE TABLE IF NOT EXISTS Track (
    track_Id INTEGER PRIMARY KEY,
    trackName TEXT,
    trackNumber INTEGER,
    trackPrice FLOAT CHECK (trackPrice >= 0),
    discNumber INTEGER,
    trackTimeMillis INTEGER,
    trackExplicitness TEXT,
    release_Date DATE,
    trackViewUrl TEXT,
    is_Streamable BOOLEAN,
    kind TEXT,
    artist_Id INT REFERENCES Artist(artist_Id),
    collection_Id INT REFERENCES Album(collection_Id),
    genre_Id INT REFERENCES Genre(genre_Id)
);


CREATE TABLE IF NOT EXISTS Track_prices (
    id SERIAL PRIMARY KEY,
    trackPrice FLOAT CHECK (trackPrice >= 0),
    checked_at DATE,
    track_id INT REFERENCES Track(track_Id)
);


CREATE TABLE IF NOT EXISTS Album_prices (
    id SERIAL PRIMARY KEY,
    collectionPrice FLOAT CHECK (collectionPrice >= 0),
    checked_at DATE,
    collection_Id INT REFERENCES Album(collection_Id)
);