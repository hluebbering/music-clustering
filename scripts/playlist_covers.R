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
    dplyr::filter(height == 640) %>% dplyr::select(url) %>% 
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

image_append(image_scale(all_images, "x900"), stack = TRUE)






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


