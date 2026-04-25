import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configuração do banco
engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

CIDADES_MONITORADAS = [
    {"id": 1, "nome": "Araruama", "lat": -22.87, "lon": -42.34},
    {"id": 2, "nome": "Cabo Frio", "lat": -22.88, "lon": -42.06},
    {"id": 3, "nome": "Arraial do Cabo", "lat": -22.96, "lon": -42.02},
    {"id": 4, "nome": "Armação dos Búzios", "lat": -22.74, "lon": -41.88},
    {"id": 5, "nome": "São Pedro da Aldeia", "lat": -22.84, "lon": -42.10},
    {"id": 6, "nome": "Iguaba Grande", "lat": -22.83, "lon": -42.22},
    {"id": 7, "nome": "Saquarema", "lat": -22.92, "lon": -42.48},
    {"id": 8, "nome": "Rio das Ostras", "lat": -22.52, "lon": -41.94},
]

def buscar_previsao(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
   
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant",
        "hourly": "relative_humidity_2m",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7
    }
    
    r = requests.get(url, params=params)
    res = r.json()
    daily = res.get("daily", {})
    hourly = res.get("hourly", {})
    
    previsoes_cidade = []
    
    for i in range(len(daily.get("time", []))):
        # Lógica para extrair a umidade média do dia (já que a API entrega por hora)
        start_idx = i * 24
        end_idx = start_idx + 24
        umidade_dia = hourly.get("relative_humidity_2m", [])[start_idx:end_idx]
        media_umidade = sum(umidade_dia) / len(umidade_dia) if umidade_dia else None

        previsoes_cidade.append({
            "data_previsao": daily["time"][i], # Data da previsão
            "id_condicao": daily["weathercode"][i], # Código WMO
            "temp_max": daily["temperature_2m_max"][i], #Temperatura Máxima
            "temp_min": daily["temperature_2m_min"][i], # Temperatura Mínima 
            "chuva_prob": daily["precipitation_probability_max"][i], # Probabilidade de chuva
            "vento_vel": daily["wind_speed_10m_max"][i], # Velocidade do vento
            "vento_dir": daily["wind_direction_10m_dominant"][i], # Direção do vento
            "umidade_rel": round(media_umidade, 2) if media_umidade else None, # Umidade média
            "data_coleta": datetime.now()
        })
    return previsoes_cidade

def main():
    lista_final = []
    for c in CIDADES_MONITORADAS:
        print(f"Coletando dados para: {c['nome']}...")
        dados = buscar_previsao(c['lat'], c['lon'])
        for item in dados:
            item["id_cidade"] = c["id"]
            lista_final.append(item)
    
    if lista_final:
        df = pd.DataFrame(lista_final)
        df.to_sql("previsao_clima", con=engine, if_exists="append", index=False)
        print("🚀 Previsão com vento e umidade atualizada")

if __name__ == "__main__":
    main()
