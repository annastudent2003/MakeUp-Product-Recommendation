import sys
import pandas as pd
import json
import os

# Construct file path dynamically
base_dir = os.path.dirname(os.path.abspath(__file__))
original_path = os.path.join(base_dir, "model", "synthetic_product_dataset.csv")
clustered_path = os.path.join(base_dir, "model", "clustered_product_dataset.csv")

# Load datasets
original_df = pd.read_csv(original_path)
clustered_df = pd.read_csv(clustered_path)

# Create mapping from original dataset
product_type_map = dict(zip(original_df.index, original_df["product_type"]))
product_type_map = {idx: prod for idx, prod in enumerate(original_df["product_type"].unique())}
skin_type_map = {idx: skin for idx, skin in enumerate(original_df["skin_type"].unique())}
sensitivity_map = {idx: sens for idx, sens in enumerate(original_df["sensitivity"].unique())}

# Convert numeric values in clustered dataset back to original text values
clustered_df["product_type"] = clustered_df["product_type"].map(product_type_map)
clustered_df["skin_type"] = clustered_df["skin_type"].map(skin_type_map)
clustered_df["sensitivity"] = clustered_df["sensitivity"].map(sensitivity_map)

# Debug: Check if mapping is working
print(f"[DEBUG] Mapped Clustered Data Sample:\n{clustered_df.head()}", file=sys.stderr)
print(f"[DEBUG] Unique Product Types After Mapping: {clustered_df['product_type'].unique()}", file=sys.stderr)

# Merge clustered data with original dataset to get product names
merged_data = clustered_df.merge(
    original_df[["product_type", "product", "price", "sensitivity", "skin_type"]], 
    on=["product_type"],  
    how="left"
)

# Rename columns to remove "_y" if merging added them
merged_data.rename(columns={"sensitivity_y": "sensitivity", "skin_type_y": "skin_type", "price_y": "price"}, inplace=True)

# Debug: Check if merging worked
print(f"[DEBUG] Merged Data Sample:\n{merged_data.head()}", file=sys.stderr)

# Function to get product recommendations
def get_recommendations(product_type, min_price, max_price, sensitivity, skin_type):
    # Convert inputs to string for proper filtering
    min_price = float(min_price)
    max_price = float(max_price)

    # Debug: Print unique dataset values before filtering
    print(f"[DEBUG] Unique Categories in Data: {merged_data['product_type'].unique()}", file=sys.stderr)
    print(f"[DEBUG] Unique Sensitivities in Data: {merged_data['sensitivity'].unique()}", file=sys.stderr)
    print(f"[DEBUG] Unique Skin Types in Data: {merged_data['skin_type'].unique()}", file=sys.stderr)
    print(f"[DEBUG] Unique Prices in Data: {merged_data['price'].describe()}", file=sys.stderr)

    # Debugging: Print filtering conditions
    print(f"[DEBUG] Filtering with: product_type={product_type}, min_price={min_price}, max_price={max_price}, sensitivity={sensitivity}, skin_type={skin_type}", file=sys.stderr)
    
    # Filter products based on given parameters
    filtered_products = merged_data[
        (merged_data["product_type"] == product_type) & 
        (merged_data["price"] >= min_price) & 
        (merged_data["price"] <= max_price) & 
        (merged_data["sensitivity"] == sensitivity) & 
        (merged_data["skin_type"] == skin_type)
    ]

    # Debugging: Print sample of filtered products before checking if empty
    print(f"[DEBUG] Filtered Products Sample:\n{filtered_products}", file=sys.stderr)

    if filtered_products.empty:
        print("[WARN] No products found.", file=sys.stderr)
        return json.dumps([])  # Empty JSON array

    # Select the top 3 unique products based on highest price
    top_products = filtered_products.drop_duplicates(subset="product").nlargest(3, "price")

    # Convert to JSON format with correct product name and price
    result = top_products[["product", "price"]].dropna().to_dict(orient="records")
    return json.dumps(result)

# Read JSON input from command-line argument
if len(sys.argv) != 2:
    print("[ERROR] Expected a JSON string as a single command-line argument.", file=sys.stderr)
    sys.exit(1)

try:
    print(f"[DEBUG] Raw sys.argv[1]: {sys.argv[1]}", file=sys.stderr)
    input_data = json.loads(sys.argv[1])  # Read JSON from argument
    product_type = input_data["product_type"]
    sensitivity = input_data["sensitivity"]
    skin_type = input_data["skinType"]
    min_price = float(input_data["priceRange"][0])
    max_price = float(input_data["priceRange"][1])

except (KeyError, ValueError, json.JSONDecodeError) as e:
    print(f"[ERROR] Invalid input data: {e}", file=sys.stderr)
    sys.exit(1)

# Get recommendations
output = get_recommendations(product_type, min_price, max_price, sensitivity, skin_type)
print(output)  # Only valid JSON goes to stdout
print(f"[INFO] Final Recommendations: {output}", file=sys.stderr)
