import psycopg2


def transfer_csv_to_postgresql(csv_list, selected_columns):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0"
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS POSTS")

    sql = '''CREATE TABLE POSTS(employee_id int NOT NULL,\
    employee_name char(20),\
    employee_email varchar(30), employee_salary float);'''
    cur.execute(sql)

    cur.execute('''INSERT INTO POSTS(employee_id, employee_name, employee_email, employee_salary) VALUES ( 
    3, 'nnn', 'eee', 9000)''')

    conn.commit()
    conn.close()