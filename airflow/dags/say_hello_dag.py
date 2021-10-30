from datetime import timedelta

from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from airflow import DAG
from scripts.hello import Hello

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'say_hello_dag',
    default_args=default_args,
    description='Say Hello DAG',
    schedule_interval=timedelta(days=1),
)

runner1 = PythonOperator(
    task_id='say_hello',
    provide_context=True,
    python_callable=Hello.say_hello,
    op_kwargs={'prefix': 'microbo-step-1'},
    dag=dag,
)

runner2 = PythonOperator(
    task_id='say_hello',
    provide_context=True,
    python_callable=Hello.say_hello,
    op_kwargs={'prefix': 'microbo-stpe-2'},
    dag=dag,
)

runner3 = PythonOperator(
    task_id='say_hello',
    provide_context=True,
    python_callable=Hello.say_hello,
    op_kwargs={'prefix': 'microbo-step-3'},
    dag=dag,
)


runner1 >> runner2 >> runner3