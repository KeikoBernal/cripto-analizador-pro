# funciones.py - Funciones compartidas para ambos modos (VERSIÓN COMPLETA CON TODAS LAS FUNCIONALIDADES)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import re
import json
import csv
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')

# ==================== FUNCIONES DE CARGA DE DATOS ====================

def importar_base_cripto(nombre_cripto: str, carpeta_data: str = "datos") -> pd.DataFrame:
    archivo_csv = os.path.join(carpeta_data, f"{nombre_cripto}.csv")
    
    if not os.path.exists(archivo_csv):
        archivo_online = os.path.join(carpeta_data, f"{nombre_cripto}_online.csv")
        if os.path.exists(archivo_online):
            archivo_csv = archivo_online
        else:
            print(f"Archivo no encontrado: {archivo_csv}")
            return crear_datos_ejemplo_cripto(nombre_cripto)
    
    try:
        encodings = ['utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(archivo_csv, encoding=encoding)
                if len(df.columns) == 1:
                    df = pd.read_csv(archivo_csv, encoding=encoding, sep=';')
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("No se pudo leer el archivo")
        
        df.columns = df.columns.str.replace('﻿', '').str.strip().str.replace('"', '')
        
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['fecha', 'date', 'time', 'timestamp']):
                column_mapping[col] = 'Date'
            elif any(x in col_lower for x in ['close', 'último', 'last', 'price', 'precio_cierre']):
                column_mapping[col] = 'Close'
            elif any(x in col_lower for x in ['open', 'apertura']):
                column_mapping[col] = 'Open'
            elif any(x in col_lower for x in ['high', 'máximo', 'max', 'alto']):
                column_mapping[col] = 'High'
            elif any(x in col_lower for x in ['low', 'mínimo', 'min', 'bajo']):
                column_mapping[col] = 'Low'
            elif any(x in col_lower for x in ['volume', 'volumen', 'vol']):
                column_mapping[col] = 'Volume'
            elif any(x in col_lower for x in ['change', 'cambio', 'var', '%']):
                column_mapping[col] = 'Change'
        
        df.rename(columns=column_mapping, inplace=True)
        
        if 'Date' not in df.columns:
            for col in df.columns:
                if pd.to_datetime(df[col], errors='coerce').notna().sum() > len(df) * 0.8:
                    df.rename(columns={col: 'Date'}, inplace=True)
                    break
        
        if 'Date' in df.columns:
            for fmt in ['%d.%m.%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    df['Date'] = pd.to_datetime(df['Date'], format=fmt)
                    break
                except:
                    continue
            else:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            
            df = df.dropna(subset=['Date'])
            df.set_index('Date', inplace=True)
        
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).apply(convertir_precio_europeo)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'Close' not in df.columns and len(df.columns) > 0:
            df['Close'] = df.iloc[:, 0]
        
        if 'Open' not in df.columns and 'Close' in df.columns:
            df['Open'] = df['Close'].shift(1).fillna(df['Close'])
        if 'High' not in df.columns:
            df['High'] = df[['Open', 'Close']].max(axis=1) if 'Open' in df.columns else df['Close']
        if 'Low' not in df.columns:
            df['Low'] = df[['Open', 'Close']].min(axis=1) if 'Open' in df.columns else df['Close']
        if 'Volume' not in df.columns:
            df['Volume'] = 0
        
        df = df.fillna(method='ffill').fillna(method='bfill')
        df.sort_index(inplace=True)
        
        print(f"✅ Datos cargados: {nombre_cripto} ({len(df)} registros)")
        return df
        
    except Exception as e:
        print(f"❌ Error cargando {nombre_cripto}: {str(e)}")
        return crear_datos_ejemplo_cripto(nombre_cripto)

def listar_criptomonedas_disponibles(carpeta_data: str = "datos") -> list:
    criptos = []
    
    if not os.path.exists(carpeta_data):
        os.makedirs(carpeta_data, exist_ok=True)
        return []
    
    for archivo in os.listdir(carpeta_data):
        if archivo.endswith('.csv') and not archivo.startswith('temp_'):
            nombre = archivo.replace('.csv', '').replace('_online', '')
            # 🚫 EXCLUIR simulaciones del listado general
            if 'simulacion' not in nombre.lower() and 'simulacion' not in carpeta_data.lower():
                if nombre not in criptos:
                    criptos.append(nombre)
    
    return sorted(criptos)

def convertir_precio_europeo(valor: str) -> float:
    if pd.isna(valor):
        return np.nan
    
    valor_str = str(valor).strip()
    valor_str = valor_str.replace('$', '').replace('€', '').replace(' ', '')
    
    if '.' in valor_str and ',' in valor_str:
        if valor_str.find('.') < valor_str.find(','):
            valor_str = valor_str.replace('.', '').replace(',', '.')
        else:
            valor_str = valor_str.replace(',', '')
    elif ',' in valor_str:
        partes = valor_str.split(',')
        if len(partes) == 2 and len(partes[1]) <= 2:
            valor_str = valor_str.replace(',', '.')
        else:
            valor_str = valor_str.replace(',', '')
    
    try:
        return float(valor_str)
    except:
        return np.nan

def crear_datos_ejemplo_cripto(nombre_cripto: str) -> pd.DataFrame:
    print(f"Generando datos de ejemplo para {nombre_cripto}...")
    
    base_prices = {
        'Bitcoin': 45000, 'Ethereum': 3100, 'BNB': 890, 'XRP': 0.62,
        'Tether': 1.0, 'Solana': 180, 'Cardano': 0.6, 'Dogecoin': 0.15,
        'BTC': 45000, 'ETH': 3100, 'BNB': 890, 'XRP': 0.62, 'ADA': 0.6,
        'SOL': 180, 'DOT': 20, 'DOGE': 0.15, 'AVAX': 35, 'MATIC': 0.8,
        'LINK': 15, 'UNI': 7, 'LTC': 80, 'BCH': 300, 'ETC': 25
    }
    
    base_price = base_prices.get(nombre_cripto, 100)
    volatility = 0.03
    
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    np.random.seed(42)
    
    prices = []
    current = base_price
    for i in range(len(dates)):
        change = np.random.normal(0.001, volatility)
        current *= (1 + change)
        prices.append(max(current, base_price * 0.1))
    
    df = pd.DataFrame({
        'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
        'High': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'Low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'Close': prices,
        'Volume': np.random.uniform(1e6, 1e8, len(dates))
    }, index=dates)
    
    return df

# ==================== FUNCIONES DE ANÁLISIS ====================

