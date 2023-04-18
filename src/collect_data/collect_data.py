import psycopg2
import pandas as pd


def transfer_csv_to_postgresql(csv_path_list):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0"
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS POSTS")

    sql = '''CREATE TABLE POSTS(model varchar(100),\
    description varchar(1000),\
    price varchar(50),\
    size int,\
    category varchar(50));'''
    cur.execute(sql)

    for csv_path in csv_path_list:
        csv_file = pd.read_csv(csv_path)
        for i, row in csv_file.iterrows():
            desc = row['description'][:1000]
            cur.execute(
                'INSERT INTO POSTS (model, description, price, size, category) VALUES (%s, %s, %s, %s, %s)',
                (row['year'], desc, row['price'], row['size'], csv_path.split('/')[-1], )
            )

    conn.commit()
    conn.close()
