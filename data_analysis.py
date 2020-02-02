import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer

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

    scaler = StandardScaler()
    x = scaler.fit_transform(imputer.fit_transform(data_frame))

    # Alternatively, choose n_components to a user defined dimensionality, e.g:
    #pca = PCA()
    pca = PCA(n_components=10)
    components = pca.fit_transform(x)
    pc_df = pd.DataFrame(data = components, columns = [f"principal component {x}" for x in range(0, pca.n_components_)])
    # print(pc_df)
    # print(pca.explained_variance_)
    # print(pca.explained_variance_ratio_)
    # print(sum(pca.explained_variance_ratio_))
    return (pca, pc_df, scaler)

# Performs PCA on all bins, collects transformations and dataframes.
def analyze_bins(data_frames):
    pca_results = []
    for i in range(0, len(data_frames)):
        pca_results.append(pca_decomposition(data_frames[i]))
    return pca_results

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

all_data = pd.read_csv(filepath_or_buffer="data/dataframe.csv") 
min_year = np.int32(all_data['year'].min())
max_year = np.int32(all_data['year'].max())
lowest_decade = min_year - (min_year % 10)
highest_decade = max_year - (max_year % 10)
n_decades = ((highest_decade - lowest_decade) // 10) + 1
bins = np.linspace(lowest_decade, highest_decade, n_decades, dtype=np.int32)

print(f"Came up with the following bins: {bins}")
print(f"Bins based on the following data:")
print(f"min_year: {min_year}")
print(f"max_year: {max_year}")
print(f"lowest_decade: {lowest_decade}")
print(f"highest_decade: {highest_decade}")
print(f"n_decades: {n_decades}")

# Initialize binned_data array of data frames, and array of np arrays that we'll use
#   to set the bins. It is pretty idiotic but it is the way.
binned_arrays = [[] for i in range(0, n_decades)]
binned_data = []

# remove string fields from all data.
all_data = all_data.drop(columns=['midi', 'midi_query', 'midi_unformatted'])

# Remove id fields because they are not really part of the feature vectors
all_data = all_data.drop(columns = ['id'])

# Remove match_score field as it is used for grabbing the feature vectors and midi's
all_data = all_data.drop(columns = ['match_score'])

# There seems to be another unamed id field, drop it.
all_data = all_data.loc[:, ~all_data.columns.str.contains('^Unnamed')]

# The data has rows that have missing values for specific features.
#   If we discard all problematic rows, we lose (1 - 451/2573) = 83% of our samples.
#   In an effort to reduce this problem, we use an Imputer to guesstimate values for the missing features based on
#   other samples.
imputer = SimpleImputer(strategy='mean')
imputer.fit_transform(all_data)

# NOTE: below you can see the alternative to imputing, which means remove all rows that have
# problematic values.
# Convert all inf values to NaN, then drop all rows that have a NaN column.
# all_data = all_data.replace([np.inf, -np.inf], np.nan)
# all_data = all_data.dropna()

for lower in bins:
    upper = lower + 10
    binned_data.append(all_data.loc[(np.int32(all_data['year']) >= lower) & (np.int32(all_data['year']) < upper)])

# Remove years
for i, bin in enumerate(binned_data):
    bin = bin.drop(columns = ['year'])
    print(f"bin {bins[i]} holds {len(bin)} songs.")

# For analyzation purposes, we want to cap the PCA analysis on 10 components.
#   Consequently, we discard a bin if it has < 10 samples to draw from,
#   which would cause the PCA to runtime crash.
binned_data = [bin for bin in binned_data if len(bin) >= 10]

# Analyze all bins. Analyzation consists of a list of 3 tuples with:
#   1. The PCA object
#   2. The bin expressed as dataframe in its principal components
#   3. The scaler object that was used to normalize the bin data.
binned_analyzation = analyze_bins(binned_data)

