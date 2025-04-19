# PricePulse
An automated engine that fix dynamic pricing based on sales

A Python-based pricing engine that dynamically adjusts product prices based on inventory and sales data, built for the Thrd Coding Challenge. PricePulse processes CSV inputs, applies smart pricing rules, and outputs updated prices, optimized for Google Colab.

## Features

- Reads `products.csv` (product details) and `sales.csv` (sales data).
- Adjusts prices based on stock levels and demand.
- Ensures a minimum 20% profit margin.
- Outputs `updated_prices.csv` with SKU, old price, and new price (USD).
- Supports file upload/download in Google Colab.

## Pricing Rules

1. **Low Stock, High Demand**: Stock < 20 and sales > 30 → Increase price by 15%.
2. **Dead Stock**: Stock > 200 and sales = 0 → Decrease price by 30%.
3. **Overstocked**: Stock > 100 and sales < 20 → Decrease price by 10%.
4. **Minimum Profit**: New price ≥ cost_price * 1.2.
5. **Rounding**: Final price rounded to 2 decimal places.

## Setup

- **Requirements**: Python 3.6+, `pandas`, Google Colab (recommended).
- **Input Files**:
  - `products.csv`: `sku,name,current_price,cost_price,stock`
  - `sales.csv`: `sku,quantity_sold`

**Example Inputs**:

```
products.csv:
sku,name,current_price,cost_price,stock
A123,Item A,649.99,500.00,150
B456,Item B,699.00,550.00,15
C789,Item C,999.00,500.00,250

sales.csv:
sku,quantity_sold
A123,10
B456,35
C789,0
```
---
```
updated_prices.csv:
sku,old_price (USD),new_price (USD)
A123,649.99,600.00
B456,699.0,803.85
C789,999.0,699.3
```

## Files

- `pricing_engine_colab.py`: Core script with pricing logic.
- `updated_prices.csv`: Output with updated prices.

## Notes

- Ensure CSVs match the specified format.
- For local use, remove Colab-specific file handling.
- Built by Ansar Afsar for the Thrd Coding Challenge.
