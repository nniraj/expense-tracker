import psycopg2

conn = psycopg2.connect('postgresql://postgres:Vedant%40065@localhost/expense_tracker')
cursor = conn.cursor()
cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'  - {table[0]}')
cursor.close()
conn.close()
