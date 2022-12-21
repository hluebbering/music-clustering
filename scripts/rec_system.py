from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re

# New Music Friday Playlist
playlist_link1 = 'https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk?si=b00c85a1c052408f'
playlist_URI1 = playlist_link1.split("/")[-1].split("?")[0]

# Most Necessary Playlist
playlist_link2 = 'https://open.spotify.com/playlist/37i9dQZF1DX2RxBh64BHjQ?si=9503cb431d684f7c'
playlist_URI2 = playlist_link2.split("/")[-1].split("?")[0]


playlist_data = pd.read_csv("data/spotify.csv")
# Duplicates of songs accross playlists
playlistDF = playlist_data.copy(deep = True)
playlistDF[['artist','name','playlist']].head(3)



# Drop song duplicates
def drop_duplicates(df):
    df['artists_song']=df.apply(lambda row: row['artist']+' - '+row['name'],axis=1)
    return df.drop_duplicates('artists_song')

songDF = drop_duplicates(playlistDF)
print(len(pd.unique(songDF.artists_song)) == len(songDF))


songDF = songDF[[
    'name', 'track_id', 'release_date', 'popularity', # Track Metadata
    'artist', 'artist_id', 'artist_pop', 'artist_genres', # Artist Info
    'danceability', 'energy', 'valence', 'tempo', # Audio Features - Mood
    'instrumentalness', 'loudness', 'speechiness', # Audio Features - Properties
    'acousticness', 'liveness', # Audio Features - Context
    'key', 'mode', 'time_signature' # Audio Features - Metadata
]]




# Get subjectivity & polarity using textblob
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Categorize polarity & subjectivity score
def getAnalysis(score, task="polarity"):
    if task == "subjectivity":
        if score < 1/3:
            return "low"
        elif score > 1/3:
            return "high"
        else:
            return "medium"
    else:
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

# Perform sentiment analysis on text
def sentiment_analysis(df, text_col):
    df['subjectivity'] = df[text_col].apply(getSubjectivity).apply(lambda x: getAnalysis(x,"subjectivity"))
    df['polarity'] = df[text_col].apply(getPolarity).apply(getAnalysis)
    return df

sentimentDF = sentiment_analysis(songDF, "name")
sentimentDF[['name', 'artist', 'subjectivity', 'polarity']].head(3)



# Create One Hot Encoded features of a specific column
def ohe_prep(df, column, new_name):
    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)    
    
    return tf_df # One-hot encoded features 
  
# One-hot encoding for the subjectivity 
subject_ohe = ohe_prep(sentimentDF, 'subjectivity','subject')
subject_ohe.iloc[0]




# TF-IDF implementation
tfidf = TfidfVectorizer()
tfidf_matrix =  tfidf.fit_transform(songDF['artist_genres'].apply(lambda x: " ".join(x)))

# Genres dataframe
genre_df = pd.DataFrame(tfidf_matrix.toarray())
genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
genre_df.reset_index(drop = True, inplace=True)
genre_df.iloc[0]



# artist_pop distribution descriptive stats
print(songDF['artist_pop'].describe())

# Normalization
pop = songDF[["artist_pop"]].reset_index(drop = True)
scaler = MinMaxScaler()
pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns = pop.columns)
pop_scaled.head()






def create_feature_set(df, float_cols):
    
    # Tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix =  tfidf.fit_transform(df['artist_genres'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    genre_df.reset_index(drop = True, inplace=True)
    
    # Sentiment analysis
    df = sentiment_analysis(df, "name")

    # One-hot encoding
    subject_ohe = ohe_prep(df, 'subjectivity','subject') * 0.3
    polar_ohe = ohe_prep(df, 'polarity','polar') * 0.5
    key_ohe = ohe_prep(df, 'key','key') * 0.5
    mode_ohe = ohe_prep(df, 'mode','mode') * 0.5

    # Normalization - scale popularity columns
    pop = df[["artist_pop","popularity"]].reset_index(drop = True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns = pop.columns) * 0.2 

    # Scale audio feature columns
    floats = df[float_cols].reset_index(drop = True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(floats), columns = floats.columns) * 0.2

    # Concanenate all features
    final = pd.concat([genre_df, floats_scaled, pop_scaled, subject_ohe, polar_ohe, key_ohe, mode_ohe], axis = 1)
    final.insert(loc=0, column='track_id', value=df['track_id'].values) # Add song name
    
    return final # Final set of features 




# Save data and generate features
float_cols = songDF.dtypes[songDF.dtypes == 'float64'].index.values
complete_feature_set = create_feature_set(songDF, float_cols=float_cols)



testDF = playlistDF[playlistDF['playlist'] == "but my feet in bottega"]

# Summarize playlist into a single vector
def generate_playlist_feature(feat_set, playlist_df):
    
    # Find song features in the playlist
    feat_set_playlist = feat_set[feat_set['track_id'].isin(playlist_df['track_id'].values)]    
    
    # Find all non-playlist song features
    feat_set_nonplaylist = feat_set[~feat_set['track_id'].isin(playlist_df['track_id'].values)]
    feat_set_playlist_final = feat_set_playlist.drop(columns = "track_id")
    
    # Single vector feature summarizing playlist
    return feat_set_playlist_final.sum(axis = 0), feat_set_nonplaylist
  
  
# Generate the features
feat_set_pl, feat_set_nonpl = generate_playlist_feature(complete_feature_set, testDF)

# Summarized playlist features
complete_feature_set
feat_set_pl




# Generated recommendation based on songs in aspecific playlist
def generate_playlist_recos(df, features, nonplaylist_features):
    
    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_40 = non_playlist_df.sort_values('sim',ascending = False).head(40)
    
    # Top 40 recommendations for that playlist
    return non_playlist_df_top_40
  
  
# features (pandas series): summarized playlist feature (single vector)
# nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist
  
  

