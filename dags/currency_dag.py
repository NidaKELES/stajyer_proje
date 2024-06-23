from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import json
import MySQLdb
import requests

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'schedule_interval': '5 10 * * *',  # Her gün saat 10:00'da çalışacak
    'catchup': False,  # Önceki aralıkları işleme alma
}

def start():
    print("DAG started.")

def read_and_insert_currency_data():
    # Dosya yolu
    url = 'https://country.io/currency.json'
    response = requests.get(url)
    if response.status_code == 200:
        currency_data = json.loads(response.text)
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

    for code, currency_code in currency_data.items():
        #print(code)
        #print(code)
        cursor.execute(f"INSERT INTO currency (country_code, currency_code) VALUES ('{code}', '{currency_code}')")
    
    
    conn.commit()
    conn.close()

def end():
    print("DAG completed.")

with DAG('currency_dag', 
         default_args=default_args, 
         description='DAG to load currency data from JSON to MySQL', 
         schedule_interval='5 10 * * *',
         catchup=False) as dag:
    
    start_task = PythonOperator(
        task_id='start',
        python_callable=start
    )

    read_and_insert_task = PythonOperator(
        task_id='read_and_insert_currency_data',
        python_callable=read_and_insert_currency_data
    )

    end_task = PythonOperator(
        task_id='end',
        python_callable=end
    )

    start_task >> read_and_insert_task >> end_task
