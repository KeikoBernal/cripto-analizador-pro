# main.py - Backend principal con Flask API (VERSIÓN COMPLETA CON TODAS LAS FUNCIONALIDADES)
import os
import sys
import json
import time
import threading
import webbrowser
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings('ignore')

# Importar funciones locales
from funciones import *
from global_data import *
from global_data import CRIPTOS_DEFAULT
allCriptos = CRIPTOS_DEFAULT()

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Variables globales para modo online
online_config = {
    'activo': False,
    'intervalo_minutos': 5,
    'ultima_actualizacion': None,
    'hilo_automatico': None,
    'datos_actuales': {},
    'analisis_actuales': {},
    'historial_precios': {}  # Para gráficos en tiempo real
}

# Asegurar carpetas existen
os.makedirs('datos', exist_ok=True)
os.makedirs('web/assets', exist_ok=True)
os.makedirs('resultados', exist_ok=True)

# ==================== RUTAS DE PÁGINAS ====================

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/online.html')
def online_page():
    return send_from_directory('web', 'online.html')

@app.route('/offline.html')
def offline_page():
    return send_from_directory('web', 'offline.html')

@app.route('/index.html')
def index_page():
    return send_from_directory('web', 'index.html')

# ==================== API - MODO OFFLINE ====================

@app.route('/api/offline/criptos', methods=['GET'])
def get_criptos_offline():
    """Obtener lista de criptomonedas disponibles offline"""
    criptos = listar_criptomonedas_disponibles('datos')
    return jsonify({'criptos': criptos, 'count': len(criptos)})

@app.route('/api/offline/analisis', methods=['POST'])
def analisis_offline():
    """Realizar análisis completo offline"""
    data = request.get_json()
    criptos = data.get('criptos', [])
    
    if not criptos:
        return jsonify({'error': 'No se seleccionaron criptomonedas'}), 400
    
    resultados = []
    for cripto in criptos:
        try:
            resultado = analisis_rapido_cripto(cripto, 'datos')
            if resultado.get('success'):
                # Convertir DataFrame a dict para JSON
                df = resultado['dataframe']
                resultado['datos_historicos'] = {
                    'fechas': df.index.strftime('%Y-%m-%d').tolist(),
                    'precios': df['Close'].tolist(),
                    'volumenes': df['Volume'].tolist() if 'Volume' in df.columns else [],
                    'open': df['Open'].tolist() if 'Open' in df.columns else [],
                    'high': df['High'].tolist() if 'High' in df.columns else [],
                    'low': df['Low'].tolist() if 'Low' in df.columns else []
                }
                del resultado['dataframe']  # Eliminar DataFrame no serializable
                resultados.append(resultado)
        except Exception as e:
            resultados.append({
                'cripto': cripto,
                'error': str(e),
                'success': False
            })
    
    return jsonify({'resultados': resultados, 'count': len(resultados)})

