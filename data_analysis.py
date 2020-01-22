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

def pca_decomposition(data_frame):
    #Standardize data
    x = MinMaxScaler().fit_transform(data_frame)
    pca = PCA()
    # Alternatively, choose n_components to a user defined dimensionality, e.g:
    # pca = PCA(n_components=3)
    components = pca.fit_transform(x)
    pc_df = pd.DataFrame(data = components, columns = [f"principal component {str(x)}" for x in range(0, pca.n_components_)])
    print(pc_df)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    print(sum(pca.explained_variance_ratio_))


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