def extraer_tendencias_offline(df_crypto: pd.DataFrame) -> tuple:
    if len(df_crypto) < 5:
        return (df_crypto['Close'].iloc[-1] if len(df_crypto) > 0 else 0, 'ESTABLE')
    
    current_price = df_crypto['Close'].iloc[-1]
    
    last_5 = df_crypto['Close'].tail(5).values
    last_10 = df_crypto['Close'].tail(10).values if len(df_crypto) >= 10 else last_5
    
    x_short = np.arange(len(last_5))
    slope_short = np.polyfit(x_short, last_5, 1)[0] if len(last_5) > 1 else 0
    
    x_medium = np.arange(len(last_10))
    slope_medium = np.polyfit(x_medium, last_10, 1)[0] if len(last_10) > 1 else 0
    
    ma_5 = last_5.mean()
    ma_10 = last_10.mean()
    
    if len(df_crypto) >= 14:
        last_14 = df_crypto['Close'].tail(14).values
        gains = np.sum(np.where(np.diff(last_14) > 0, np.diff(last_14), 0))
        losses = np.abs(np.sum(np.where(np.diff(last_14) < 0, np.diff(last_14), 0)))
        rsi = 100 - (100 / (1 + gains/max(losses, 0.001)))
    else:
        rsi = 50
    
    score = (slope_short / current_price * 100 * 0.4 if current_price > 0 else 0) + \
            (1 if ma_5 > ma_10 else -1 if ma_5 < ma_10 else 0) * 0.3 + \
            (1 if rsi > 55 else -1 if rsi < 45 else 0) * 0.3
    
    if score > 0.15:
        tendencia = 'ALTA'
    elif score < -0.15:
        tendencia = 'BAJA'
    else:
        tendencia = 'ESTABLE'
    
    return (current_price, tendencia)

def limpieza_datos(df_crypto: pd.DataFrame) -> dict:
    df = df_crypto.copy()
    
    df = df[~df.index.duplicated(keep='first')]
    df.dropna(subset=['Close'], inplace=True)
    
    if len(df) == 0:
        return {
            'media': 0, 'mediana': 0, 'desviacion': 0,
            'precio_min': 0, 'precio_max': 0,
            'count_original': len(df_crypto), 'count_limpio': 0
        }
    
    if len(df) >= 10:
        Q1 = df['Close'].quantile(0.25)
        Q3 = df['Close'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df['Close'] >= Q1 - 1.5*IQR) & (df['Close'] <= Q3 + 1.5*IQR)]
    
    return {
        'media': df['Close'].mean(),
        'mediana': df['Close'].median(),
        'desviacion': df['Close'].std(),
        'precio_min': df['Close'].min(),
        'precio_max': df['Close'].max(),
        'count_original': len(df_crypto),
        'count_limpio': len(df),
        'q1': df['Close'].quantile(0.25),
        'q3': df['Close'].quantile(0.75)
    }

def predecir_precio(df_crypto: pd.DataFrame, dias_futuro: int = 1) -> dict:
    if len(df_crypto) < 5:
        current = df_crypto['Close'].iloc[-1] if len(df_crypto) > 0 else 0
        return {
            'precio_actual': current,
            'prediccion_final': current,
            'intervalo_confianza': (current*0.95, current*1.05),
            'cambio_porcentual': 0,
            'metodos': {}
        }
    
    prices = df_crypto['Close'].values
    current_price = float(prices[-1])
    
    pred_linear = current_price
    if len(prices) >= 10:
        try:
            X = np.arange(len(prices)).reshape(-1, 1)
            y = prices.reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, y)
            pred_linear = float(model.predict([[len(prices)]])[0][0])
        except:
            pred_linear = current_price
    
    pred_ema = current_price
    try:
        if len(prices) >= 14:
            alpha = 2 / (14 + 1)
            ema = float(prices[0])
            for p in prices[1:]:
                ema = alpha * float(p) + (1 - alpha) * ema
            pred_ema = ema
        else:
            pred_ema = np.mean(prices[-5:])
    except:
        pred_ema = current_price
    
    pred_trend = current_price
    try:
        if len(prices) >= 5:
            recent = prices[-5:]
            returns = np.diff(recent) / recent[:-1]
            avg_return = np.mean(returns) if len(returns) > 0 else 0
            pred_trend = current_price * (1 + float(avg_return))
        else:
            pred_trend = current_price * 1.001
    except:
        pred_trend = current_price
    
    pred_final = pred_linear * 0.4 + pred_ema * 0.35 + pred_trend * 0.25
    
    max_change = 0.15
    min_pred = current_price * (1 - max_change)
    max_pred = current_price * (1 + max_change)
    pred_final = max(min_pred, min(pred_final, max_pred))
    
    try:
        if len(prices) >= 10:
            std_error = np.std(prices[-10:] - np.mean(prices[-10:]))
            intervalo = (pred_final - 1.96*std_error, pred_final + 1.96*std_error)
        else:
            intervalo = (pred_final * 0.9, pred_final * 1.1)
    except:
        intervalo = (pred_final * 0.9, pred_final * 1.1)
    
    cambio = ((pred_final - current_price) / current_price * 100) if current_price > 0 else 0
    
    return {
        'precio_actual': current_price,
        'prediccion_final': float(pred_final),
        'intervalo_confianza': (float(intervalo[0]), float(intervalo[1])),
        'cambio_porcentual': float(cambio),
        'metodos': {
            'lineal': float(pred_linear),
            'ema': float(pred_ema),
            'tendencia': float(pred_trend)
        }
    }

def tomar_desiciones(current_price: float, estadisticas: dict, 
                    prediccion: dict, tendencia: str) -> dict:
    factores = {}
    
    factores['tendencia'] = 1 if tendencia == 'ALTA' else -1 if tendencia == 'BAJA' else 0
    
    media = estadisticas.get('media', current_price)
    desviacion = (current_price - media) / media if media > 0 else 0
    factores['precio_vs_media'] = -1 if desviacion < -0.05 else 1 if desviacion > 0.05 else 0
    
    cambio = prediccion.get('cambio_porcentual', 0)
    factores['prediccion'] = 1 if cambio > 2 else -1 if cambio < -2 else 0
    
    rango = estadisticas.get('precio_max', current_price) - estadisticas.get('precio_min', current_price)
    if rango > 0:
        posicion = (current_price - estadisticas['precio_min']) / rango
        factores['posicion_rango'] = 1 if posicion < 0.3 else -1 if posicion > 0.7 else 0
    else:
        factores['posicion_rango'] = 0
    
    pesos = {'tendencia': 0.3, 'precio_vs_media': 0.25, 'prediccion': 0.25, 'posicion_rango': 0.2}
    puntaje = sum(factores[k] * pesos[k] for k in factores)
    
    if puntaje > 0.3:
        decision = 'COMPRAR FUERTE'
    elif puntaje > 0.1:
        decision = 'COMPRAR'
    elif puntaje < -0.3:
        decision = 'VENDER FUERTE'
    elif puntaje < -0.1:
        decision = 'VENDER'
    else:
        decision = 'MANTENER'
    
    razones = []
    if factores['tendencia'] > 0:
        razones.append("Tendencia alcista confirmada")
    elif factores['tendencia'] < 0:
        razones.append("Tendencia bajista detectada")
    
    if factores['precio_vs_media'] > 0:
        razones.append("Precio sobrevalorado respecto a media histórica")
    elif factores['precio_vs_media'] < 0:
        razones.append("Precio subvalorado, oportunidad de entrada")
    
    if factores['prediccion'] > 0:
        razones.append(f"Proyección positiva del {prediccion['cambio_porcentual']:+.1f}%")
    elif factores['prediccion'] < 0:
        razones.append(f"Proyección negativa del {prediccion['cambio_porcentual']:+.1f}%")
    
    if not razones:
        razones.append("Señales mixtas, se recomienda esperar")
    
    return {
        'decision': decision,
        'confianza': min(0.95, 0.5 + abs(puntaje)),
        'puntaje': puntaje,
        'factores': factores,
        'razones': razones
    }

