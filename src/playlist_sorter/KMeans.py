import numpy as np
import random
import pandas as pd


class KMeans:
    def __init__(self, n_clusters=3, max_iter=200):
        self.n_clusters = n_clusters
        self.max_iter = max_iter


    def fit(self, X_df):
        clusters = []
        for _ in range(self.n_clusters):
            np.random.seed(10)
            clusters.append({'x_cluster':np.random.choice(X_df['x']), 'y_cluster': np.random.choice(X_df['y'])})
        self.clusters_df = pd.DataFrame(clusters)


        for _ in range(self.max_iter):
            X_df = self._assign_labels(X_df)
            new_centroids = self._update_centroids(X_df)

            if new_centroids.equals(self.clusters_df):
                break

            self.clusters_df = new_centroids        


    def _assign_labels(self, X_df):
        labels = []
        for _, row in X_df.iterrows():
            distances = []
            for _, point in self.clusters_df.iterrows():
                distance = np.sqrt((row['x'] - point['x_cluster'])**2 + (row['y'] - point['y_cluster'])**2)
                distances.append(distance)

            closest_label = distances.index(min(distances))
            labels.append(closest_label)

        X_df['label'] = pd.DataFrame({'label': labels})
        return X_df


    def _update_centroids(self, X_df):
        new_centroids = X_df.groupby('label').agg('mean')
        new_centroids.rename(columns={'x': 'x_cluster', 'y': 'y_cluster'}, inplace=True)
        new_centroids.index.name = None
        return new_centroids


    def inertia(self, X_df):
        X_df_copy = X_df.copy()
        clusters_df_copy = self.clusters_df.copy()
        clusters_df_copy.index.names = ['label']
        all_df = X_df_copy.merge(clusters_df_copy, how='left', on='label')
        all_df['difference'] = all_df.apply(lambda x: np.sqrt((x['x'] - x['x_cluster'])**2 + (x['y'] - x['y_cluster'])**2), axis=1)
        inertias = all_df.groupby('label').agg('sum')['difference'].sum()
        return inertias
