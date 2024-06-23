from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import json
import MySQLdb
import requests

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'schedule_interval': '0 10 * * *',  # Her gün saat 10:00'da çalışacak
    'catchup': False,  # Önceki aralıkları işleme alma
}

def start():
    print("DAG started.")

def read_and_insert_country_data():
    # Dosya yolu
    url = 'https://country.io/names.json'
    response = requests.get(url)
    if response.status_code == 200:
        country_data = json.loads(response.text)
    else:
        print("Veri alınamadı:", response.status_code)
        exit()

    
    # MySQL bağlantısı
    conn = MySQLdb.connect(host='mysql', 
                           port=3306, 
                           user='kartaca', 
                           passwd='kartaca', 
                           db='kartaca')
    cursor = conn.cursor()

    # JSON dosyasını oku ve MySQL tablosuna ekle

    for code, name in country_data.items():
        #print(code)
        #print(name)
        cursor.execute(f"INSERT INTO country (country_code, country_name) VALUES ('{code}', '{name}')")
    
    
    conn.commit()
    conn.close()

def end():
    print("DAG completed.")

with DAG('country_dag', 
         default_args=default_args, 
         description='DAG to load country data from JSON to MySQL', 
         schedule_interval='0 10 * * *',
         catchup=False) as dag:
    
    start_task = PythonOperator(
        task_id='start',
        python_callable=start
    )

    read_and_insert_task = PythonOperator(
        task_id='read_and_insert_country_data',
        python_callable=read_and_insert_country_data
    )

    end_task = PythonOperator(
        task_id='end',
        python_callable=end
    )

    start_task >> read_and_insert_task >> end_task
