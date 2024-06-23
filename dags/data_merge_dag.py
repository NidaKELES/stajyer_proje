from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import MySQLdb

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'schedule_interval': '15 10 * * *',  # Her gün saat 10:15'te çalışacak
    'catchup': False,  # Önceki aralıkları işleme alma
}

def start():
    print("DAG started.")

def merge_data():
    # MySQL bağlantısı
    conn = MySQLdb.connect(host='mysql',
                           port=3306,
                           user='kartaca',
                           passwd='kartaca',
                           db='kartaca')
    cursor = conn.cursor()

    # country ve currency tablolarını birleştirip data_merge tablosuna ekle
    merge_query = """
    INSERT INTO data_merge (country_name, currency_code)
    SELECT c.country_name, cu.currency_code
    FROM country c
    JOIN currency cu ON c.country_code = cu.country_code
    """
    cursor.execute(merge_query)
    conn.commit()
    conn.close()

def end():
    print("DAG completed.")

with DAG('data_merge_dag', 
         default_args=default_args, 
         description='DAG to merge country and currency data and insert into data_merge table', 
         schedule_interval='15 10 * * *',
         catchup=False) as dag:
    
    start_task = PythonOperator(
        task_id='start',
        python_callable=start
    )

    merge_task = PythonOperator(
        task_id='merge_data',
        python_callable=merge_data
    )

    end_task = PythonOperator(
        task_id='end',
        python_callable=end
    )

    start_task >> merge_task >> end_task
