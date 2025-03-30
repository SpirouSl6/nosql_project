MATCH (f1:Films), (f2:Films)
                        WHERE f1 <> f2 AND f1.title < f2.title  // Évite les doublons (A, B) et (B, A)
                        UNWIND split(f1.genre, ',') AS genre1
                        UNWIND split(f2.genre, ',') AS genre2
                        WITH f1, f2, genre1, genre2
                        WHERE genre1 = genre2
                        WITH f1, f2, COLLECT(DISTINCT genre1) AS genres_communs
                        RETURN f1.title AS Film1, f1.director AS Realisateur1, 
                               f2.title AS Film2, f2.director AS Realisateur2, 
                               genres_communs AS GenresPartages
                        LIMIT 10;