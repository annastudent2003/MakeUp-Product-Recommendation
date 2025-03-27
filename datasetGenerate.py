import pandas as pd
import numpy as np

# Generate Synthetic Dataset
np.random.seed(42)
num_rows = 1000

brands = ['Maybelline', "L'Oreal", 'MAC', 'Clinique', 'Sephora', 'Revlon', 'Estee Lauder', 'Dior', 'Lancome', 'NARS']
categories = ['Makeup', 'Skincare']
product_types = ['Foundation', 'Concealer', 'Face Powder', 'Sunscreen', 'Body Lotion', 'Face Cream']
skin_types = ['Normal', 'Dry', 'Oily']
sensitivities = ['Yes', 'No']

# Create the dataset
data = {
    'brand': np.random.choice(brands, num_rows),
    'category': np.random.choice(categories, num_rows),
    'product_type': np.random.choice(product_types, num_rows),
    'skin_type': np.random.choice(skin_types, num_rows),
    'sensitivity': np.random.choice(sensitivities, num_rows),
    'rating': np.round(np.random.uniform(1, 5, num_rows), 1),
    'price': np.round(np.random.uniform(5, 100, num_rows), 2)
}

# Create DataFrame
df = pd.DataFrame(data)

# Add 'product' column to specify unique product names with SPF for sunscreen
def generate_product(row):
    edition = np.random.choice(['A', 'B', 'C', 'D', 'E']) + str(np.random.randint(1, 10))
    if row['product_type'] == 'Sunscreen':
        spf = np.random.choice([15, 30, 50, 70, 100])
        return f"{row['brand']} {row['product_type']} SPF{spf} Edition {edition}"
    return f"{row['brand']} {row['product_type']} Edition {edition}"

df['product'] = df.apply(generate_product, axis=1)

# Save to CSV
df.to_csv('./model/synthetic_product_dataset.csv', index=False)

print("Synthetic dataset created with", num_rows, "rows.")
