from src.collect_data.collect_data import transfer_csv_to_postgresql
import os
import psycopg2


def data_unification(csv_path_list, file_directory):
    transfer_csv_to_postgresql(csv_path_list=csv_path_list)

    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0"
    )
    cur = conn.cursor()

    sql = "COPY (SELECT * FROM POSTS) TO STDOUT WITH CSV DELIMITER ';'"
    with open(os.path.join(file_directory, 'posts.csv'), "w") as file:
        cur.copy_expert(sql, file)
