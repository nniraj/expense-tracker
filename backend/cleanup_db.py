import psycopg2

conn = psycopg2.connect('postgresql://postgres:Vedant%40065@localhost/expense_tracker')
cursor = conn.cursor()

# Drop all tables with CASCADE to remove dependencies
tables = ['alembic_version', 'expense', 'expenses', 'category', 'categories', 'user', 'users']
for table in tables:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
        print(f"Dropped {table}")
    except Exception as e:
        print(f"Error dropping {table}: {e}")

conn.commit()
cursor.close()
conn.close()
print("Database cleanup complete")
