import os
from typing import Optional, List
from pathlib import Path
import pandas as pd


def create_sample_csv(output_path: str = "./data/sample_data.csv"):

    # Create sample sales data
    data = {
        "date": [
            "2024-01-15", "2024-01-22", "2024-02-03", "2024-02-14",
            "2024-03-01", "2024-03-15", "2024-04-02", "2024-04-18",
            "2024-05-05", "2024-05-20", "2024-06-01", "2024-06-15"
        ],
        "product": [
            "Laptop", "Smartphone", "Tablet", "Laptop",
            "Smartphone", "Headphones", "Laptop", "Tablet",
            "Smartphone", "Headphones", "Laptop", "Tablet"
        ],
        "category": [
            "Electronics", "Electronics", "Electronics", "Electronics",
            "Electronics", "Accessories", "Electronics", "Electronics",
            "Electronics", "Accessories", "Electronics", "Electronics"
        ],
        "quantity": [5, 12, 8, 3, 15, 25, 7, 10, 20, 30, 4, 6],
        "unit_price": [
            1200, 800, 500, 1200,
            800, 150, 1200, 500,
            800, 150, 1200, 500
        ],
        "region": [
            "North", "South", "East", "West",
            "North", "South", "East", "West",
            "North", "South", "East", "West"
        ],
        "salesperson": [
            "Alice", "Bob", "Charlie", "Diana",
            "Alice", "Bob", "Charlie", "Diana",
            "Alice", "Bob", "Charlie", "Diana"
        ]
    }
    
    df = pd.DataFrame(data)
    df["total_revenue"] = df["quantity"] * df["unit_price"]
    
    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✅ Sample CSV created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_sample_csv()