import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose

def preprocess_data(data):
    """
    Подготовка данных: проверка и заполнение пропусков, установка индекса.
    """
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data.sort_index(inplace=True)
    data['views'].fillna(method='ffill', inplace=True)  # Заполнение пропусков
    return data

def seasonal_decomposition(data, period=30):
    """
    Выполняет сезонную декомпозицию временного ряда.
    """
    decomposition = seasonal_decompose(data['views'], model='multiplicative', period=period)
    return {
        "trend": decomposition.trend.dropna().tolist(),
        "seasonal": decomposition.seasonal.dropna().tolist(),
        "residual": decomposition.resid.dropna().tolist(),
        "dates": decomposition.trend.dropna().index.strftime('%Y-%m-%d').tolist()
    }

def forecast_with_sarimax(data, steps=30, order=(2, 1, 1), seasonal_order=(2, 1, 1, 12)):
    """
    Строит прогноз с использованием модели SARIMAX.
    """
    # Настройка модели
    model = SARIMAX(data['views'], order=order, seasonal_order=seasonal_order)
    results = model.fit(disp=False)

    # Прогнозирование
    forecast = results.get_forecast(steps=steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=steps + 1, freq='D')[1:]
    forecast_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()

    return {
        "forecast_dates": forecast_index.strftime('%Y-%m-%d').tolist(),
        "forecast_values": forecast_mean.tolist(),
        "lower_bounds": conf_int.iloc[:, 0].tolist(),
        "upper_bounds": conf_int.iloc[:, 1].tolist()
    }

def analyze_data(data, steps=30):
    """
    Выполняет полный анализ данных: декомпозицию и прогнозирование.
    """
    processed_data = preprocess_data(data)

    # Сезонная декомпозиция
    decomposition = seasonal_decomposition(processed_data)

    # Прогнозирование
    forecast = forecast_with_sarimax(processed_data, steps=steps)

    return {
        "decomposition": decomposition,
        "forecast": forecast
    }