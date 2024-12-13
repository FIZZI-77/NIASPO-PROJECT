from flask import Flask, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine
from analysis import analyze_data  # Здесь импортируем ваш анализатор данных

app = Flask(__name__,
            template_folder='../front/templates',  # Указание пути к папке с шаблонами
            static_folder='../front/static')

# Укажите правильные параметры подключения
DB_URL = "postgresql://username:password@localhost:5432/thecleverprogrammer"
engine = create_engine(DB_URL)

@app.route('/')
def index():
    # Получаем данные для отображения в графиках
    with engine.connect() as connection:
        query = "SELECT date, views FROM traffic_data ORDER BY date;"
        data = pd.read_sql_query(query, connection)

        # Анализируем данные: сезонная декомпозиция и прогноз
        analysis_result = analyze_data(data)

    # Передаем анализированные данные в шаблон
    return render_template('index.html', analysis_result=analysis_result)

@app.route('/analyze', methods=['GET'])
def analyze():
    with engine.connect() as connection:
        query = "SELECT date, views FROM traffic_data ORDER BY date;"
        data = pd.read_sql_query(query, connection)

        # Анализируем данные
        analysis_result = analyze_data(data)

        return jsonify(analysis_result)


if __name__ == '__main__':
    app.run(debug=True)