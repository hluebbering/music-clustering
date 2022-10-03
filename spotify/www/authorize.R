library(kableExtra)
library(knitr)
library(ggplot2)
library(hrbrthemes)
library(lubridate)
library(GGally)
library(ggrepel)
library(spotifyr)
library(tidyverse)



## Authentification function
authenticate <- function(id, secret) {
  # authenticate the spotify client stuff
  Sys.setenv(SPOTIFY_CLIENT_ID = id)
  Sys.setenv(SPOTIFY_CLIENT_SECRET = secret)
  
  access_token <- get_spotify_access_token()
}





# Spotify authorization tokens

Sys.setenv(SPOTIFY_CLIENT_ID = "4cf3afdca2d74dc48af9999b1b7c9c61")
Sys.setenv(SPOTIFY_CLIENT_SECRET = "f6ca08ad37bb41a0afab5ca1dc74b208")
mytoke <- spotifyr::get_spotify_authorization_code()
access_token <- get_spotify_access_token()
access_token <- get_spotify_access_token()


myPlaylists <- spotifyr::get_user_playlists(user_id = 'hannahluebbering')
myPlaylists <- myPlaylists %>% dplyr::select('name','id')



juice_wrld <- spotifyr::get_artist_audio_features(artist = 'Juice Wrld')
juice_wrld <- juice_wrld %>% dplyr::select('track_name','artist_name','artist_id','artists','album_release_date','album_name','danceability','energy','key','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','key_name')

juice_wrld_id <- unique(juice_wrld$artist_id)
juice_wrld_top_tracks <- spotifyr::get_artist_top_tracks(juice_wrld_id)
juice_wrld_top_tracks <- juice_wrld_top_tracks %>%
  dplyr::select('artists', 'name','popularity','album.name')