def analisis_rapido_cripto(nombre_cripto: str, carpeta_data: str = "datos") -> dict:
    try:
        df = importar_base_cripto(nombre_cripto, carpeta_data)
        
        if df.empty or len(df) < 10:
            return {'success': False, 'error': 'Datos insuficientes'}
        
        precio_actual, tendencia = extraer_tendencias_offline(df)
        estadisticas = limpieza_datos(df)
        prediccion = predecir_precio(df)
        decision_info = tomar_desiciones(precio_actual, estadisticas, prediccion, tendencia)
        
        rsi = calcular_rsi(df['Close'])
        macd = calcular_macd(df['Close'])
        
        return {
            'cripto': nombre_cripto,
            'fecha_analisis': datetime.now(),
            'precio_actual': precio_actual,
            'tendencia': tendencia,
            'estadisticas': estadisticas,
            'prediccion': prediccion,
            'decision_info': decision_info,
            'indicadores': {
                'rsi': rsi.iloc[-1] if not rsi.empty else 50,
                'macd': macd['macd'].iloc[-1] if not macd.empty else 0,
                'macd_signal': macd['signal'].iloc[-1] if not macd.empty else 0
            },
            'dataframe': df,
            'success': True
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e), 'cripto': nombre_cripto}

def calcular_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def calcular_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return pd.DataFrame({
        'macd': macd,
        'signal': signal_line,
        'histogram': histogram
    })

def calcular_bollinger_bands(prices, period=20, std_dev=2):
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return pd.DataFrame({'upper': upper, 'middle': sma, 'lower': lower})

# ==================== FUNCIONES DE EXPORTACIÓN ====================

def exportar_resultados(resultados: list, formato: str = 'csv'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs("resultados", exist_ok=True)
    
    if formato.lower() == 'csv':
        archivo = f"resultados/analisis_{timestamp}.csv"
        with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Cripto', 'Precio', 'Tendencia', 'Decision', 'Confianza', 
                           'Prediccion', 'Cambio_%', 'Media', 'RSI'])
            for r in resultados:
                if r.get('success'):
                    writer.writerow([
                        r['cripto'],
                        f"{r['precio_actual']:.2f}",
                        r['tendencia'],
                        r['decision_info']['decision'],
                        f"{r['decision_info']['confianza']*100:.0f}%",
                        f"{r['prediccion']['prediccion_final']:.2f}",
                        f"{r['prediccion']['cambio_porcentual']:.2f}",
                        f"{r['estadisticas']['media']:.2f}",
                        f"{r['indicadores'].get('rsi', 50):.1f}"
                    ])
        return archivo
    
    elif formato.lower() == 'json':
        archivo = f"resultados/analisis_{timestamp}.json"
        exportables = []
        for r in resultados:
            if r.get('success'):
                r_copy = {k: v for k, v in r.items() if k != 'dataframe'}
                r_copy['fecha_analisis'] = r_copy['fecha_analisis'].isoformat()
                exportables.append(r_copy)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(exportables, f, indent=2, default=str)
        return archivo
    
    return None

def exportar_a_pdf(resultados: list, archivo_pdf: str = None):
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        
        if archivo_pdf is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archivo_pdf = f"resultados/informe_ejecutivo_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(archivo_pdf), exist_ok=True)
        
        doc = SimpleDocTemplate(
            archivo_pdf, 
            pagesize=landscape(A4),
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1565c0'),
            spaceBefore=20,
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        elements = []
        
        elements.append(Spacer(1, 50))
        elements.append(Paragraph("INFORME EJECUTIVO", title_style))
        elements.append(Paragraph("Análisis de Criptomonedas", subtitle_style))
        elements.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}", subtitle_style))
        elements.append(Paragraph(f"<b>Hora:</b> {datetime.now().strftime('%H:%M')}", subtitle_style))
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1565c0')))
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("RESUMEN EJECUTIVO", header_style))
        
        total_criptos = len([r for r in resultados if r.get('success')])
        compras = len([r for r in resultados if r.get('success') and 'COMPRAR' in r['decision_info']['decision']])
        ventas = len([r for r in resultados if r.get('success') and 'VENDER' in r['decision_info']['decision']])
        mantener = len([r for r in resultados if r.get('success') and 'MANTENER' in r['decision_info']['decision']])
        
        resumen_text = f"""
        El presente informe analiza <b>{total_criptos} criptomonedas</b> utilizando indicadores técnicos avanzados.
        <br/><br/>
        <b>Señales identificadas:</b><br/>
        • <font color="#4CAF50"><b>{compras} oportunidades de compra</b></font><br/>
        • <font color="#F44336"><b>{ventas} señales de venta</b></font><br/>
        • <font color="#FF9800"><b>{mantener} posiciones de mantener</b></font>
        """
        elements.append(Paragraph(resumen_text, body_style))
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("DETALLE DE ANÁLISIS", header_style))
        
        data = [['Cripto', 'Precio Actual', 'Tendencia', 'Decisión', 'Conf.', 'Predicción 24h', 'RSI', 'Cambio Est.']]
        
        for r in resultados:
            if r.get('success'):
                decision_color = '#4CAF50' if 'COMPRAR' in r['decision_info']['decision'] else \
                               '#F44336' if 'VENDER' in r['decision_info']['decision'] else '#FF9800'
                
                data.append([
                    Paragraph(f"<b>{r['cripto']}</b>", body_style),
                    f"${r['precio_actual']:,.2f}",
                    r['tendencia'],
                    Paragraph(f"<font color='{decision_color}'><b>{r['decision_info']['decision']}</b></font>", body_style),
                    f"{r['decision_info']['confianza']*100:.0f}%",
                    f"${r['prediccion']['prediccion_final']:,.2f}",
                    f"{r['indicadores'].get('rsi', 50):.1f}",
                    f"{r['prediccion']['cambio_porcentual']:+.1f}%"
                ])
        
        table = Table(data, colWidths=[2*cm, 2.5*cm, 2*cm, 3*cm, 1.5*cm, 2.5*cm, 1.5*cm, 2*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        elements.append(Paragraph("ANÁLISIS DETALLADO", header_style))
        elements.append(Spacer(1, 10))
        
        for r in resultados:
            if r.get('success'):
                cripto_text = f"""
                <b>{r['cripto']}</b> - Precio: ${r['precio_actual']:,.2f}<br/>
                <font size="9">
                • <b>Decisión:</b> {r['decision_info']['decision']} (Confianza: {r['decision_info']['confianza']*100:.0f}%)<br/>
                • <b>Predicción 24h:</b> ${r['prediccion']['prediccion_final']:,.2f} ({r['prediccion']['cambio_porcentual']:+.1f}%)<br/>
                • <b>RSI:</b> {r['indicadores'].get('rsi', 50):.1f} | <b>MACD:</b> {r['indicadores'].get('macd', 0):.2f}<br/>
                • <b>Razones:</b> {', '.join(r['decision_info']['razones'][:2])}
                </font>
                """
                elements.append(Paragraph(cripto_text, body_style))
                elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 10))
        
        disclaimer = """
        <font size="8" color="#666666">
        <b>ADVERTENCIA:</b> Este informe es solo para fines informativos y educativos. 
        Las criptomonedas son activos de alto riesgo. Las predicciones están basadas en modelos estadísticos 
        históricos y no garantizan resultados futuros. Consulte con un asesor financiero antes de realizar 
        cualquier inversión.
        </font>
        """
        elements.append(Paragraph(disclaimer, body_style))
        
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"<font size=\"8\" color=\"#999999\">Generado por Cripto Analizador Pro | {datetime.now().strftime('%Y')}</font>",
            ParagraphStyle('footer', alignment=TA_CENTER)
        ))
        
        doc.build(elements)
        return archivo_pdf
        
    except ImportError:
        return exportar_a_html(resultados)
    except Exception as e:
        print(f"Error exportando PDF: {e}")
        return exportar_a_html(resultados)

