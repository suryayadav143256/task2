import pandas as pd
import sqlite3
import os

def create_sqlite_db():
    csv_path = r"d:\Joshi\task1_wrangling\cleaned_retail.csv"
    db_dir = r"d:\Joshi\task2_eda"
    db_path = os.path.join(db_dir, "retail.db")
    
    # Ensure directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    print(f"Loading cleaned data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    print("Writing transactions table...")
    # Convert InvoiceDate back to string/text for SQLite compatibility if needed, 
    # but pd.to_sql handles datetimes fine as text.
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    
    # Verify table and row count
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"Successfully created table 'transactions' with {count:,} rows.")
    
    # Add an index on CustomerID, InvoiceNo, and InvoiceDate for faster queries
    print("Creating database indexes...")
    cursor.execute("CREATE INDEX idx_customer ON transactions(CustomerID)")
    cursor.execute("CREATE INDEX idx_invoice ON transactions(InvoiceNo)")
    cursor.execute("CREATE INDEX idx_date ON transactions(InvoiceDate)")
    conn.commit()
    
    conn.close()
    print("Database creation complete!")

if __name__ == "__main__":
    create_sqlite_db()