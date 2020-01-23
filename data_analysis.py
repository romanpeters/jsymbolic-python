import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt


def feature_histogram(data_frame, feature_id):
    plt.hist(data_frame[feature_id], bins=n_tunes//5)
    plt.title(f"histogram of feature#: {feature_id}")
    plt.show()

def show_all_histograms(data_frame):
    for i in range(0, n_features):
        feature_histogram(data_frame, i)

# Returns a 3-valued tuple, with a PCA object (containing the transformations),
#   a dataframe that has the transformations applied to it
#   and the scaler object that was used to scale the data. We will scale
#   subsequent queries according to the properties in the scaler.   
def pca_decomposition(data_frame):
    #Standardize data
    scaler = MinMaxScaler()
    x = scaler.fit_transform(data_frame)
    pca = PCA()
    # Alternatively, choose n_components to a user defined dimensionality, e.g:
    # pca = PCA(n_components=3)
    components = pca.fit_transform(x)
    pc_df = pd.DataFrame(data = components, columns = [f"principal component {x}" for x in range(0, pca.n_components_)])
    print(pc_df)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    print(sum(pca.explained_variance_ratio_))
    return (pca, pc_pf, scaler)

# Performs PCA on all bins, collects transformations and dataframes.
def analyze_bins(data_frames):
    pca_results = []
    for i in range(0, len(data_frames)):
        pca_results.append(pca_decomposition(data_frames[i]))
    return results

# Euclidean distance computation w/ respect to the transformed feature vector
#   space for each bin, smallest distance wins.
def query_all_bins(bins, query):
    distances = []
    for i in range(0, len(bins)):
        # Retrieve bin components, scaled frame and scales.
        pca = bins[i][0]
        pc_df = bins[i][1]
        scaler = bins[i][2]

        # Scale the query according to the min maxes within the current bin (unscaled training data).
        scaled_query = scaler.transform(query)

        # transorm the query to the shape of the binned PCA
        transformed_scaled_query = pca.transform(scaled_query)

        pc_means = pc_df.mean(axis=0)
        distance_frame = transformed_scaled_query.sub(pc_means).abs()
        squared_distance = distance_frame.dot(distance_frame)
        distances.append(sqrt(squared_distance))
    
    smallest = float("inf")
    bin_id = 0
    for i in range(0, len(distances)):
        if distances[i] < smallest:
            smallest = distances[i]
            bin_id = i
    
    return bin_id




        

        
df = pd.read_csv(filepath_or_buffer="dataframe.csv") 
pca_decomposition(df)


#print(dataframe)
#pca = pca_decomposition(standardize(dataframe))




# print("Dummy data for refference:")
# print(dummy_data)
# # Histogram computations
# # show_all_histograms(dummy_data)
# 
# 
# # Principal component analysis
# print("PCA analysis results:")
# pca = pca_decomposition(dummy_data)
# print(f"components: {pca.components_}")
# print(f"explained variance: {pca.explained_variance_}")
# print(f"explained variance ratio: {pca.explained_variance_ratio_}")
# print(f"singular values: {pca.singular_values_}")
