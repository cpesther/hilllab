# Christopher Esther, Hill Lab, 1/16/2026
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
import pandas as pd

def classify_GMM(summary, identifier=None):

    """
    Classifies beads into three clusters (stuck, oscillating, and
    transiting as 0, 1, and 2, respectively) when provided the summary
    data from the primary_analysis function.

    ARGUMENTS:
        summary_data (pandas.DataFrame): the summary data as calcualted
            by the primary_analysis function.
    """

    # Select the features
    n_clusters = 3
    features = ['displacement', 'straightness', 'circular_variance', 'bb_area', 'mean_speed', 'mean_acceleration']
    X = summary[features].dropna().to_numpy()  # shape (n_particles, n_features)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit GMM
    gmm = GaussianMixture(n_components=n_clusters, covariance_type='full', random_state=42)
    gmm.fit(X_scaled)  # or X if not scaling

    # Generate cluster labels
    cluster_labels = gmm.predict(X_scaled)  # array of cluster indices for each particle
    cluster_probs = gmm.predict_proba(X_scaled)

    # Convert these numerical labels to sensible strings
    cluster_strings = {
        0: 'stuck',
        1: 'oscillating',
        2: 'transiting'
    }
    cluster_label_strings = [cluster_strings[label] for label in cluster_labels]

    # Save cluster labels to data
    summary['cluster'] = cluster_label_strings

    # Save cluster weights as well
    for cluster_number in list(cluster_strings.keys()):
        summary[f'{cluster_strings[cluster_number]}_cluster_weight'] = cluster_probs[:, cluster_number]

    # If provided with an identifier column, we can create a pivot table with this value
    if identifier is not None:
        cluster_pivot = pd.pivot_table(
            summary,
            index='cluster',       # rows
            columns=identifier,    # columns
            aggfunc='size',        # counts number of occurrences
            fill_value=0           # replace NaN with 0
        )

        return summary, cluster_pivot
    
    else:
        return summary, None
