# Load packages
library(kableExtra)
library(knitr)
library(ggplot2)
library(hrbrthemes)
library(lubridate)
library(GGally)
library(ggrepel)
library(spotifyr)
library(tidyverse)


###################################################
############## SPOTIFY PLAYLIST DATA ##############
###################################################

# Spotify authorization tokens
Sys.setenv(SPOTIFY_CLIENT_ID = "xxx")
Sys.setenv(SPOTIFY_CLIENT_SECRET = "xxx")
spotifyr::get_spotify_authorization_code()


# Get Spotify Playlists
playlist1 <- spotifyr::get_playlist(playlist_id = "4lSykOrQfnAiCgtHKVudTT")
playlist2 <- spotifyr::get_playlist(playlist_id = "1nvpVNmzL7Vi1pXcQEiaLx")
playlist3 <- spotifyr::get_playlist(playlist_id = "7JJd5q4ZPK0P1Q4atTcpkR")
playlist4 <- spotifyr::get_playlist(playlist_id = "3NqHrY8dm9DBq29GowDFtw")
playlist5 <- spotifyr::get_playlist(playlist_id = "4qfffs5EG6ikw9YkhCGGDl")


# Get Playlist Tracks
playlist1_tracks <- playlist1$tracks$items
playlist2_tracks <- playlist2$tracks$items
playlist3_tracks <- playlist3$tracks$items
playlist4_tracks <- playlist4$tracks$items
playlist5_tracks <- playlist5$tracks$items


# Label and Merge Playlists
playlist1_tracks$playlist_name <- rep(
  playlist1$name[1],
  length(playlist1_tracks$added_at)
)
playlist2_tracks$playlist_name <- rep(
  playlist2$name[1],
  length(playlist2_tracks$added_at)
)
playlist3_tracks$playlist_name <- rep(
  playlist3$name[1], length(playlist3_tracks$added_at)
)
playlist4_tracks$playlist_name <- rep(
  playlist4$name[1], length(playlist4_tracks$added_at)
)
playlist5_tracks$playlist_name <- rep(
  playlist5$name[1], length(playlist5_tracks$added_at)
)


playlists_merged <- dplyr::bind_rows(playlist1_tracks, playlist2_tracks,
                                     playlist3_tracks, playlist4_tracks,
                                     playlist5_tracks)

# Get Track Features
n <- length(playlists_merged$track.id)
for (i in n) {
  if (i > 100) {
    playlist_idsA <- playlists_merged$track.id[1:100]
    playlist_idsB <- playlists_merged$track.id[101:200]
    playlist_idsC <- playlists_merged$track.id[201:300]
    playlist_idsD <- playlists_merged$track.id[301:400]
    playlist_idsE <- playlists_merged$track.id[401:500]
    playlist_idsF <- playlists_merged$track.id[501:600]
    playlist_idsG <- playlists_merged$track.id[601:700]
    playlist_idsH <- playlists_merged$track.id[701:i]
    #playlist_idsH <- playlists_merged$track.id[701:i]
    x <- rbind(
      get_track_audio_features(playlist_idsA),
      get_track_audio_features(playlist_idsB),
      get_track_audio_features(playlist_idsC),
      get_track_audio_features(playlist_idsD),
      get_track_audio_features(playlist_idsE),
      get_track_audio_features(playlist_idsF),
      get_track_audio_features(playlist_idsG),
      get_track_audio_features(playlist_idsH)
  )
    playlists_merged2 <- cbind(playlists_merged, x)
  }
}


# Choose column attributes
playlists_merged_tracks <- playlists_merged2 %>%
  dplyr::select(
    "added_at", "track.name", "track.id", "track.artists",
    "track.duration_ms", "track.popularity", "track.explicit",
    "track.album.id", "track.album.name", "track.album.release_date",
    "playlist_name",
    "danceability", "energy", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", "liveness",
    "valence", "tempo", "time_signature"
  )