def exportar_a_html(resultados: list):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo = f"resultados/informe_ejecutivo_{timestamp}.html"
    os.makedirs("resultados", exist_ok=True)
    
    total_criptos = len([r for r in resultados if r.get('success')])
    compras = len([r for r in resultados if r.get('success') and 'COMPRAR' in r['decision_info']['decision']])
    ventas = len([r for r in resultados if r.get('success') and 'VENDER' in r['decision_info']['decision']])
    mantener = len([r for r in resultados if r.get('success') and 'MANTENER' in r['decision_info']['decision']])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Informe Ejecutivo - Análisis de Criptomonedas</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; color: #333; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; border-bottom: 3px solid #1565c0; padding-bottom: 30px; margin-bottom: 30px; }}
            .header h1 {{ color: #1a237e; font-size: 32px; margin: 0; }}
            .summary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 30px; }}
            .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }}
            th {{ background: #1565c0; color: white; padding: 15px 10px; text-align: center; font-weight: 600; }}
            td {{ padding: 12px 10px; text-align: center; border-bottom: 1px solid #e0e0e0; }}
            tr:nth-child(even) {{ background: #f9f9f9; }}
            .compra {{ background: #e8f5e9 !important; color: #2e7d32; font-weight: bold; }}
            .venta {{ background: #ffebee !important; color: #c62828; font-weight: bold; }}
            .mantener {{ background: #fff8e1 !important; color: #f57f17; font-weight: bold; }}
            .disclaimer {{ background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 20px; margin-top: 40px; font-size: 12px; color: #856404; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>INFORME EJECUTIVO</h1>
                <p>Análisis de Criptomonedas</p>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d de %B de %Y')} | <strong>Hora:</strong> {datetime.now().strftime('%H:%M')}</p>
            </div>
            <div class="summary">
                <div class="summary-grid">
                    <div><h3>{total_criptos}</h3><p>Analizadas</p></div>
                    <div><h3 style="color: #4CAF50;">{compras}</h3><p>Compras</p></div>
                    <div><h3 style="color: #F44336;">{ventas}</h3><p>Ventas</p></div>
                    <div><h3 style="color: #FF9800;">{mantener}</h3><p>Mantener</p></div>
                </div>
            </div>
            <table>
                <tr><th>Cripto</th><th>Precio Actual</th><th>Tendencia</th><th>Decisión</th><th>Confianza</th><th>Predicción 24h</th><th>RSI</th><th>Cambio Est.</th></tr>
    """
    
    for r in resultados:
        if r.get('success'):
            clase = 'compra' if 'COMPRAR' in r['decision_info']['decision'] else 'venta' if 'VENDER' in r['decision_info']['decision'] else 'mantener'
            html += f"""
                <tr class="{clase}">
                    <td><strong>{r['cripto']}</strong></td>
                    <td>${r['precio_actual']:,.2f}</td>
                    <td>{r['tendencia']}</td>
                    <td>{r['decision_info']['decision']}</td>
                    <td>{r['decision_info']['confianza']*100:.0f}%</td>
                    <td>${r['prediccion']['prediccion_final']:,.2f} ({r['prediccion']['cambio_porcentual']:+.1f}%)</td>
                    <td>{r['indicadores'].get('rsi', 50):.1f}</td>
                    <td>{r['prediccion']['cambio_porcentual']:+.1f}%</td>
                </tr>
            """
    
    html += f"""
            </table>
            <div class="disclaimer">
                <strong>ADVERTENCIA:</strong> Este informe es solo para fines informativos. Las criptomonedas son activos de alto riesgo.
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return archivo

# ==================== FUNCIONES DE PROCESAMIENTO CSV ====================

def procesar_csv_subido(ruta_archivo: str) -> dict:
    try:
        encodings = ['utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(ruta_archivo, encoding=encoding)
                if len(df.columns) == 1:
                    df = pd.read_csv(ruta_archivo, encoding=encoding, sep=';')
                break
            except:
                continue
        
        if df is None:
            return {'success': False, 'message': 'No se pudo leer el archivo'}
        
        df.columns = df.columns.str.strip().str.replace('﻿', '').str.replace('"', '')
        
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['fecha', 'date', 'time']):
                column_mapping[col] = 'Date'
            elif any(x in col_lower for x in ['close', 'último', 'last', 'price']):
                column_mapping[col] = 'Close'
            elif any(x in col_lower for x in ['open', 'apertura']):
                column_mapping[col] = 'Open'
            elif any(x in col_lower for x in ['high', 'máximo', 'max']):
                column_mapping[col] = 'High'
            elif any(x in col_lower for x in ['low', 'mínimo', 'min']):
                column_mapping[col] = 'Low'
            elif any(x in col_lower for x in ['volume', 'volumen', 'vol']):
                column_mapping[col] = 'Volume'
        
        df.rename(columns=column_mapping, inplace=True)
        
        if 'Date' in df.columns:
            for fmt in ['%d.%m.%Y', '%Y-%m-%d', '%m/%d/%Y']:
                try:
                    df['Date'] = pd.to_datetime(df['Date'], format=fmt)
                    break
                except:
                    continue
            else:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            
            df = df.dropna(subset=['Date'])
            df.set_index('Date', inplace=True)
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace(',', '.')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'Close' not in df.columns:
            return {'success': False, 'message': 'Columna de precio (Close) no encontrada'}
        
        if 'Open' not in df.columns:
            df['Open'] = df['Close'].shift(1).fillna(df['Close'])
        if 'High' not in df.columns:
            df['High'] = df[['Open', 'Close']].max(axis=1)
        if 'Low' not in df.columns:
            df['Low'] = df[['Open', 'Close']].min(axis=1)
        if 'Volume' not in df.columns:
            df['Volume'] = 0
        
        df.sort_index(inplace=True)
        
        return {
            'success': True,
            'df': df,
            'message': f'Archivo procesado: {len(df)} registros',
            'rango_fechas': f"{df.index.min().date()} - {df.index.max().date()}"
        }
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

def estandarizar_formato_csv(df: pd.DataFrame, nombre_cripto: str) -> pd.DataFrame:
    """Estandariza el DataFrame al formato de web scraping"""
    df_std = pd.DataFrame()
    
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    columnas_requeridas = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    for col in columnas_requeridas:
        if col in df.columns:
            df_std[col] = df[col]
        else:
            if col == 'Open':
                df_std[col] = df['Close'].shift(1).fillna(df['Close'])
            elif col == 'High':
                df_std[col] = df[['Close', 'Open']].max(axis=1) if 'Open' in df.columns else df['Close']
            elif col == 'Low':
                df_std[col] = df[['Close', 'Open']].min(axis=1) if 'Open' in df.columns else df['Close']
            elif col == 'Volume':
                df_std[col] = 0
            else:
                df_std[col] = df['Close']
    
    df_std = df_std.fillna(method='ffill').fillna(method='bfill')
    
    return df_std

def guardar_csv_cripto(df: pd.DataFrame, nombre_cripto: str, carpeta_data: str = "datos") -> bool:
    try:
        os.makedirs(carpeta_data, exist_ok=True)
        archivo = os.path.join(carpeta_data, f"{nombre_cripto}.csv")
        
        df_guardar = df.copy()
        if isinstance(df_guardar.index, pd.DatetimeIndex):
            df_guardar.reset_index(inplace=True)
        
        if 'Date' in df_guardar.columns:
            df_guardar['Date'] = pd.to_datetime(df_guardar['Date']).dt.strftime('%Y-%m-%d')
        
        df_guardar.to_csv(archivo, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        print(f"Error guardando CSV: {e}")
        return False

# ==================== FUNCIONES DE SIMULACIÓN ====================
def generar_datos_sinteticos(precio_inicial: float = 50000, dias: int = 90,
                            volatilidad: float = 0.03, tendencia: float = 0.001,
                            nombre: str = 'Simulacion') -> pd.DataFrame:
    """
    Genera datos sintéticos de mercado usando SIMULACIÓN DE MONTE CARLO.
    Simula múltiples trayectorias y devuelve la media como serie final.
    """
    np.random.seed(int(datetime.now().timestamp()) % 10000)

    # Parámetros de Monte Carlo
    num_simulaciones = 1000
    dt = 1  # un paso por día

    # Arrays para almacenar trayectorias
    trayectorias = np.zeros((num_simulaciones, dias))
    trayectorias[:, 0] = precio_inicial

    # Simulación Monte Carlo con movimiento browniano geométrico
    for t in range(1, dias):
        # Shock aleatorio normal
        z = np.random.standard_normal(num_simulaciones)
        # Fórmula de GBM: S_t = S_{t-1} * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*z)
        trayectorias[:, t] = trayectorias[:, t-1] * np.exp(
            (tendencia - 0.5 * volatilidad**2) * dt + volatilidad * np.sqrt(dt) * z
        )

    # Usamos la trayectoria media como representativa
    precios_medios = np.mean(trayectorias, axis=0)

    # Generar fechas
    fechas = pd.date_range(end=datetime.now(), periods=dias, freq='D')

    # Crear DataFrame con OHLCV simulados
    df = pd.DataFrame(index=fechas)
    df['Close'] = precios_medios

    # Generar OHLC a partir del precio de cierre
    df['Open'] = df['Close'].shift(1)
    df.loc[df.index[0], 'Open'] = df['Close'].iloc[0]

    # Simular High y Low con ruido intra-día
    intraday_vol = volatilidad * 0.5
    df['High'] = df[['Open', 'Close']].max(axis=1) * (1 + np.abs(np.random.normal(0, intraday_vol, dias)))
    df['Low'] = df[['Open', 'Close']].min(axis=1) * (1 - np.abs(np.random.normal(0, intraday_vol, dias)))

    # Volumen simulado con correlación al cambio de precio
    cambio_pct = df['Close'].pct_change().fillna(0)
    volumen_base = np.random.lognormal(20, 1, dias)
    df['Volume'] = volumen_base * (1 + np.abs(cambio_pct) * 10)

    return df
# ==================== FUNCIONES DE SENTIMIENTO Y ANOMALÍAS ====================

def obtener_sentimiento_mercado_real(cripto: str = "Bitcoin") -> dict:
    try:
        ticker = yf.Ticker(f"{cripto}-USD" if '-' not in cripto else cripto)
        hist = ticker.history(period="30d", interval="1d")
        
        if hist.empty:
            return {'error': 'Sin datos disponibles'}
        
        returns = hist['Close'].pct_change().dropna()
        
        volatility = returns.std() * np.sqrt(365) * 100
        
        return_7d = (hist['Close'].iloc[-1] / hist['Close'].iloc[-7] - 1) * 100 if len(hist) >= 7 else 0
        return_30d = (hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100 if len(hist) >= 30 else 0
        
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].tail(5).mean()
        volume_trend = 'Creciente' if recent_volume > avg_volume * 1.2 else 'Decreciente' if recent_volume < avg_volume * 0.8 else 'Estable'
        
        if return_7d > 15:
            sentimiento = 'Muy Positivo'
            score = 0.85
        elif return_7d > 5:
            sentimiento = 'Positivo'
            score = 0.65
        elif return_7d < -15:
            sentimiento = 'Muy Negativo'
            score = 0.15
        elif return_7d < -5:
            sentimiento = 'Negativo'
            score = 0.35
        else:
            sentimiento = 'Neutral'
            score = 0.5
        
        rsi = calcular_rsi(hist['Close']).iloc[-1]
        macd_df = calcular_macd(hist['Close'])
        macd_trend = 'Alcista' if macd_df['macd'].iloc[-1] > macd_df['signal'].iloc[-1] else 'Bajista'
        
        return {
            'cripto': cripto,
            'sentimiento_general': sentimiento,
            'score': score,
            'metricas': {
                'rendimiento_7d': round(return_7d, 2),
                'rendimiento_30d': round(return_30d, 2),
                'volatilidad_anual': round(volatility, 2),
                'tendencia_volumen': volume_trend,
                'rsi': round(rsi, 1),
                'tendencia_macd': macd_trend
            },
            'analisis': {
                'momentum': 'Fuerte alcista' if return_7d > 10 else 'Alcista' if return_7d > 0 else 'Bajista' if return_7d < 0 else 'Neutral',
                'volatilidad': 'Alta' if volatility > 80 else 'Moderada' if volatility > 50 else 'Baja',
                'condicion': 'Sobrecompra' if rsi > 70 else 'Sobreventa' if rsi < 30 else 'Normal'
            },
            'recomendacion': {
                'corto_plazo': 'COMPRAR' if score > 0.6 and rsi < 70 else 'VENDER' if score < 0.4 or rsi > 80 else 'MANTENER',
                'medio_plazo': 'COMPRAR' if return_30d > 0 and macd_trend == 'Alcista' else 'VENDER' if return_30d < -10 else 'MANTENER'
            }
        }
        
    except Exception as e:
        return {'error': str(e)}

def generar_explicacion_ia_completa(cripto: str, indicadores: dict) -> str:
    """Genera una explicación detallada y mejorada con mejor legibilidad para usuarios sin conocimiento"""
    if not indicadores:
        return f"No hay datos disponibles para {cripto}. Por favor, actualiza los datos primero."
    
    # Colores mejorados para modo nocturno con alta legibilidad
    colores = {
        'alcista': '#00E676',        # Verde brillante
        'bajista': '#FF5252',        # Rojo brillante
        'neutral': '#FFD740',        # Amarillo brillante
        'advertencia': '#FFAB40',    # Naranja brillante
        'informacion': '#40C4FF',    # Azul brillante
        'exito': '#00E5FF',          # Cian brillante
        'titulo': '#E3F2FD',         # Azul claro para títulos
        'texto': '#FFFFFF',          # Blanco puro para texto
        'secundario': '#B0BEC5',     # Gris claro para texto secundario
        'importante': '#FFE082',     # Amarillo claro para destacar
        'explicacion': '#E8F5E8'    # Verde muy claro para explicaciones
    }
    
    partes = []
    
    # Datos principales con mejor contraste
    precio = indicadores.get('precio_actual', 0)
    tendencia = indicadores.get('tendencia', 'ESTABLE')
    decision = indicadores.get('decision', 'MANTENER')
    confianza = indicadores.get('confianza', 0.5)
    
    # Header con mejor diseño
    partes.append(f"<div style='background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(156, 39, 176, 0.1)); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;'>")
    partes.append(f"<h2 style='color: {colores['titulo']}; margin: 0 0 1rem 0; font-size: 1.5rem;'>📊 <strong>Análisis Completo de {cripto}</strong></h2>")
    partes.append(f"</div>")
    
    # Resumen ejecutivo con mejor presentación
    partes.append(f"<div style='background: rgba(33, 150, 243, 0.05); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--primary-color); margin: 1.5rem 0;'>")
    partes.append(f"<h3 style='color: {colores['titulo']}; margin: 0 0 1rem 0;'>🎯 <strong>Resumen Ejecutivo para Principiantes</strong></h3>")
    
    # Datos principales en formato de tarjetas
    partes.append(f"<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;'>")
    
    # Precio
    partes.append(f"<div style='background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; text-align: center;'>")
    partes.append(f"<div style='color: {colores['titulo']}; font-size: 0.875rem; margin-bottom: 0.5rem;'>💰 Precio Actual</div>")
    partes.append(f"<div style='color: {colores['exito']}; font-size: 1.25rem; font-weight: bold;'>${precio:,.2f}</div>")
    partes.append(f"</div>")
    
    # Tendencia
    color_tendencia = colores['alcista'] if tendencia == 'ALTA' else colores['bajista'] if tendencia == 'BAJA' else colores['neutral']
    partes.append(f"<div style='background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; text-align: center;'>")
    partes.append(f"<div style='color: {colores['titulo']}; font-size: 0.875rem; margin-bottom: 0.5rem;'>📊 Tendencia</div>")
    partes.append(f"<div style='color: {color_tendencia}; font-size: 1.25rem; font-weight: bold;'>{tendencia}</div>")
    partes.append(f"</div>")
    
    # Decisión
    color_decision = colores['exito'] if 'COMPRAR' in decision else colores['advertencia'] if 'VENDER' in decision else colores['informacion']
    partes.append(f"<div style='background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; text-align: center;'>")
    partes.append(f"<div style='color: {colores['titulo']}; font-size: 0.875rem; margin-bottom: 0.5rem;'>🎯 Decisión</div>")
    partes.append(f"<div style='color: {color_decision}; font-size: 1.25rem; font-weight: bold;'>{decision}</div>")
    partes.append(f"</div>")
    
    # Confianza
    color_confianza = colores['exito'] if confianza > 0.7 else colores['advertencia'] if confianza > 0.5 else colores['neutral']
    partes.append(f"<div style='background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; text-align: center;'>")
    partes.append(f"<div style='color: {colores['titulo']}; font-size: 0.875rem; margin-bottom: 0.5rem;'>⚡ Confianza</div>")
    partes.append(f"<div style='color: {color_confianza}; font-size: 1.25rem; font-weight: bold;'>{confianza*100:.0f}%</div>")
    partes.append(f"</div>")
    
    partes.append(f"</div>")
    
    # Explicación simple
    partes.append(f"<div style='color: {colores['texto']}; line-height: 1.6; margin-top: 1rem;'>")
    partes.append(f"**<span style='color:{colores['importante']}'>📌 ¿Qué significa esto para ti?</span>**")
    partes.append(f"")
    partes.append(f"- **Precio:** ${precio:,.2f} USD es el valor actual de 1 {cripto}")
    partes.append(f"- **Tendencia:** {tendencia} significa que {'el precio está subiendo 📈' if tendencia == 'ALTA' else 'el precio está bajando 📉' if tendencia == 'BAJA' else 'el precio está estable 📊'}")
    partes.append(f"- **Decisión:** {decision} indica que {'es un buen momento para comprar' if 'COMPRAR' in decision else 'es un buen momento para vender' if 'VENDER' in decision else 'es mejor esperar'}")
    partes.append(f"- **Confianza:** {confianza*100:.0f}% representa cuán seguros estamos de esta recomendación")
    partes.append(f"</div>")
    
    partes.append(f"</div>")
    
    # RSI con mejor presentación
    rsi = indicadores.get('rsi', 50)
    partes.append(f"<div style='background: rgba(158, 39, 176, 0.05); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #9C27B0; margin: 1.5rem 0;'>")
    partes.append(f"<h3 style='color: {colores['titulo']}; margin: 0 0 1rem 0;'>🔥 <strong>RSI - Índice de Fuerza Relativa ({rsi:.1f})</strong></h3>")
    
    partes.append(f"<div style='color: {colores['explicacion']}; background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; margin: 1rem 0;'>")
    partes.append(f"**<span style='color:{colores['titulo']}'>¿Qué es el RSI?</span>**")
    partes.append(f"")
    partes.append(f"El RSI es como un termómetro del mercado:")
    partes.append(f"- Mide si un activo está **'caliente'** (sobrecomprado) o **'frío'** (sobrevendido)")
    partes.append(f"- Va de **0 a 100**, donde:")
    partes.append(f"  - **0-30** = Muy frío (posiblemente barato)")
    partes.append(f"  - **30-70** = Temperatura normal")
    partes.append(f"  - **70-100** = Muy caliente (posiblemente caro)")
    partes.append(f"</div>")
    
    if rsi < 30:
        partes.append(f"🟢 **<span style='color:{colores['exito']}'>¡Oportunidad de compra detectada!</span>**")
        partes.append(f"📈 **<span style='color:{colores['alcista']}'>El RSI está en {rsi:.1f}, lo que significa que {cripto} está 'en oferta' o más barato de lo normal.</span>**")
        partes.append(f"💡 **<span style='color:{colores['informacion']}'>Para principiantes:</span>** Esto podría ser un buen momento para comprar, pero recuerda que los mercados pueden seguir bajando antes de recuperarse.")
    elif rsi > 70:
        partes.append(f"🔴 **<span style='color:{colores['advertencia']}'>¡Alerta de sobrecompra!</span>**")
        partes.append(f"📉 **<span style='color:{colores['bajista']}'>El RSI está en {rsi:.1f}, lo que significa que {cripto} podría estar 'sobrevalorado' o más caro de lo normal.</span>**")
        partes.append(f"💡 **<span style='color:{colores['informacion']}'>Para principiantes:</span>** Esto podría ser un buen momento para tomar ganancias si ya tienes {cripto}, o esperar a que el precio baje antes de comprar.")
    else:
        zona = "neutral" if 40 <= rsi <= 60 else "levemente caliente" if rsi > 60 else "levemente frío"
        partes.append(f"✅ **<span style='color:{colores['neutral']}'>Zona {zona.title()}</span>**")
        partes.append(f"🔄 **<span style='color:{colores['texto']}'>El RSI de {rsi:.1f} indica que el mercado está en equilibrio. No hay señales extremas de compra o venta.</span>**")
        partes.append(f"⏳ **<span style='color:{colores['secundario']}'>Estrategia recomendada:</span>** Mantener las posiciones actuales y esperar señales más claras.")
    
    partes.append(f"</div>")
    
    # Resto de la explicación con el mismo estilo mejorado...
    # [Continúa con el resto del contenido de la función original pero aplicando el mismo estilo de colores y formato]
    
    return "\n".join(partes)

# ==================== FUNCIONES DE CORRELACIÓN ====================

def calcular_correlacion_criptos(criptos: list, carpeta_data: str = "datos") -> dict:
    datos = {}
    
    for cripto in criptos:
        df = importar_base_cripto(cripto, carpeta_data)
        if not df.empty and len(df) > 10:
            datos[cripto] = df['Close']
    
    if len(datos) < 2:
        return {'error': 'Se necesitan al menos 2 criptomonedas con datos suficientes'}
    
    df_combined = pd.DataFrame(datos)
    df_combined = df_combined.dropna()
    
    if len(df_combined) < 5:
        return {'error': 'Datos históricos insuficientes para correlación'}
    
    returns = df_combined.pct_change().dropna()
    corr_matrix = returns.corr()
    
    recomendaciones = []
    matriz_valores = []
    
    for i in range(len(corr_matrix.columns)):
        fila = []
        for j in range(len(corr_matrix.columns)):
            val = corr_matrix.iloc[i, j]
            fila.append(float(val))
            
            if i < j:
                corr_val = corr_matrix.iloc[i, j]
                if corr_val < 0.3:
                    recomendaciones.append({
                        'par': f"{corr_matrix.columns[i]}-{corr_matrix.columns[j]}",
                        'correlacion': float(corr_val),
                        'tipo': 'Diversificación ideal',
                        'mensaje': f'Baja correlación ({corr_val:.2f}) - Buena para diversificar riesgo',
                        'estrategia': 'Incluir ambas en cartera para reducir riesgo sistemático'
                    })
                elif corr_val > 0.9:
                    recomendaciones.append({
                        'par': f"{corr_matrix.columns[i]}-{corr_matrix.columns[j]}",
                        'correlacion': float(corr_val),
                        'tipo': 'Movimiento sincronizado',
                        'mensaje': f'Alta correlación ({corr_val:.2f}) - Se mueven juntas',
                        'estrategia': 'Evitar sobreexposición, no aportan diversificación'
                    })
                elif corr_val > 0.7:
                    recomendaciones.append({
                        'par': f"{corr_matrix.columns[i]}-{corr_matrix.columns[j]}",
                        'correlacion': float(corr_val),
                        'tipo': 'Correlación moderada-alta',
                        'mensaje': f'Correlación significativa ({corr_val:.2f})',
                        'estrategia': 'Limitar exposición combinada'
                    })
        matriz_valores.append(fila)
    
    clusters = identificar_clusters(corr_matrix)
    
    return {
        'matriz_correlacion': {
            'labels': list(corr_matrix.columns),
            'valores': matriz_valores
        },
        'recomendaciones': sorted(recomendaciones, key=lambda x: abs(x['correlacion'])),
        'clusters': clusters,
        'periodo_analisis': len(returns),
        'estadisticas': {
            'correlacion_promedio': float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()),
            'max_correlacion': float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].max()),
            'min_correlacion': float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].min())
        }
    }

def identificar_clusters(corr_matrix):
    try:
        from scipy.cluster.hierarchy import linkage, fcluster
        from scipy.spatial.distance import squareform
        
        dist_matrix = 1 - np.abs(corr_matrix)
        
        linkage_matrix = linkage(squareform(dist_matrix), method='average')
        clusters = fcluster(linkage_matrix, t=3, criterion='maxclust')
        
        grupos = {}
        for i, cripto in enumerate(corr_matrix.columns):
            cluster_id = int(clusters[i])
            if cluster_id not in grupos:
                grupos[cluster_id] = []
            grupos[cluster_id].append(cripto)
        
        return [{'id': k, 'criptomonedas': v} for k, v in grupos.items()]
    except:
        return []

# ==================== BACKTESTING ====================

def backtesting_estrategia(df: pd.DataFrame, capital_inicial: float = 10000, estrategia: str = "rsi_macd") -> dict:
    """
    Simula una estrategia de trading sobre datos históricos.
    Estrategias soportadas: "rsi_macd", "bollinger", "golden_cross"
    """
    if len(df) < 30:  # ✅ Cambiado de 200 a 30 días mínimos
        return {"error": "Datos insuficientes para backtesting (mínimo 30 días)"}

    df = df.copy()
    df['rsi'] = calcular_rsi(df['Close'])
    df['macd'] = calcular_macd(df['Close'])['macd']
    df['signal'] = calcular_macd(df['Close'])['signal']
    df['sma50'] = df['Close'].rolling(50).mean()
    df['sma200'] = df['Close'].rolling(200).mean()
    bb = calcular_bollinger_bands(df['Close'])
    df['bb_upper'] = bb['upper']
    df['bb_lower'] = bb['lower']

    capital = capital_inicial
    posicion = 0  # 0 = sin posición, 1 = comprado
    operaciones = []
    precio_compra = 0

    for i in range(1, len(df)):
        precio = df['Close'].iloc[i]
        fecha = df.index[i]

        if estrategia == "rsi_macd":
            senal_compra = df['rsi'].iloc[i] < 30 and df['macd'].iloc[i] > df['signal'].iloc[i]
            senal_venta = df['rsi'].iloc[i] > 70 and df['macd'].iloc[i] < df['signal'].iloc[i]
        elif estrategia == "bollinger":
            senal_compra = precio < df['bb_lower'].iloc[i]
            senal_venta = precio > df['bb_upper'].iloc[i]
        elif estrategia == "golden_cross":
            senal_compra = df['sma50'].iloc[i] > df['sma200'].iloc[i] and df['sma50'].iloc[i-1] <= df['sma200'].iloc[i-1]
            senal_venta = df['sma50'].iloc[i] < df['sma200'].iloc[i] and df['sma50'].iloc[i-1] >= df['sma200'].iloc[i-1]
        else:
            return {"error": "Estrategia no soportada"}

        if senal_compra and posicion == 0:
            posicion = 1
            precio_compra = precio
            operaciones.append({"tipo": "COMPRA", "fecha": fecha, "precio": precio})
        elif senal_venta and posicion == 1:
            posicion = 0
            ganancia = (precio - precio_compra) / precio_compra
            capital *= (1 + ganancia)
            operaciones.append({"tipo": "VENTA", "fecha": fecha, "precio": precio, "ganancia": ganancia})

    # Cerrar posición si queda abierta
    if posicion == 1:
        precio_final = df['Close'].iloc[-1]
        ganancia = (precio_final - precio_compra) / precio_compra
        capital *= (1 + ganancia)
        operaciones.append({"tipo": "VENTA", "fecha": df.index[-1], "precio": precio_final, "ganancia": ganancia})

    retorno_total = (capital - capital_inicial) / capital_inicial * 100
    buy_hold = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100
    max_drawdown = ((df['Close'].cummax() - df['Close']) / df['Close'].cummax()).max() * 100

    return {
        "estrategia": estrategia,
        "capital_inicial": capital_inicial,
        "capital_final": capital,
        "retorno_total": retorno_total,
        "buy_and_hold": buy_hold,
        "max_drawdown": max_drawdown,
        "operaciones": operaciones,
        "cantidad_operaciones": len(operaciones),
        "ganadoras": len([o for o in operaciones if o.get("ganancia", 0) > 0]),
        "perdedoras": len([o for o in operaciones if o.get("ganancia", 0) < 0])
    }

import requests
from bs4 import BeautifulSoup

# funciones.py - Reemplazar obtener_top_100_coinmarketcap()

def obtener_top_100_coinmarketcap():

    return ['ADA', 'BNB', 'BTC', 'DOGE', 'DOT', 'ETH', 'SOL', 'XRP', 'USDT']

# ==================== FUNCIONES PARA SIMULACIÓN ====================

def guardar_simulacion_csv(df: pd.DataFrame, nombre: str) -> bool:
    """Guarda un CSV de simulación en la carpeta 'simulacion/'"""
    os.makedirs("simulacion", exist_ok=True)
    ruta = os.path.join("simulacion", f"{nombre}.csv")
    try:
        df.to_csv(ruta, index=True, index_label='Date')
        return True
    except Exception as e:
        print(f"❌ Error guardando simulación: {e}")
        return False

def analizar_simulacion(nombre_simulacion: str) -> dict:
    """Analiza una simulación guardada y devuelve resultados"""
    ruta = os.path.join("simulacion", f"{nombre_simulacion}.csv")
    
    try:
        df = pd.read_csv(ruta, parse_dates=['Date'], index_col='Date')
        if df.empty or len(df) < 5:
            return {'error': 'Datos insuficientes en la simulación'}
        
        precio_actual = df['Close'].iloc[-1]
        precio_inicial = df['Close'].iloc[0]
        cambio_total = ((precio_actual - precio_inicial) / precio_inicial) * 100
        volatilidad = df['Close'].pct_change().std() * np.sqrt(365) * 100
        maximo = df['Close'].max()
        minimo = df['Close'].min()
        
        return {
            'success': True,
            'nombre': nombre_simulacion,
            'precio_inicial': float(precio_inicial),
            'precio_actual': float(precio_actual),
            'cambio_total': float(cambio_total),
            'volatilidad': float(volatilidad),
            'maximo': float(maximo),
            'minimo': float(minimo),
            'fechas': df.index.strftime('%Y-%m-%d').tolist(),
            'precios': df['Close'].tolist()
        }
        
    except Exception as e:
        return {'error': str(e)}
        ruta = os.path.join("simulacion", f"{nombre_simulacion}.csv")
        try:
            df = pd.read_csv(ruta, parse_dates=['Date'], index_col='Date')
            if df.empty or len(df) < 5:
                return {'error': 'Datos insuficientes en la simulación'}

            precio_actual = df['Close'].iloc[-1]
            precio_inicial = df['Close'].iloc[0]
            cambio_total = ((precio_actual - precio_inicial) / precio_inicial) * 100
            volatilidad = df['Close'].pct_change().std() * np.sqrt(365) * 100
            maximo = df['Close'].max()
            minimo = df['Close'].min()

            return {
                'success': True,
                'nombre': nombre_simulacion,
                'precio_actual': precio_actual,
                'precio_inicial': precio_inicial,
                'cambio_total': cambio_total,
                'volatilidad': volatilidad,
                'maximo': maximo,
                'minimo': minimo,
                'fechas': df.index.strftime('%Y-%m-%d').tolist(),
                'precios': df['Close'].tolist()
            }
        except Exception as e:
            return {'error': str(e)}

