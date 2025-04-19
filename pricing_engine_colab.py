
import pandas as pd
from google.colab import files
import os

def apply_pricing_rules(products_df, sales_df):
    # Merge product and sales data on SKU
    merged_df = products_df.merge(sales_df, on='sku', how='left')
    # Fill NaN values in quantity_sold with 0 for products with no sales
    merged_df['quantity_sold'] = merged_df['quantity_sold'].fillna(0).astype(float)
    
    # Ensure numeric columns are floats
    merged_df['current_price'] = merged_df['current_price'].astype(float)
    merged_df['cost_price'] = merged_df['cost_price'].astype(float)
    merged_df['stock'] = merged_df['stock'].astype(float)
    
    # Initialize new_price column
    merged_df['new_price'] = merged_df['current_price']
    
    # Apply pricing rules
    for index, row in merged_df.iterrows():
        sku = row['sku']
        stock = row['stock']
        quantity_sold = row['quantity_sold']
        current_price = row['current_price']
        cost_price = row['cost_price']
        
        # Apply first applicable rule (1, 2, or 3)
        new_price = current_price
        rule_applied = "None"
        
        # Rule 1: Low Stock, High Demand
        if stock < 20 and quantity_sold > 30:
            new_price = current_price * 1.15
            rule_applied = "Rule 1 (Low Stock, High Demand)"
        # Rule 2: Dead Stock
        elif stock > 200 and quantity_sold == 0:
            new_price = current_price * 0.7
            rule_applied = "Rule 2 (Dead Stock)"
        # Rule 3: Overstocked Inventory
        elif stock > 100 and quantity_sold < 20:
            new_price = current_price * 0.9
            rule_applied = "Rule 3 (Overstocked Inventory)"
        
        # Rule 4: Minimum Profit Constraint
        min_price = cost_price * 1.2
        if new_price < min_price:
            new_price = min_price
        
        # Rule 5: Final Rounding
        new_price = round(new_price, 2)
        
        merged_df.at[index, 'new_price'] = new_price
    
    # Prepare output DataFrame
    output_df = merged_df[['sku', 'current_price', 'new_price']].copy()
    output_df.rename(columns={'current_price': 'old_price'}, inplace=True)
    
    return output_df

def main():
    print("Please upload products.csv and sales.csv")
    uploaded = files.upload()
    
    # Check if required files are uploaded
    if 'products.csv' not in uploaded or 'sales.csv' not in uploaded:
        print("Error: Please upload both products.csv and sales.csv")
        return
    
    # Read input CSV files
    try:
        products_df = pd.read_csv('products.csv')
        sales_df = pd.read_csv('sales.csv')
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return
    
    # Validate required columns
    required_product_cols = ['sku', 'name', 'current_price', 'cost_price', 'stock']
    required_sales_cols = ['sku', 'quantity_sold']
    if not all(col in products_df.columns for col in required_product_cols):
        print("Error: products.csv is missing required columns.")
        return
    if not all(col in sales_df.columns for col in required_sales_cols):
        print("Error: sales.csv is missing required columns.")
        return
    
    # Apply pricing rules
    output_df = apply_pricing_rules(products_df, sales_df)
    
    # Add units to column names
    output_df.columns = ['sku', 'old_price (USD)', 'new_price (USD)']
    
    # Save output to CSV
    output_df.to_csv('updated_prices.csv', index=False)
    print("Pricing engine completed. Output saved to updated_prices.csv")
    
    # Download the output CSV
    files.download('updated_prices.csv')

if __name__ == "__main__":
    main()
