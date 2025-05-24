# Descripción de columnas del DataFrame de iTunes

| **Columna**                | **Descripción** |
|----------------------------|-----------------|
| `wrapperType`              | Tipo general del resultado (`track`, `collection`, etc.) |
| `kind`                     | Tipo específico de media (`song`, `music-video`, etc.) |
| `artistId`                 | Identificador único del artista |
| `collectionId`             | Identificador único del álbum o colección |
| `trackId`                  | Identificador único de la canción o pista |
| `artistName`               | Nombre del artista |
| `collectionName`           | Nombre del álbum o colección |
| `trackName`                | Título de la canción o pista |
| `collectionCensoredName`   | Nombre censurado del álbum (sin lenguaje explícito) |
| `trackCensoredName`        | Nombre censurado de la canción (sin lenguaje explícito) |
| `artistViewUrl`            | Enlace a la página del artista en iTunes |
| `collectionViewUrl`        | Enlace a la página del álbum en iTunes |
| `trackViewUrl`             | Enlace a la página de la canción en iTunes |
| `previewUrl`               | URL para escuchar un fragmento de la canción |
| `artworkUrl30`             | Imagen de portada (30×30 px) |
| `artworkUrl60`             | Imagen de portada (60×60 px) |
| `artworkUrl100`            | Imagen de portada (100×100 px) |
| `collectionPrice`          | Precio del álbum o colección |
| `trackPrice`               | Precio individual de la canción |
| `releaseDate`              | Fecha de publicación de la canción o álbum |
| `collectionExplicitness`   | Indicador de contenido explícito en el álbum |
| `trackExplicitness`        | Indicador de contenido explícito en la canción |
| `discCount`                | Total de discos en la colección |
| `discNumber`               | Número de disco al que pertenece la canción |
| `trackCount`               | Total de canciones en la colección |
| `trackNumber`              | Número de pista dentro del disco |
| `trackTimeMillis`          | Duración de la canción en milisegundos |
| `country`                  | País de origen de los datos (en este caso, EE. UU.) |
| `currency`                 | Moneda del precio (por ejemplo, USD) |
| `primaryGenreName`         | Género principal de la canción |
| `isStreamable`             | Indica si la canción se puede reproducir en streaming |
| `collectionArtistId`       | ID del artista de la colección (si es distinto del principal) |
| `collectionArtistName`     | Nombre del artista principal de la colección |
| `collectionArtistViewUrl`  | URL del artista de la colección |
| `contentAdvisoryRating`    | Clasificación de contenido (`Explicit`, `Clean`, etc.) |
| `checked_at`               | Fecha de extracción del dato (fecha del scraping) |

## cleaned suele aplicarse a álbumes de hip-hop o pop que tienen una versión "radio edit" o familiar.

## explicit indica que el contenido no ha sido modificado y puede tener lenguaje fuerte.

## notExplicit representa álbumes que nunca incluyeron contenido sensible.