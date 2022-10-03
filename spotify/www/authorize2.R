library(kableExtra)
library(knitr)
library(ggplot2)
library(hrbrthemes)
library(lubridate)
library(GGally)
library(ggrepel)
library(spotifyr)
library(tidyverse)
library(httr)
library(dplyr)


client_id <- '4cf3afdca2d74dc48af9999b1b7c9c61'
client_secret <- 'f6ca08ad37bb41a0afab5ca1dc74b208'

response <- POST(
  "https://accounts.spotify.com/api/token",
  config = httr::authenticate(
    user = Sys.getenv("client_id"),
    password = Sys.getenv("client_secret")
  ),
  body = list(grant_type = "client_credentials"), 
  encode = "form"
)


#extract content of response
token <-  content(response) 

# Paste token_type with access_token to make authorization
bearer.token <- paste(token$token_type, token$access_token)









# token <- POST('https://accounts.spotify.com/api/token',
#               accept_json(),
#               httr::authenticate(client_id, client_secret),
#               body = list(grant_type ='client_credentials'),
#               encode = 'form',
#               httr::config(http_version=2)) %>% 
#   content %>% .$access_token     


# ## Authentification function
# authenticate <- function(id, secret) {
#   # authenticate the spotify client stuff
#   Sys.setenv(SPOTIFY_CLIENT_ID = id)
#   Sys.setenv(SPOTIFY_CLIENT_SECRET = secret)
# 
#   access_token <- get_spotify_access_token()
# }











# ## favorite artists table function
# fav_artists <- function() {
#   as.data.frame(
#     get_my_top_artists_or_tracks(
#       type = 'artists', 
#       time_range = 'long_term', 
#       limit = 25) %>% 
#       rename(followers = followers.total) %>% 
#       select(.data$genres, .data$name, 
#              .data$popularity, .data$followers) %>% 
#       rowwise %>% 
#       mutate(genres = paste(.data$genres, collapse = ', ')) %>% 
#       ungroup
#   )
# }
# 
# ## datatableify fav_artists
# fav_artists_datatable <- function() {
#   datatable(
#     fav_artists()) %>% 
#     formatStyle(c('name', 'genres', 'popularity', 'followers'), 
#                 color = 'black')
# }
# 
# # audio features for top artists table function
# audio_features_fav_artist <- function(artist_name) {
#   get_artist_audio_features(
#     artist = artist_name, return_closest_artist = TRUE) %>% 
#     rename(positivity = valence) %>% 
#     select(.data$artist_name, .data$track_name, 
#            .data$album_name, .data$danceability, 
#            .data$energy, .data$loudness, .data$speechiness, 
#            .data$acousticness, .data$liveness, 
#            .data$positivity, .data$tempo) %>% 
#     distinct(.data$track_name, .keep_all= TRUE)
# }
# 
# ## datatablify audio_features
# sentiment_datatable <- function(artist_name) {
#   datatable(
#     audio_features_fav_artist(artist_name)) %>% 
#     formatStyle(c('artist_name', 'track_name', 
#                   'album_name', 'danceability', 'energy', 
#                   'loudness', 'speechiness', 'acousticness', 
#                   'liveness', 'positivity', 'tempo'), 
#                 color = 'black')
# }
# 
