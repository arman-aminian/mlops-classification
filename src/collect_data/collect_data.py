import psycopg2
import pandas as pd


def transfer_csv_to_postgresql(csv_path_list, selected_columns=None):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0"
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS POSTS")

    sql = '''CREATE TABLE POSTS(model int,\
    description varchar(1000),\
    price varchar(50);'''
    cur.execute(sql)

    for csv_path in csv_path_list:
        csv_file = pd.read_csv(csv_path)
        for i, row in csv_file.iterrows():
            cur.execute(f'''INSERT INTO POSTS(model, description, price) VALUES ( 
            {row['Model']}, {row['Description']}, {row['Price']})''')

    conn.commit()
    conn.close()
