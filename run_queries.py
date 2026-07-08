import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

def df_to_markdown(df, include_index=False):
    if include_index:
        df = df.reset_index()
    headers = list(df.columns)
    markdown = "| " + " | ".join(map(str, headers)) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for _, row in df.iterrows():
        # Clean values to avoid issues in markdown tables
        cleaned_vals = []
        for val in row.values:
            val_str = str(val).replace('\n', ' ').replace('|', '\\|')
            cleaned_vals.append(val_str)
        markdown += "| " + " | ".join(cleaned_vals) + " |\n"
    return markdown

def run_queries_and_eda():
    db_path = r"C:\Users\rkvig\Downloads\Joshi\task2_eda\retail.db"
    sql_file_path = r"C:\Users\rkvig\Downloads\Joshi\task2_eda\queries.sql"
    output_report_path = r"C:\Users\rkvig\Downloads\Joshi\task2_eda\eda_report.md"
    artifact_img_dir = r"C:\Users\rkvig\Downloads\Joshi\task2_eda\artifact_images\.gemini\antigravity\brain\fa836e50-85bb-4edf-afb3-7208fd016c50\images"
    local_img_dir = r"C:\Users\rkvig\Downloads\Joshi\task2_eda\images"
    
    # Ensure directories exist
    os.makedirs(artifact_img_dir, exist_ok=True)
    os.makedirs(local_img_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    print("Reading SQL queries file...")
    with open(sql_file_path, "r") as f:
        sql_content = f.read()
        
    # Split queries by semicolon (ignoring comments)
    queries = []
    current_query = []
    for line in sql_content.split('\n'):
        if line.strip().startswith('--') or not line.strip():
            continue
        current_query.append(line)
        if ';' in line:
            queries.append('\n'.join(current_query))
            current_query = []
            
    print(f"Parsed {len(queries)} queries.")
    
    # Run SQL Queries and collect tables
    query_results = []
    titles = [
        "Q1: Top 5 Products by Revenue in the Last 6 Months",
        "Q2: Monthly Sales and Active Customer Trends",
        "Q3: Top 5 Countries by Revenue (Excluding UK)",
        "Q4: Average Order Value (AOV) by Country (Top 10)",
        "Q5: Customer Retention - Repeat vs One-Time Buyers",
        "Q6: Hour of the Day Transaction Density and Revenue"
    ]
    
    for idx, q in enumerate(queries):
        print(f"Running Query {idx+1}...")
        df_res = pd.read_sql_query(q, conn)
        query_results.append(df_res)
        
    print("Generating EDA Visualizations...")
    # Visual 1: Monthly Sales Trend (Q2)
    df_q2 = query_results[1]
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")
    sns.lineplot(data=df_q2, x="Month", y="MonthlyRevenue", marker="o", color="#2A9D8F", linewidth=2.5)
    plt.title("Monthly Revenue Trend (Dec 2010 - Dec 2011)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Revenue (£)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    v1_path = os.path.join(artifact_img_dir, "monthly_revenue_trend.png")
    plt.savefig(v1_path, dpi=150)
    plt.savefig(os.path.join(local_img_dir, "monthly_revenue_trend.png"), dpi=150)
    plt.close()
    
    # Visual 2: Top Countries by Revenue (Q3)
    df_q3 = query_results[2]
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_q3, x="Country", y="TotalRevenue", hue="Country", palette="viridis", legend=False)
    plt.title("Top 5 International Countries by Revenue", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Country", fontsize=12)
    plt.ylabel("Revenue (£)", fontsize=12)
    plt.tight_layout()
    v2_path = os.path.join(artifact_img_dir, "top_countries_revenue.png")
    plt.savefig(v2_path, dpi=150)
    plt.savefig(os.path.join(local_img_dir, "top_countries_revenue.png"), dpi=150)
    plt.close()
    
    # Visual 3: Hourly Order Density (Q6)
    df_q6 = query_results[5]
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_q6, x="HourOfDay", y="OrderCount", hue="HourOfDay", palette="Blues_d", legend=False)
    plt.title("Hourly Transaction Density (Order Volume)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Number of Orders", fontsize=12)
    plt.tight_layout()
    v3_path = os.path.join(artifact_img_dir, "hourly_order_density.png")
    plt.savefig(v3_path, dpi=150)
    plt.savefig(os.path.join(local_img_dir, "hourly_order_density.png"), dpi=150)
    plt.close()

    print("Generating Descriptive Statistics...")
    # Load sample/subset to get description stats and correlation matrix
    df_full = pd.read_sql_query("SELECT Quantity, UnitPrice, LineTotal, IsCancelled FROM transactions", conn)
    desc_stats = df_to_markdown(df_full.describe(), include_index=True)
    corr_df = df_full[['Quantity', 'UnitPrice', 'LineTotal', 'IsCancelled']].corr()
    corr_matrix = df_to_markdown(corr_df, include_index=True)
    
    # Generate Heatmap (Multivariate Analysis)
    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".3f", linewidths=0.5)
    plt.title("Correlation Matrix Heatmap", fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    v4_path = os.path.join(artifact_img_dir, "correlation_heatmap.png")
    plt.savefig(v4_path, dpi=150)
    plt.savefig(os.path.join(local_img_dir, "correlation_heatmap.png"), dpi=150)
    plt.close()
    
    print("Writing EDA report...")
    with open(output_report_path, "w") as f:
        f.write("# Exploratory Data Analysis & Business Intelligence Report\n\n")
        f.write("This report presents descriptive statistics, univariate analysis, and solutions to key business questions using SQL and visualizations.\n\n")
        
        f.write("## 1. Descriptive Statistics & Univariate Analysis\n\n")
        f.write("### Numerical Summary Statistics\n\n")
        f.write(desc_stats + "\n\n")
        f.write("### Correlation Matrix\n\n")
        f.write(corr_matrix + "\n\n")
        f.write("#### Correlation Heatmap (Multivariate):\n\n")
        f.write("![Correlation Matrix Heatmap](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/correlation_heatmap.png)\n\n")
        f.write("> [!NOTE]\n")
        f.write("> There is a negative correlation between `IsCancelled` and `Quantity`/`LineTotal` as cancellations contain negative values.\n\n")
        
        f.write("## 2. SQL Business Questions and Results\n\n")
        
        for idx, df_res in enumerate(query_results):
            f.write(f"### {titles[idx]}\n\n")
            f.write("#### SQL Query:\n")
            f.write("```sql\n" + queries[idx].strip() + "\n```\n\n")
            f.write("#### Results Table:\n\n")
            f.write(df_to_markdown(df_res) + "\n\n")
            
            # Embed corresponding visualizations
            if idx == 1:
                f.write("#### Visualization:\n\n")
                f.write("![Monthly Revenue Trend](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/monthly_revenue_trend.png)\n\n")
            elif idx == 2:
                f.write("#### Visualization:\n\n")
                f.write("![Top Countries Revenue](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/top_countries_revenue.png)\n\n")
            elif idx == 5:
                f.write("#### Visualization:\n\n")
                f.write("![Hourly Order Density](C:/Users/HP/.gemini/antigravity/brain/fa836e50-85bb-4edf-afb3-7208fd016c50/images/hourly_order_density.png)\n\n")
            
            f.write("---\n\n")
            
    conn.close()
    print(f"EDA report successfully saved to {output_report_path}")

if __name__ == "__main__":
    run_queries_and_eda()