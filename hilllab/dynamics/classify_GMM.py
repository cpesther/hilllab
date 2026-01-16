# Christopher Esther, Hill Lab, 1/16/2026

from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

def classify_GMM(summary):

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
    gmm.fit(X_scaled)

    # Generate cluster labels
    cluster_labels = gmm.predict(X_scaled)  # array of cluster indices for each particle
    cluster_probs = gmm.predict_proba(X_scaled)

    summary['cluster'] = cluster_labels  # save cluster labels to data

    # Add cluster weights into data
    for i in range(n_clusters):
        summary[f'cluster_{i}_weight'] = cluster_probs[:, i]