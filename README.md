# Data Analytics SQL Practice GUI

A modern desktop application built with Python and CustomTkinter to help you practice and improve your SQL data analysis skills. This application provides 40 curated SQL challenges ranging from Easy to Very Hard, strictly based on a comprehensive mock company database schema.

## Features

- **40 Curated SQL Challenges**: Test your skills with 4 levels of difficulty:
  - **Easy**: Basic `SELECT`, `WHERE`, `ORDER BY`.
  - **Medium**: Aggregations (`GROUP BY`, `SUM`, `COUNT`) and basic `JOIN`s.
  - **Hard**: Multiple `JOIN`s, `LEFT JOIN`, Date functions, and Subqueries.
  - **Very Hard**: Window Functions (`RANK`, `ROW_NUMBER`, `LAG`, `LEAD`, *Running Total*) and CTEs.
- **Bento UI Dashboard**: Modern, clean, and responsive grid layout with persistent progress tracking (✅ Solved / ❌ Unsolved).
- **Interactive Practice Page**:
  - Displays the Database ERD for easy reference.
  - Text editor to input JSON results directly copied from Supabase.
  - Built-in JSON Validator that compares your result against the highly precise Expected Output.
  - Displays Expected Output in a clear ASCII Table format.

## System Requirements

- **Python**: Version 3.8 or higher.
- **Supabase**: A Supabase project (or any local PostgreSQL database) initialized with the provided `query.txt` file.

## Setup & Installation

1. **Initialize the Database**:
   - Copy the contents of `../query.txt` (or the equivalent SQL generation script).
   - Paste and execute it in your Supabase SQL Editor. This will create 15 interconnected tables (HR, Sales, Inventory, Finance) and insert thousands of mock records.

2. **Install Python Dependencies**:
   Navigate to this repository folder and install the required GUI libraries:
   ```powershell
   pip install customtkinter pillow
   ```

3. **Setup Progress Tracking (Optional)**:
   The application tracks your solved questions locally in a `progress.json` file (ignored by Git). If you are setting this up for the first time, the application will automatically create it for you upon your first correct answer. 
   Alternatively, you can manually create `progress.json` in the root folder with the following format:
   ```json
   {
       "solved_ids": [1, 2, 3]
   }
   ```

## How to Use

1. Launch the application:
   ```powershell
   python app.py
   ```
2. The **Dashboard** will open. Click on any challenge card to begin.
3. Read the instructions carefully. Note any specific column names (*aliases*) required by the prompt.
4. Go to your Supabase SQL Editor, write your SQL query, and run it.
5. Click the **Copy as JSON** button on the Supabase results table.
6. Paste the JSON into the Text Area in the GUI app.
7. Click **Check Answer**. The system will validate your logic and data structure.

## Database Schema (ERD)

The database simulates a complete retail/e-commerce enterprise:
- **HR**: `departments`, `employees`, `job_titles`, `employee_salaries`
- **Sales**: `customers`, `customer_addresses`, `orders`, `order_items`, `shipping_methods`
- **Inventory**: `products`, `product_categories`, `suppliers`
- **Finance & CS**: `invoices`, `payments`, `reviews`

*An ERD image (`erd.png`) is provided locally and displayed inside the application for your convenience.*
