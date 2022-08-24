library(kableExtra)
library(knitr)
library(ggplot2)
library(hrbrthemes)
library(lubridate)
library(GGally)
library(ggrepel)
library(spotifyr)
library(tidyverse)

# Spotify authorization tokens

Sys.setenv(SPOTIFY_CLIENT_ID = '4cf3afdca2d74dc48af9999b1b7c9c61')
Sys.setenv(SPOTIFY_CLIENT_SECRET = 'f6ca08ad37bb41a0afab5ca1dc74b208')
spotifyr::get_spotify_authorization_code()


# Get Spotify Playlists

playlist1 <- spotifyr::get_playlist(playlist_id = "4lSykOrQfnAiCgtHKVudTT")
playlist2 <- spotifyr::get_playlist(playlist_id = "1nvpVNmzL7Vi1pXcQEiaLx")
playlist3 <- spotifyr::get_playlist(playlist_id = "7JJd5q4ZPK0P1Q4atTcpkR")


# Get Playlist Tracks

playlist1_tracks <- playlist1$tracks$items
playlist2_tracks <- playlist2$tracks$items


# Label and Merge Playlists

playlist1_tracks$playlist_name <- rep(playlist1$name[1],
                                      length(playlist1_tracks$added_at))
playlist2_tracks$playlist_name <- rep(playlist2$name[1],
                                      length(playlist2_tracks$added_at))



playlists_merged <- dplyr::bind_rows(playlist1_tracks, playlist2_tracks)



## Get Track Features

n <- length(playlists_merged$track.id)
for (i in n) {
  if (i > 100) {
    playlist_idsA <- playlists_merged$track.id[1:100]
    playlist_idsB <- playlists_merged$track.id[101:200]
    playlist_idsC <- playlists_merged$track.id[201:i]
    x <- rbind(get_track_audio_features(playlist_idsA),
              get_track_audio_features(playlist_idsB),
              get_track_audio_features(playlist_idsC))
    
    playlists_merged2 <- cbind(playlists_merged, x)
    
    
  }
  
}




# Choose column variables

playlists_merged_tracks <- playlists_merged2 %>%
  dplyr::select('added_at', 'track.name', 'track.id', 'track.artists', 
                'track.duration_ms', 'track.popularity', 'track.explicit', 
                'track.album.id', 'track.album.name', 'track.album.release_date', 
                'track.href', 'playlist_name', 
                "danceability", "energy", "key", "loudness", "mode", 
                "speechiness", "acousticness", "instrumentalness", "liveness", 
                "valence", "tempo", "time_signature")

# Format as dataframe

df <- playlists_merged_tracks %>% data.frame() %>%
  dplyr::mutate(artist_name = map_chr(track.artists, function(x) x$name[1]),
                added = as_date(added_at),
                release_date = as_date(track.album.release_date)) %>%
  dplyr::select('added', 'track.name', 'track.id', 'artist_name', 
                'track.duration_ms', 'track.popularity', 'track.explicit', 
                'track.album.name', 'track.album.id', 'release_date', 
                'track.href', 'playlist_name',
                "danceability", "energy", "key", "loudness", "mode", 
                "speechiness", "acousticness", "instrumentalness", "liveness", 
                "valence", "tempo", "time_signature")

colnames(df) <- c('date_added', 'track_name', 'track_id', 'artist_name', 
                  'duration_ms', 'popularity', 'explicit', 'album_name', 
                  'album_id',  'release_date', 'href', 'playlist_name',
                  "danceability", "energy", "key", "loudness", "mode", 
                  "speechiness", "acousticness", "instrumentalness", "liveness", 
                  "valence", "tempo", "time_signature")

# Save as csv file

write.csv(df, file = "scripts/playlists.csv", row.names = FALSE)


