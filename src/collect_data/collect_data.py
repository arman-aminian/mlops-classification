import psycopg2
import pandas as pd


def transfer_csv_to_postgresql(csv_path_list, selected_columns):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0"
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS POSTS")

    sql = '''CREATE TABLE POSTS(model int NOT NULL,\
    description varchar(1000),\
    price varchar(50);'''
    cur.execute(sql)

    cur.execute('''INSERT INTO POSTS(employee_id, employee_name, employee_email, employee_salary) VALUES ( 
    3, 'nnn', 'eee', 9000)''')

    for csv_path in csv_path_list:
        csv_file = pd.read_csv(csv_path)
        for i, row in csv_file.iterrows():


    conn.commit()
    conn.close()