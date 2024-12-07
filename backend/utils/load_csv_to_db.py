import pandas as pd
from sqlalchemy import create_engine

# Настройки подключения к базе данных
DB_URL = "postgresql+psycopg2://postgres:zaprudno1@localhost:5432/mydatabase"

def load_csv_to_db(file_path):
    try:
        # Загрузка данных из CSV
        data = pd.read_csv(file_path, parse_dates=['Date'])
        data.columns = ['date', 'views']  # Приведение к стандартным именам столбцов

        # Подключение к базе данных
        engine = create_engine(DB_URL)
        with engine.connect() as connection:
            # Загружаем данные в таблицу (данные будут добавляться, а не заменяться)
            data.to_sql('traffic_data', con=connection, if_exists='append', index=False)
            print("Данные загружены в базу данных.")
    except Exception as e:
        print(f"Произошла ошибка при загрузке данных: {e}")


# Пример вызова
if __name__ == "__main__":
    load_csv_to_db('data/Thecleverprogrammer.csv')