# Format as dataframe
df <- playlists_merged_tracks %>%
  data.frame() %>%
  dplyr::mutate(
    artist_name = map_chr(track.artists, function(x) x$name[1]),
    added = as_date(added_at),
    release_date = as_date(track.album.release_date)
  ) %>%
  dplyr::select(
    "track.name", "track.id", "artist_name",
    "track.duration_ms", "track.popularity", "track.explicit",
    "track.album.name", "track.album.id", "release_date",
    "playlist_name",
    "danceability", "energy", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", "liveness",
    "valence", "tempo", "time_signature"
  )

colnames(df) <- c(
  "track_name", "track_id", "artist_name",
  "duration_ms", "popularity", "explicit", "album_name",
  "album_id", "release_date", "playlist_name",
  "danceability", "energy", "key", "loudness", "mode",
  "speechiness", "acousticness", "instrumentalness", "liveness",
  "valence", "tempo", "time_signature"
)


# Save as csv file
write.csv(df, file = "data/playlists.csv", row.names = TRUE, append = FALSE)




###################################################
############## PLAYLIST COVER IMAGES ##############
###################################################

mydf2 <- spotifyr::get_my_playlists(limit = 50) %>%
  dplyr::filter(public == TRUE) %>%
  dplyr::select(id, images, name, snapshot_id) %>% 
  dplyr::filter(id != '33SzrwTchxvwouepwsj8KV') %>%
  dplyr::filter(id != '09GJ0uEndlrfFWZXX423Jm') %>%
  dplyr::filter(id != '73zGnfOwzNdzMqymtECwkp') %>%
  dplyr::filter(id != '0cUfOXZrFRuz5xn5J9KwGj') %>%
  dplyr::filter(id != '1nvpVNmzL7Vi1pXcQEiaLx')

ximg <- mydf2$images 
get_images <- list()

for (i in 1:16) {
  myimage <- ximg[i] %>% data.frame() %>% 
    dplyr::filter(height == 640) %>% 
    dplyr::select(url) %>% 
    unlist(use.names = FALSE)
  
  tiger <- image_read(path = myimage, depth = 16, density = 2000)
  get_images <- append(get_images, tiger)
}

get_images <- image_scale(get_images, "1000x1000")
get_images1 <- image_append(image_scale(get_images[1:4], "x900"))
get_images2 <- image_append(image_scale(get_images[5:8], "x900"))
get_images3 <- image_append(image_scale(get_images[9:12], "x900")) 
get_images4 <- image_append(image_scale(get_images[13:16], "x900")) 
all_images <- c(get_images1, get_images2, get_images3, get_images4)


x <- image_append(image_scale(all_images, "x280"), stack = TRUE)
image_write(x, path = "my_playlists.png", format = "png",quality = 100,depth = 16,density = 1000)








mydf <- spotifyr::get_my_playlists(limit = 50) %>%
  dplyr::filter(public == TRUE) %>%
  dplyr::select(id, images, name, snapshot_id) %>% 
  dplyr::filter(id != '33SzrwTchxvwouepwsj8KV')


mydf %>%
  dplyr::select(id, name) %>% 
  kable(row.names = 1:nrow(mydf)) %>%
  kable_styling(font_size = 12, bootstrap_options = c("striped", "condensed"))


ximg <- mydf$images 
playlist_images <- list()

for (i in 1:20) {
  myimage <- ximg[i] %>% data.frame() %>% 
    dplyr::filter(height == 640) %>% dplyr::select(url) %>% 
    unlist(use.names = FALSE)
  tiger <- image_read(path = myimage, depth = 16, density = 1800)
  playlist_images <- append(playlist_images, tiger)
}

playlist_images <- image_scale(playlist_images, "800x800")

playlist_images1A <- image_append(image_scale(playlist_images[1:10], "x900"))
playlist_images1B <- image_append(image_scale(playlist_images[11:20], "x900"))
all_playlist_images <- c(playlist_images1A, playlist_images1B)


x2 <- image_append(image_scale(all_playlist_images, "x250"), stack = TRUE)
image_write(x2, path = "my_playlists2.png", format = "png",quality = 100,depth = 16,density = 1000)



