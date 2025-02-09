from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import base64
from io import BytesIO


def scale_songs(tracks_all_analysis):
    songs = tracks_all_analysis[tracks_all_analysis['energy'].notnull()].reset_index()

    scaler = MinMaxScaler()
    songs[['loudness', 'tempo']] = scaler.fit_transform(songs[['loudness', 'tempo']])
    return songs


def fit_PCA(songs):
    features = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness','speechiness', 'tempo']

    """ 
    Use PCA to When there are many input attributes, it is difficult to visualize the data. 
    There is a very famous term ‘Curse of dimensionality in the machine learning domain. 
    Basically, it refers to the fact that a higher number of attributes in a dataset adversely affects the accuracy and training time of the machine learning model. 
    Principal Component Analysis (PCA) is a way to address this issue and is used for better data visualization and improving accuracy.
    """

    principal = PCA(n_components=2)
    principal.fit(songs[features])
    x = principal.transform(songs[features])
    x_df = pd.DataFrame({'x':x[:,0], 'y':x[:,1]})
    return x_df


def show_plots(x_df, KMeans):        
    means = []
    inertias = []

    for n in range(1, 20):
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(x_df)
        means.append(n)
        inertias.append(kmeans.inertia(x_df))

    fig, ax = plt.subplots(2, figsize=(12,12), facecolor="#d3d3d3")
    ax[0].plot(means, inertias)
    ax[0].set_xlabel('Number of clusters/playlists')
    ax[0].set_ylabel('Inertia')
    ax[0].set_xticks(np.arange(0,20))
    ax[0].grid()
    kmeans = KMeans(n_clusters=7)
    kmeans.fit(x_df)
    x_df.plot.scatter(x='x',y='y', c='label', colormap='viridis', ax=ax[1])
    ax[0].set_facecolor("#d3d3d3")
    ax[1].set_facecolor("#d3d3d3")
    ax[1].grid()
    plt.subplots_adjust(left=0.05, top=0.95)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


def show_cluster(x_df, n_clusters, KMeans):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(x_df)
    x_df.plot.scatter('x','y', c='label', colormap='viridis')
    plt.show()


# show_elbow_plot(x_df)
# show_cluster(x_df, 7)

# playlist_kmeans = KMeans(n_clusters=7)
# playlist_kmeans.fit(x_df)