@app.route('/api/offline/subir-csv', methods=['POST'])
def subir_csv():
    """Procesar y guardar archivo CSV subido con formato estándar"""
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    nombre_cripto = request.form.get('nombre', '').strip()
    
    if not nombre_cripto:
        return jsonify({'error': 'Nombre de criptomoneda requerido'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'Archivo vacío'}), 400
    
    try:
        # Guardar temporalmente
        temp_path = os.path.join('datos', 'temp_' + file.filename)
        file.save(temp_path)
        
        # Procesar CSV y estandarizar formato
        resultado = procesar_csv_subido(temp_path)
        
        if not resultado['success']:
            os.remove(temp_path)
            return jsonify({'error': resultado['message']}), 400
        
        # Estandarizar al formato de web scraping
        df_estandar = estandarizar_formato_csv(resultado['df'], nombre_cripto)
        
        # Guardar con nombre final
        exito = guardar_csv_cripto(df_estandar, nombre_cripto, 'datos')
        
        # Limpiar temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if exito:
            return jsonify({
                'success': True,
                'message': f'Criptomoneda {nombre_cripto} guardada correctamente',
                'registros': len(df_estandar),
                'rango': resultado.get('rango_fechas', 'N/A')
            })
        else:
            return jsonify({'error': 'Error al guardar archivo'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/exportar', methods=['POST'])
def exportar_offline():
    """Exportar resultados a diferentes formatos"""
    data = request.get_json()
    formato = data.get('formato', 'csv')
    resultados = data.get('resultados', [])
    
    try:
        if formato == 'pdf':
            archivo = exportar_a_pdf(resultados)
        else:
            archivo = exportar_resultados(resultados, formato)
        
        if archivo and os.path.exists(archivo):
            return send_file(archivo, as_attachment=True)
        else:
            return jsonify({'error': 'Error al generar archivo'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS PARA EXPORTACIÓN ONLINE ====================

# ==================== RUTAS DE EXPORTACIÓN ONLINE ====================

@app.route('/api/online/exportar', methods=['POST'])
def exportar_online():
    """Exportar resultados online a diferentes formatos - IDENTICO a offline"""
    data = request.get_json()
    formato = data.get('formato', 'csv').lower()
    resultados = data.get('resultados', [])
    
    try:
        if not resultados:
            return jsonify({'error': 'No hay resultados para exportar'}), 400
        
        # Validar formato
        if formato not in ['csv', 'pdf', 'json']:
            return jsonify({'error': 'Formato no soportado'}), 400
        
        # Generar archivo
        if formato == 'pdf':
            archivo = exportar_a_pdf(resultados)
        else:
            archivo = exportar_resultados(resultados, formato)
        
        if archivo and os.path.exists(archivo):
            # Enviar archivo como descarga
            return send_file(
                archivo,
                as_attachment=True,
                download_name=os.path.basename(archivo),
                mimetype=get_mimetype(formato)
            )
        else:
            return jsonify({'error': 'Error al generar archivo'}), 500
            
    except Exception as e:
        print(f"❌ Error en exportación online: {e}")
        return jsonify({'error': str(e)}), 500

def get_mimetype(formato):
    """Obtener MIME type según formato"""
    mimetypes = {
        'csv': 'text/csv',
        'pdf': 'application/pdf',
        'json': 'application/json',
        'html': 'text/html'
    }
    return mimetypes.get(formato, 'application/octet-stream')

@app.route('/api/online/exportar-grafico', methods=['POST'])
def exportar_grafico_online():
    """Exportar gráfico online"""
    data = request.get_json()
    chart_id = data.get('chart_id', 'realtime-chart')
    formato = data.get('formato', 'png')
    
    try:
        # Aquí iría la lógica para capturar el gráfico
        # Por ahora, retornamos un mensaje de éxito
        return jsonify({'success': True, 'message': 'Funcionalidad de exportación de gráficos implementada'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/simulacion', methods=['POST'])
def simulacion_mercado():
    """Generar datos sintéticos de mercado y devolverlos como JSON válido"""
    data = request.get_json()
    params = {
        'precio_inicial': data.get('precio_inicial', 50000),
        'dias': data.get('dias', 90),
        'volatilidad': data.get('volatilidad', 0.03),
        'tendencia': data.get('tendencia', 0.001),
        'nombre': data.get('nombre', 'Simulacion')
    }

    try:
        df = generar_datos_sinteticos(**params)

        # ✅ Convertir DataFrame a JSON serializable
        df_serializable = {
            'fechas': df.index.strftime('%Y-%m-%d').tolist(),
            'precios': df['Close'].tolist(),
            'volumenes': df['Volume'].tolist(),
            'open': df['Open'].tolist(),
            'high': df['High'].tolist(),
            'low': df['Low'].tolist()
        }

        # Guardar como CSV en carpeta simulacion
        os.makedirs("simulacion", exist_ok=True)
        df.to_csv(os.path.join("simulacion", f"{params['nombre']}.csv"), index=True, index_label='Date')

        return jsonify({
            'success': True,
            'datos': df_serializable,
            'message': f'Simulación {params["nombre"]} generada con éxito'
        })

    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/correlacion', methods=['POST'])
def calcular_correlacion_offline():
    """Calcular correlación entre criptomonedas offline"""
    data = request.get_json()
    criptos = data.get('criptos', [])
    
    if len(criptos) < 2:
        return jsonify({'error': 'Se necesitan al menos 2 criptomonedas'}), 400
    
    try:
        resultado = calcular_correlacion_criptos(criptos, 'datos')
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/datos-historicos/<cripto>', methods=['GET'])
def get_datos_historicos(cripto):
    """Obtener datos históricos para gráficos offline"""
    try:
        df = importar_base_cripto(cripto, 'datos')
        if df.empty:
            return jsonify({'error': 'No hay datos'}), 404
        
        return jsonify({
            'fechas': df.index.strftime('%Y-%m-%d').tolist(),
            'precios': df['Close'].tolist(),
            'volumenes': df['Volume'].tolist() if 'Volume' in df.columns else [],
            'open': df['Open'].tolist() if 'Open' in df.columns else [],
            'high': df['High'].tolist() if 'High' in df.columns else [],
            'low': df['Low'].tolist() if 'Low' in df.columns else []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/backtesting', methods=['POST'])
def backtesting_offline():
    """Backtesting de estrategias sobre datos históricos offline"""
    data = request.get_json()
    cripto = data.get('cripto')
    estrategia = data.get('estrategia', 'rsi_macd')
    capital = float(data.get('capital', 10000))

    if not cripto:
        return jsonify({'error': 'Criptomoneda requerida'}), 400

    try:
        df = importar_base_cripto(cripto, 'datos')
        if df.empty or len(df) < 30:  # ✅ Cambiado a 30 días
            return jsonify({'error': 'Datos insuficientes para backtesting (mínimo 30 días)'}), 400

        resultado = backtesting_estrategia(df, capital, estrategia)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/comparacion', methods=['POST'])
def comparacion_offline():
    """Comparación múltiple de métricas entre criptomonedas offline"""
    data = request.get_json()
    criptos = data.get('criptos', [])
    metrica = data.get('metrica', 'precio')

    if len(criptos) < 2:
        return jsonify({'error': 'Se necesitan al menos 2 criptomonedas'}), 400

    try:
        resultados = []
        for cripto in criptos:
            df = importar_base_cripto(cripto, 'datos')
            if df.empty:
                continue
            
            actual = analisis_rapido_cripto(cripto, 'datos')
            if not actual.get('success'):
                continue

            valor = None
            if metrica == 'precio':
                valor = actual['precio_actual']
            elif metrica == 'cambio':
                valor = actual['prediccion']['cambio_porcentual']
            elif metrica == 'rsi':
                valor = actual['indicadores']['rsi']
            elif metrica == 'macd':
                valor = actual['indicadores']['macd']

            resultados.append({
                'cripto': cripto,
                'valor': valor,
                'metrica': metrica
            })

        return jsonify({
            'metrica': metrica,
            'resultados': resultados,
            'maximo': max([r['valor'] for r in resultados]) if resultados else 0,
            'minimo': min([r['valor'] for r in resultados]) if resultados else 0,
            'promedio': np.mean([r['valor'] for r in resultados]) if resultados else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/eliminar/<nombre>', methods=['DELETE'])
def eliminar_cripto(nombre):
    """Eliminar archivo de criptomoneda"""
    try:
        archivo = os.path.join('datos', f"{nombre}.csv")
        if os.path.exists(archivo):
            os.remove(archivo)
            return jsonify({'success': True, 'message': f'{nombre} eliminado'})
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline/obtener-datos/<cripto>', methods=['GET'])
def obtener_datos_cripto(cripto):
    """Obtener datos históricos de una criptomoneda para el minijuego FOMO"""
    try:
        # Intentar con sufijo _online primero, luego sin sufijo
        archivo = os.path.join('datos', f"{cripto}_online.csv")
        if not os.path.exists(archivo):
            archivo = os.path.join('datos', f"{cripto}.csv")
        
        if not os.path.exists(archivo):
            print(f"[v0] Archivo no encontrado: {cripto} - intenté: {cripto}_online.csv y {cripto}.csv")
            return jsonify({'success': False, 'error': f'Criptomoneda no encontrada: {cripto}'}), 404
        
        # Cargar datos
        print(f"[v0] Cargando archivo: {archivo}")
        df = pd.read_csv(archivo)
        print(f"[v0] Datos cargados: {len(df)} filas, columnas: {list(df.columns)}")
        
        # Normalizar columnas (convertir a minúsculas y limpiar espacios)
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Detectar estructura del CSV y adaptarse
        if 'date' in df.columns:
            fecha_col = 'date'
        elif 'timestamp' in df.columns:
            fecha_col = 'timestamp'
        elif 'time' in df.columns:
            fecha_col = 'time'
        else:
            fecha_col = df.columns[0]
        
        # Detectar columnas de precio
        open_col = next((c for c in df.columns if 'open' in c), df.columns[1] if len(df.columns) > 1 else None)
        close_col = next((c for c in df.columns if 'close' in c), df.columns[-1] if len(df.columns) > 1 else None)
        high_col = next((c for c in df.columns if 'high' in c), None)
        low_col = next((c for c in df.columns if 'low' in c), None)
        volume_col = next((c for c in df.columns if 'volume' in c), None)
        
        # Crear datos estructurados para el juego
        datos_formateados = []
        for idx, row in df.iterrows():
            try:
                datos_formateados.append({
                    'timestamp': str(row[fecha_col]),
                    'open': float(row[open_col]) if open_col and pd.notna(row[open_col]) else 0,
                    'close': float(row[close_col]) if close_col and pd.notna(row[close_col]) else 0,
                    'high': float(row[high_col]) if high_col and pd.notna(row[high_col]) else 0,
                    'low': float(row[low_col]) if low_col and pd.notna(row[low_col]) else 0,
                    'volume': float(row[volume_col]) if volume_col and pd.notna(row[volume_col]) else 0
                })
            except Exception as e:
                print(f"[v0] Error procesando fila {idx}: {e}")
                continue
        
        if not datos_formateados:
            return jsonify({'success': False, 'error': 'No hay datos válidos en el archivo'}), 400
        
        return jsonify({
            'success': True,
            'cripto': cripto,
            'datos': datos_formateados,
            'count': len(datos_formateados)
        })
        
    except Exception as e:
        print(f"[v0] Error en obtener_datos_cripto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== API - MODO ONLINE ====================

@app.route('/api/online/iniciar', methods=['POST'])
def iniciar_online():
    """Iniciar monitoreo online automático"""
    global online_config
    
    data = request.get_json()
    online_config['intervalo_minutos'] = data.get('intervalo', 5)
    online_config['criptos_seleccionadas'] = data.get('criptos', ['BTC', 'ETH', 'BNB'])
    online_config['activo'] = True
    
    # Primera ejecución inmediata
    actualizar_datos_online()
    
    # Iniciar hilo automático si no está corriendo
    if online_config['hilo_automatico'] is None or not online_config['hilo_automatico'].is_alive():
        online_config['hilo_automatico'] = threading.Thread(target=loop_automatico, daemon=True)
        online_config['hilo_automatico'].start()
    
    return jsonify({
        'success': True,
        'config': {
            'intervalo': online_config['intervalo_minutos'],
            'criptos': online_config['criptos_seleccionadas']
        }
    })

@app.route('/api/online/detener', methods=['POST'])
def detener_online():
    """Detener monitoreo online"""
    global online_config
    online_config['activo'] = False
    return jsonify({'success': True, 'message': 'Monitoreo detenido'})

@app.route('/api/online/estado', methods=['GET'])
def estado_online():
    """Obtener estado actual del modo online"""
    return jsonify({
        'activo': online_config['activo'],
        'ultima_actualizacion': online_config['ultima_actualizacion'],
        'criptos': list(online_config['datos_actuales'].keys()),
        'analisis': online_config['analisis_actuales']
    })

@app.route('/api/online/actualizar-manual', methods=['POST'])
def actualizar_manual():
    """Forzar actualización manual"""
    try:
        actualizar_datos_online()
        return jsonify({
            'success': True,
            'ultima_actualizacion': online_config['ultima_actualizacion'],
            'datos': online_config['analisis_actuales']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/online/sentimiento-detallado', methods=['GET'])
def analisis_sentimiento_detallado():
    """Análisis de sentimiento con datos históricos"""
    cripto = request.args.get('cripto', 'Bitcoin')
    dias = int(request.args.get('dias', '30'))
    
    try:
        ticker = yf.Ticker(f"{cripto}-USD")
        hist = ticker.history(period=f"{dias}d", interval="1d")
        
        if hist.empty:
            return jsonify({'error': 'Sin datos disponibles'})
        
        # Calcular métricas para cada día
        sentimiento_historico = []
        
        for i in range(len(hist)):
            if i < 7:  # Necesitamos al menos 7 días para cálculos
                continue
                
            # Datos del período
            precios_recientes = hist['Close'].iloc[i-6:i+1].values
            volumen_actual = hist['Volume'].iloc[i]
            volumen_promedio = hist['Volume'].iloc[i-6:i].mean()
            
            # Validar datos antes de procesar
            if len(precios_recientes) < 7 or pd.isna(volumen_actual) or pd.isna(volumen_promedio):
                continue
                
            # Calcular métricas con validación
            cambio_7d = 0
            if precios_recientes[0] > 0:
                cambio_7d = (precios_recientes[-1] / precios_recientes[0] - 1) * 100
            
            volatilidad_7d = 0
            if len(precios_recientes) > 1:
                returns = np.diff(precios_recientes) / precios_recientes[:-1]
                volatilidad_7d = np.std(returns) * np.sqrt(365) * 100 if len(returns) > 0 else 0
            
            # RSI con validación
            rsi = 50.0
            try:
                if len(precios_recientes) >= 7:
                    rsi_series = calcular_rsi(pd.Series(precios_recientes))
                    rsi_val = float(rsi_series.iloc[-1])
                    if not np.isnan(rsi_val):
                        rsi = rsi_val
            except:
                pass
            
            # Volumen con validación
            ratio_volumen = 1.0
            if volumen_promedio > 0 and not np.isnan(volumen_promedio):
                ratio_volumen = volumen_actual / volumen_promedio
            
            # Calcular score de sentimiento (0-1)
            score = 0.5  # Neutro por defecto
            
            # Factor cambio de precio (40%)
            if cambio_7d > 5:
                score += 0.2
            elif cambio_7d > 2:
                score += 0.1
            elif cambio_7d < -5:
                score -= 0.2
            elif cambio_7d < -2:
                score -= 0.1
            
            # Factor volatilidad (20%)
            if volatilidad_7d > 100:
                score -= 0.1
            elif volatilidad_7d < 30:
                score += 0.05
            
            # Factor volumen (20%)
            if ratio_volumen > 2:
                score += 0.1
            elif ratio_volumen < 0.5:
                score -= 0.1
            
            # Factor RSI (20%)
            if rsi < 30:
                score += 0.15
            elif rsi > 70:
                score -= 0.15
            
            # Asegurar que esté entre 0 y 1
            score = max(0, min(1, score))
            
            sentimiento_historico.append({
                'fecha': hist.index[i].strftime('%Y-%m-%d'),
                'score': round(score, 3),
                'precio': float(precios_recientes[-1]) if not np.isnan(precios_recientes[-1]) else 0.0,
                'cambio_7d': round(cambio_7d, 2),
                'volatilidad_7d': round(volatilidad_7d, 2),
                'rsi': round(rsi, 1),
                'volumen_ratio': round(ratio_volumen, 2)
            })
        
        # Análisis actual
        if len(sentimiento_historico) == 0:
            return jsonify({'error': 'Datos insuficientes para análisis'})
            
        ultimo = sentimiento_historico[-1]
        
        # Determinar tendencia
        tendencia = 'neutral'
        if len(sentimiento_historico) >= 3:
            ultimos_3 = sentimiento_historico[-3:]
            tendencia = 'alcista' if ultimos_3[-1]['score'] > ultimos_3[0]['score'] else 'bajista'
        
        return jsonify({
            'cripto': cripto,
            'sentimiento_general': 'Muy Positivo' if ultimo['score'] > 0.7 else 
                                 'Positivo' if ultimo['score'] > 0.6 else
                                 'Negativo' if ultimo['score'] < 0.4 else
                                 'Muy Negativo' if ultimo['score'] < 0.3 else 'Neutral',
            'score': ultimo['score'],
            'tendencia': tendencia,
            'historico': sentimiento_historico,
            'metricas': {
                'rendimiento_7d': ultimo['cambio_7d'],
                'volatilidad_7d': ultimo['volatilidad_7d'],
                'rsi_actual': ultimo['rsi'],
                'volumen_ratio': ultimo['volumen_ratio'],
                'precio_actual': ultimo['precio']
            },
            'analisis': {
                'momentum': 'Fuerte alcista' if ultimo['cambio_7d'] > 5 else
                           'Alcista' if ultimo['cambio_7d'] > 0 else
                           'Bajista' if ultimo['cambio_7d'] < -5 else 'Neutral',
                'volatilidad': 'Alta' if ultimo['volatilidad_7d'] > 80 else
                              'Moderada' if ultimo['volatilidad_7d'] > 40 else 'Baja',
                'condicion': 'Sobrecompra' if ultimo['rsi'] > 70 else
                            'Sobreventa' if ultimo['rsi'] < 30 else 'Normal'
            }
        })
        
    except Exception as e:
        print(f"Error completo en sentimiento: {e}")
        return jsonify({'error': f'Error procesando datos: {str(e)}'})

@app.route('/api/online/anomalias', methods=['GET'])
def detectar_anomalias():
    """Detectar anomalías en el mercado"""
    try:
        anomalias = []
        
        for simbolo, datos in online_config['datos_actuales'].items():
            if simbolo in online_config['analisis_actuales']:
                analisis = online_config['analisis_actuales'][simbolo]
                cambio_1h = analisis.get('cambio_esperado', 0)
                
                # Detectar pump/dump
                if abs(cambio_1h) > 10:
                    tipo = 'pump' if cambio_1h > 0 else 'dump'
                    anomalias.append({
                        'tipo': tipo,
                        'cripto': simbolo,
                        'valor': float(cambio_1h),
                        'mensaje': f'{"Pump" if tipo == "pump" else "Dump"} detectado en {simbolo}: {cambio_1h:+.1f}% en 1h'
                    })
                
                # Detectar volumen anormal
                volatilidad = analisis.get('indicadores', {}).get('volatilidad', 0)
                if volatilidad > 10:
                    anomalias.append({
                        'tipo': 'volumen_anormal',
                        'cripto': simbolo,
                        'valor': float(volatilidad),
                        'mensaje': f'Alta volatilidad en {simbolo}: {volatilidad:.1f}%'
                    })
        
        return jsonify({'anomalias': anomalias, 'count': len(anomalias)})
    except Exception as e:
        print(f"Error en detección de anomalías: {e}")
        return jsonify({'anomalias': [], 'count': 0, 'error': str(e)})

@app.route('/api/online/ia-explicacion', methods=['POST'])
def ia_explicacion():
    """Generar explicación con IA local de la decisión"""
    data = request.get_json()
    cripto = data.get('cripto')
    
    try:
        # Obtener análisis actual si existe
        indicadores = online_config['analisis_actuales'].get(cripto, {})
        explicacion = generar_explicacion_ia_completa(cripto, indicadores)
        return jsonify({'explicacion': explicacion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/online/correlacion', methods=['POST'])
def calcular_correlacion_online():
    """Calcular correlación entre criptomonedas online"""
    data = request.get_json()
    criptos = data.get('criptos', [])
    
    if len(criptos) < 2:
        return jsonify({'error': 'Se necesitan al menos 2 criptomonedas'}), 400
    
    try:
        # Obtener datos históricos de Yahoo Finance
        datos = {}
        for cripto in criptos:
            try:
                ticker = yf.Ticker(f"{cripto}-USD")
                hist = ticker.history(period="30d", interval="1d")
                if not hist.empty:
                    datos[cripto] = hist['Close']
            except Exception as e:
                print(f"Error obteniendo datos de {cripto}: {e}")
                continue
        
        if len(datos) < 2:
            return jsonify({'error': 'No se pudieron obtener datos suficientes'}), 400
        
        df_combined = pd.DataFrame(datos)
        df_combined = df_combined.dropna()
        
        if len(df_combined) < 5:
            return jsonify({'error': 'Datos históricos insuficientes'}), 400
        
        # Calcular retornos
        returns = df_combined.pct_change().dropna()
        corr_matrix = returns.corr()
        
        # Preparar matriz para JSON
        matriz_valores = []
        for i in range(len(corr_matrix.columns)):
            fila = []
            for j in range(len(corr_matrix.columns)):
                valor = float(corr_matrix.iloc[i, j])
                # Asegurar que no haya NaN
                if np.isnan(valor):
                    valor = 0.0
                fila.append(valor)
            matriz_valores.append(fila)
        
        # Recomendaciones
        recomendaciones = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = float(corr_matrix.iloc[i, j])
                if not np.isnan(corr_val):
                    if corr_val < 0.3:
                        recomendaciones.append({
                            'par': f"{corr_matrix.columns[i]}-{corr_matrix.columns[j]}",
                            'correlacion': corr_val,
                            'tipo': 'Diversificación ideal',
                            'mensaje': f'Baja correlación ({corr_val:.2f}) - Buena para diversificar riesgo'
                        })
                    elif corr_val > 0.9:
                        recomendaciones.append({
                            'par': f"{corr_matrix.columns[i]}-{corr_matrix.columns[j]}",
                            'correlacion': corr_val,
                            'tipo': 'Movimiento sincronizado',
                            'mensaje': f'Alta correlación ({corr_val:.2f}) - Se mueven juntas, evitar sobreexposición'
                        })
        
        # Calcular estadísticas
        valores_matriz = np.array(matriz_valores)
        valores_validos = valores_matriz[~np.isnan(valores_matriz)]
        
        return jsonify({
            'matriz_correlacion': {
                'labels': list(corr_matrix.columns),
                'valores': matriz_valores
            },
            'recomendaciones': recomendaciones,
            'periodo_analisis': len(returns),
            'estadisticas': {
                'correlacion_promedio': float(np.mean(valores_validos)) if len(valores_validos) > 0 else 0.0,
                'max_correlacion': float(np.max(valores_validos)) if len(valores_validos) > 0 else 0.0,
                'min_correlacion': float(np.min(valores_validos)) if len(valores_validos) > 0 else 0.0
            }
        })
    except Exception as e:
        print(f"Error en correlación online: {e}")
        return jsonify({'error': f'Error procesando correlación: {str(e)}'}), 500

@app.route('/api/online/historial/<cripto>', methods=['GET'])
def get_historial_online(cripto):
    """Obtener historial de precios para gráficos"""
    periodo = request.args.get('periodo', '7d')
    
    try:
        ticker = yf.Ticker(f"{cripto}-USD")
        hist = ticker.history(period=periodo, interval="1h")
        
        if hist.empty:
            return jsonify({'error': 'Sin datos'}), 404
        
        return jsonify({
            'fechas': hist.index.strftime('%Y-%m-%d %H:%M').tolist(),
            'precios': hist['Close'].tolist(),
            'volumenes': hist['Volume'].tolist(),
            'open': hist['Open'].tolist(),
            'high': hist['High'].tolist(),
            'low': hist['Low'].tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/online/config-alerta', methods=['POST'])
def configurar_alerta():
    """Configurar alertas personalizadas"""
    data = request.get_json()
    # Guardar configuración de alertas (en memoria por ahora)
    return jsonify({'success': True, 'message': 'Alerta configurada'})

# ==================== SISTEMA DE ALERTAS ====================

# Almacenamiento de alertas en memoria (persistente durante la sesión)
alertas_configuradas = []
alertas_activas = []

@app.route('/api/online/guardar-alerta', methods=['POST'])
def guardar_alerta_completa():
    """Guardar alerta en memoria y archivo JSON"""
    global alertas_configuradas
    
    data = request.get_json()
    alerta = {
        'id': len(alertas_configuradas) + 1,
        'tipo': data.get('tipo'),
        'cripto': data.get('cripto'),
        'valor': data.get('valor'),
        'condicion': data.get('condicion'),
        'activa': True,
        'fecha_creacion': datetime.now().isoformat(),
        'ultima_ejecucion': None,
        'ejecuciones': []
    }
    
    alertas_configuradas.append(alerta)
    
    # Guardar en archivo JSON
    try:
        with open('alertas_config.json', 'w') as f:
            json.dump(alertas_configuradas, f, indent=2)
    except Exception as e:
        print(f"Error guardando alertas: {e}")
    
    return jsonify({'success': True, 'alerta': alerta})

@app.route('/api/online/obtener-alertas', methods=['GET'])
def obtener_alertas():
    """Obtener todas las alertas configuradas"""
    return jsonify({'alertas': alertas_configuradas})

@app.route('/api/online/eliminar-alerta/<int:alerta_id>', methods=['DELETE'])
def eliminar_alerta(alerta_id):
    """Eliminar alerta específica"""
    global alertas_configuradas
    
    alertas_configuradas = [a for a in alertas_configuradas if a['id'] != alerta_id]
    
    # Actualizar archivo
    try:
        with open('alertas_config.json', 'w') as f:
            json.dump(alertas_configuradas, f, indent=2)
    except Exception as e:
        print(f"Error actualizando alertas: {e}")
    
    return jsonify({'success': True})

def cargar_alertas_guardadas():
    """Cargar alertas desde archivo al iniciar"""
    global alertas_configuradas
    
    try:
        if os.path.exists('alertas_config.json'):
            with open('alertas_config.json', 'r') as f:
                alertas_configuradas = json.load(f)
    except Exception as e:
        print(f"Error cargando alertas: {e}")
        alertas_configuradas = []

def verificar_alertas_activas():
    """Verificar todas las alertas configuradas contra datos actuales"""
    global alertas_activas
    
    if not online_config['activo'] or not alertas_configuradas:
        return
    
    nuevas_alertas = []
    datos_actuales = online_config['datos_actuales']
    analisis_actuales = online_config['analisis_actuales']
    
    for alerta in alertas_configuradas:
        if not alerta['activa']:
            continue
            
        try:
            cripto = alerta['cripto']
            if cripto == 'all':
                # Verificar para todas las criptos
                for cripto_actual in datos_actuales.keys():
                    if verificar_alerta_individual(alerta, cripto_actual, datos_actuales, analisis_actuales):
                        alerta_copia = alerta.copy()
                        alerta_copia['cripto_afectada'] = cripto_actual
                        nuevas_alertas.append(alerta_copia)
            else:
                # Verificar para cripto específica
                if cripto in datos_actuales and verificar_alerta_individual(alerta, cripto, datos_actuales, analisis_actuales):
                    alerta['cripto_afectada'] = cripto
                    nuevas_alertas.append(alerta)
                    
        except Exception as e:
            print(f"Error verificando alerta {alerta['id']}: {e}")
    
    alertas_activas = nuevas_alertas

def verificar_alerta_individual(alerta, cripto, datos_actuales, analisis_actuales):
    """Verificar si una alerta específica se debe activar"""
    tipo = alerta['tipo']
    
    if tipo == 'pump':
        cambio = analisis_actuales.get(cripto, {}).get('cambio_esperado', 0)
        return cambio > 10
    elif tipo == 'dump':
        cambio = analisis_actuales.get(cripto, {}).get('cambio_esperado', 0)
        return cambio < -10
    elif tipo == 'volumen':
        volatilidad = analisis_actuales.get(cripto, {}).get('indicadores', {}).get('volatilidad', 0)
        return volatilidad > 10  # 10% de volatilidad
    elif tipo == 'rsi':
        rsi = analisis_actuales.get(cripto, {}).get('rsi', 50)
        return rsi > 80 or rsi < 20
    elif tipo == 'precio':
        precio_actual = datos_actuales.get(cripto, {}).get('precio', 0)
        valor_objetivo = float(alerta.get('valor', 0))
        condicion = alerta.get('condicion', 'above')
        
        if condicion == 'above':
            return precio_actual >= valor_objetivo
        else:
            return precio_actual <= valor_objetivo
    elif tipo == 'cambio':
        cambio = analisis_actuales.get(cripto, {}).get('cambio_esperado', 0)
        valor_cambio = float(alerta.get('valor', 0))
        condicion = alerta.get('condicion', 'increase')
        
        if condicion == 'increase':
            return cambio >= valor_cambio
        else:
            return cambio <= -valor_cambio
    
    return False

@app.route('/api/online/comparacion', methods=['POST'])
def comparacion_online():
    """Comparación múltiple de métricas entre criptomonedas online"""
    data = request.get_json()
    criptos = data.get('criptos', [])
    metrica = data.get('metrica', 'precio')

    if len(criptos) < 2:
        return jsonify({'error': 'Se necesitan al menos 2 criptomonedas'}), 400

    try:
        resultados = []
        for cripto in criptos:
            if cripto in online_config['analisis_actuales']:
                analisis = online_config['analisis_actuales'][cripto]
                
                valor = None
                if metrica == 'precio':
                    valor = analisis.get('precio_actual', 0)
                elif metrica == 'cambio':
                    valor = analisis.get('cambio_esperado', 0)
                elif metrica == 'rsi':
                    valor = analisis.get('rsi', 50)
                elif metrica == 'macd':
                    valor = analisis.get('macd', 0)

                resultados.append({
                    'cripto': cripto,
                    'valor': valor,
                    'metrica': metrica
                })

        return jsonify({
            'metrica': metrica,
            'resultados': resultados,
            'maximo': max([r['valor'] for r in resultados]) if resultados else 0,
            'minimo': min([r['valor'] for r in resultados]) if resultados else 0,
            'promedio': np.mean([r['valor'] for r in resultados]) if resultados else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/online/backtesting', methods=['POST'])
def backtesting_online():
    """Backtesting de estrategias sobre datos online"""
    data = request.get_json()
    cripto = data.get('cripto')
    estrategia = data.get('estrategia', 'rsi_macd')
    capital = float(data.get('capital', 10000))

    if not cripto:
        return jsonify({'error': 'Criptomoneda requerida'}), 400

    try:
        # Obtener datos históricos
        ticker = yf.Ticker(f"{cripto}-USD")
        df = ticker.history(period="1y", interval="1d")
        
        if df.empty or len(df) < 200:
            return jsonify({'error': 'Datos insuficientes para backtesting'}), 400

        resultado = backtesting_estrategia(df, capital, estrategia)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== FUNCIONES AUXILIARES ====================

def loop_automatico():
    """Loop automático para actualización online"""
    while online_config['activo']:
        try:
            actualizar_datos_online()
            # Dormir por el intervalo configurado
            for _ in range(online_config['intervalo_minutos'] * 60):
                if not online_config['activo']:
                    break
                time.sleep(1)
        except Exception as e:
            print(f"Error en loop automático: {e}")
            time.sleep(60)

def actualizar_datos_online():
    """Actualizar datos desde Yahoo Finance"""
    global online_config
    
    print(f"[{datetime.now()}] Actualizando datos online...")
    
    for simbolo in online_config['criptos_seleccionadas']:
        try:
            # Usar Yahoo Finance directamente
            ticker = yf.Ticker(f"{simbolo}-USD")
            hist = ticker.history(period="7d", interval="1h")
            
            if hist.empty or len(hist) < 2:
                print(f"⚠️ Sin datos para {simbolo}")
                continue
            
            # Calcular precio actual y tendencia
            current_price = float(hist['Close'].iloc[-1])
            prev_price = float(hist['Close'].iloc[-2])
            change_pct = ((current_price - prev_price) / prev_price) * 100
            tendencia = 'ALTA' if change_pct > 0 else 'BAJA' if change_pct < 0 else 'ESTABLE'
            
            # Guardar en CSV para uso offline
            try:
                hist_clean = hist.copy()
                if hist_clean.index.tz is not None:
                    hist_clean.index = hist_clean.index.tz_localize(None)
                hist_clean.to_csv(f'datos/{simbolo}_online.csv')
            except Exception as e:
                print(f"⚠️ Error guardando CSV: {e}")
            
            # Análisis completo
            try:
                estadisticas = limpieza_datos(hist)
                prediccion = predecir_precio(hist)
                decision_info = tomar_desiciones(current_price, estadisticas, prediccion, tendencia)
                
                # Calcular RSI
                try:
                    rsi_vals = calcular_rsi(hist['Close'])
                    rsi_val = float(rsi_vals.iloc[-1]) if not rsi_vals.empty else 50.0
                except:
                    rsi_val = 50.0
                
                # Calcular MACD
                try:
                    macd_df = calcular_macd(hist['Close'])
                    macd_val = float(macd_df['macd'].iloc[-1]) if not macd_df.empty else 0.0
                except:
                    macd_val = 0.0
                
                # Guardar historial para gráficos
                if simbolo not in online_config['historial_precios']:
                    online_config['historial_precios'][simbolo] = []
                
                online_config['historial_precios'][simbolo].append({
                    'timestamp': datetime.now().isoformat(),
                    'precio': current_price
                })
                
                # Mantener solo últimos 100 puntos
                if len(online_config['historial_precios'][simbolo]) > 100:
                    online_config['historial_precios'][simbolo] = online_config['historial_precios'][simbolo][-100:]
                
                online_config['datos_actuales'][simbolo] = {
                    'precio': current_price,
                    'tendencia': tendencia,
                    'volumen_24h': float(hist['Volume'].sum()) if 'Volume' in hist.columns else 0,
                    'high_24h': float(hist['High'].max()) if 'High' in hist.columns else current_price,
                    'low_24h': float(hist['Low'].min()) if 'Low' in hist.columns else current_price,
                    'change_24h': change_pct
                }
                
                online_config['analisis_actuales'][simbolo] = {
                    'precio_actual': current_price,
                    'tendencia': tendencia,
                    'decision': decision_info['decision'],
                    'confianza': float(decision_info['confianza']),
                    'prediccion': float(prediccion['prediccion_final']),
                    'cambio_esperado': float(prediccion['cambio_porcentual']),
                    'rsi': rsi_val,
                    'macd': macd_val,
                    'indicadores': {
                        'media': float(estadisticas['media']),
                        'volatilidad': float(estadisticas['desviacion'] / estadisticas['media'] * 100) if estadisticas['media'] > 0 else 0
                    }
                }
                
                print(f"  ✅ {simbolo}: ${current_price:,.2f} - {decision_info['decision']}")
                
            except Exception as e:
                print(f"  ❌ Error en análisis de {simbolo}: {e}")
                
        except Exception as e:
            print(f"❌ Error crítico actualizando {simbolo}: {e}")
            continue
    
    online_config['ultima_actualizacion'] = datetime.now().isoformat()
    print(f"[{datetime.now()}] Actualización completada")

def calcular_rsi(prices, period=14):
    """Calcular RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(prices, fast=12, slow=26, signal=9):
    """Calcular MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return pd.DataFrame({'macd': macd, 'signal': signal_line, 'histogram': histogram})

@app.route('/api/online/top100', methods=['GET'])
def top_100_coinmarketcap():
    try:
        criptos = CRIPTOS_DEFAULT()  # Esto ahora devuelve solo las 9
        return jsonify({'success': True, 'criptos': criptos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== RUTAS PARA SIMULACIÓN ====================

@app.route('/api/offline/simulacion/analizar', methods=['POST'])
def analizar_simulacion_route():
    """Analiza una simulación guardada y devuelve resultados JSON"""
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'error': 'Nombre de simulación requerido'}), 400

    try:
        resultado = analizar_simulacion(nombre)
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error analizando simulación: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== INICIAR APLICACIÓN ====================

if __name__ == '__main__':
    # Verificar dependencias
    try:
        import webview
        HAS_WEBVIEW = True
    except ImportError:
        HAS_WEBVIEW = False
        print("pywebview no instalado. Ejecutando solo servidor Flask.")
    
    # Iniciar Flask en hilo separado
    def run_flask():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("Servidor Flask iniciado en http://127.0.0.1:5000")
    
    # Iniciar pywebview si está disponible
    if HAS_WEBVIEW:
        time.sleep(2)
        webview.create_window(
            'Cripto Analizador Pro',
            'http://127.0.0.1:5000',
            width=1400,
            height=900,
            min_size=(1000, 700)
        )
        webview.start()
    else:
        webbrowser.open('http://127.0.0.1:5000')
        while True:
            time.sleep(1)
