import sqlite3
import csv
import os

def export_table_to_csv(db_path, table_name, csv_path=None):
       
    # Set default CSV path if not provided
    if csv_path is None:
        csv_path = f"{table_name}.csv"
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        
        if not cursor.fetchone():
            print(f"Error: Table '{table_name}' not found in database")
            return False
        
        # Get all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Write to CSV file
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(column_names)
            
            # Write data rows
            writer.writerows(data)
        
        print(f"Successfully exported {len(data)} rows from '{table_name}' to '{csv_path}'")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except IOError as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Main execution
if __name__ == "__main__":
    db_file = "inventory.db"
    table_name = "vendor_sales_summary"
    output_file = "vendor_sales_summary.csv"
    
    # Check if database file exists
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' not found")
    else:
        export_table_to_csv(db_file, table_name, output_file)