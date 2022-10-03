# setup
# -----------------------------------------------------------------------------
library(shiny)
library(shinyWidgets)
library(dslabs)
library(tidyverse)
library(plotly)
library(shinydashboard)
library(rdrop2)
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

#source('www/authorize2.R')



# Create functions to make plots
Sys.setenv(SPOTIFY_CLIENT_ID = "4cf3afdca2d74dc48af9999b1b7c9c61")
Sys.setenv(SPOTIFY_CLIENT_SECRET = "f6ca08ad37bb41a0afab5ca1dc74b208")

client_id <- '4cf3afdca2d74dc48af9999b1b7c9c61'
client_secret <- 'f6ca08ad37bb41a0afab5ca1dc74b208'

ui <- dashboardPage(
  dashboardHeader(title = "Value boxes"),
  dashboardSidebar(
    textInput('userInput', label = "User ID", value = 'hannahluebbering'),
    uiOutput("secondSelection")
    #uiOutput("thirdSelection")
  ),
  dashboardBody(
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
    ),
    fluidRow(
      # A static valueBox
      valueBox(10 * 2, "New Orders", icon = icon("credit-card")),
      # Dynamic valueBoxes
      valueBoxOutput("progressBox")
    ),
    
    fluidRow(
      DT::dataTableOutput("mytable",height = 400),
      plotlyOutput("audio_features")
    ),
    fluidRow(
      column(width = 6,
        plotlyOutput("artist_name")),
      column(width = 6,
             plotlyOutput("genre_count"))
    )
  )
)



server <- function(input, output) {
  authorize <- get_spotify_authorization_code()
  #access_token <- get_spotify_access_token(client_id = client_id,
  #                                        client_secret = client_secret)
  
  
  output$progressBox <- renderValueBox({
    valueBox(
      paste0(25 + input$count, "%"), "Progress", icon = icon("list"),
      color = "purple"
    )
  })
  
  
  d1 <- reactive({
    spotifyr::get_user_playlists(user_id = input$userInput) %>% 
      dplyr::select('name','id')
  })
  
  output$secondSelection <- renderUI({
    selectInput("User", "Playlist", 
                choices = (d1())$name)
  })
  
  
  
  
  
  d2 <- reactive({
    spotifyr::get_playlist_audio_features(
      playlist_uris = d1()[d1()$name==input$User,"id"]) %>%
      data.frame() %>%
      dplyr::mutate(artist_name = map_chr(track.artists, function(x) x$name[1]),
                    artist_id = map_chr(track.artists, function(x) x$id[1]),
                    release_date = lubridate::as_date(track.album.release_date)) %>%
      dplyr::select(track.id, track.name, artist_id, artist_name, 
                    track.album.name, release_date,
                    track.explicit, track.popularity, track.duration_ms,
                    danceability, energy, loudness, speechiness, acousticness, 
                    instrumentalness, liveness, valence, tempo, key_mode) %>%
      dplyr::rename('track_name' = track.name, 'album' = track.album.name, 
                    'popularity' = track.popularity) %>% 
      dplyr::arrange(desc(popularity))
    
  })

  output$mytable = DT::renderDataTable({
    DT::datatable(
      d2() %>% 
        head(10) %>%
        dplyr::select(track_name, artist_name, album, 
                             popularity, release_date),
      escape = FALSE,
      options = list(searching = FALSE,
                     pageLength = 4,
                     lengthChange = FALSE)
      )
    })
  
  

  
  
  output$artist_name <- renderPlotly({
    artist_count <- d2() %>% 
      dplyr::count(artist_name) %>% 
      dplyr::arrange(desc(n)) %>%
      head(20) %>%
      ggplot(aes(x = reorder(artist_name, n), y = n, fill = n)) + 
      geom_bar(stat = "identity") +
      coord_flip() + theme_modern_rc(base_size = 10, plot_title_size = 11)
    
    ggplotly(artist_count)
    
  })
  
  
  output$genre_count <- renderPlotly({
    artist_ids <- d2() %>% 
      dplyr::select(artist_id) %>% dplyr::distinct()
    
    nartists <- nrow(artist_ids)
    artist_id_list <- unlist(artist_ids)
    total_artist_list = data.frame()
    
    for (i in 1:nartists){
      model <- spotifyr::get_artists(artist_id_list[i])
      df <- data.frame(model)
      # add vector to a dataframe
      total_artist_list <- rbind(total_artist_list, df)
    }
    
    genre_list <- unlist(total_artist_list$genres)
    genre_count <- data.frame("genre" = genre_list) %>%
      dplyr::count(genre) %>% dplyr::group_by(genre) %>%
      dplyr::arrange(desc(n)) 
    
    p <- ggplot(head(genre_count, 24), 
                mapping = aes(x = reorder(genre, n), y = n, fill = n)) + 
      geom_bar(stat = "identity") + 
      labs(title = "Genres in playlist", x = "Frequency", y = "Genre") +
      coord_flip() + theme_modern_rc(base_size = 10, plot_title_size = 11) 
    
    ggplotly(p)
    
  })
  
  
  
  output$audio_features <- renderPlotly({
    audio_features <- d2() %>%
      tidyr::pivot_longer(cols = c(danceability, energy, loudness, 
                                   speechiness, acousticness, instrumentalness, 
                                   liveness, valence, tempo),
                          names_to = "feature",
                          values_to = "value")
    
    feature_plot <- ggplot(audio_features, mapping = aes(x=value)) +
      geom_histogram(stat = 'bin', bins = 8, mapping = aes(fill = feature),
                     color='black') + 
      facet_wrap(vars(feature), scales = 'free')  + 
      #hrbrthemes::theme_ipsum_rc(base_size = 8,strip_text_size = 11, strip_text_face = "bold") + 
      xlab(NULL) + ylab(NULL) + theme(legend.position = "none") + 
      scale_fill_manual(values = c('red','blue','magenta','plum','purple','pink','hotpink','green','navy','aquamarine'))
    ggplotly(feature_plot)
    
  })

  
  
  
  
  
  output$feature <- renderPlotly({
    d2() %>%
      tidyr::pivot_longer(cols = c(danceability, energy, loudness, 
                                   speechiness, acousticness, instrumentalness, 
                                   liveness, valence, tempo),
                          names_to = "feature",
                          values_to = "value") %>%
      plot_ly(x = ~feature, y = ~value, color = ~feature)
    
  })
  
  
  
  
  
  
  
  
  
  
  
  
  
  output$thirdSelection <- renderUI({
    selectizeInput("artistInput", "Artist",
                   choices = unique((d2()$artist_name)),
                   multiple = TRUE) 
  })
  
  d3 <- reactive({
    d2() %>%
      filter(artist_name == input$artistInput)
  })
  
  output$artistplot <- renderPlot({
    
    ggplot(d3(), aes(x= artist_name, y = popularity, color=track_name)) +
      geom_point() + 
      theme_bw() + hrbrthemes::theme_ipsum() +
      xlab("Year") +
      ggtitle("Cases over time")
  })
  
  

 
}

shinyApp(ui=ui, server=server)
