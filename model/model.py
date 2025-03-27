import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the dataset
dataset_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dataset_dir, "cleaned_product_dataset.csv")
df = pd.read_csv(file_path)

# The dataset is already label-encoded
numerical_cols = ["rating", "price"]

# Standardize numerical features
scaler = StandardScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Apply KMeans clustering with optimized clusters
optimal_clusters = 5  # Could be tuned using the elbow method or silhouette score
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(df[numerical_cols + ["category", "sensitivity", "skin_type"]])

# Save the clustered dataset
output_file_path = os.path.join(dataset_dir, "clustered_product_dataset.csv")
df.to_csv(output_file_path, index=False)

# Apply PCA for visualization
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df[numerical_cols])
df["pca1"], df["pca2"] = df_pca[:, 0], df_pca[:, 1]

# Function to recommend products based on user input
def recommend_products(category, price_range, sensitivity, skin_type, df):
    # Ensure input values are within the dataset range
    if category not in df["category"].values:
        raise ValueError(f"Category {category} is not in the dataset.")
    if sensitivity not in df["sensitivity"].values:
        raise ValueError(f"Sensitivity {sensitivity} is not in the dataset.")
    if skin_type not in df["skin_type"].values:
        raise ValueError(f"Skin type {skin_type} is not in the dataset.")
    
    # Filter based on input
    filtered_df = df[(df["category"] == category) &
                     (df["sensitivity"] == sensitivity) &
                     (df["skin_type"] == skin_type) &
                     (df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]
    
    return filtered_df.head(5)  # Return top 5 recommendations

# Example usage
user_category = 0  # Replace with actual integer value
user_price_range = (-1, 1)  # Standardized price range
user_sensitivity = 1  # Replace with actual integer value
user_skin_type = 0  # Replace with actual integer value

recommended_products = recommend_products(user_category, user_price_range, user_sensitivity, user_skin_type, df)
print(recommended_products)

# Plot clustering results using PCA
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["pca1"], y=df["pca2"], hue=df["cluster"], palette="viridis", alpha=0.7)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("K-Means Clustering of Products (PCA Reduced)")
plt.legend(title="Cluster")
plt.show()
