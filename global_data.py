# global_data.py - Configuraciones globales (VERSIÓN COMPLETA CON TODAS LAS FUNCIONALIDADES)

# Configuración de User-Agent para web scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Headers HTTP estándar
HTTP_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Criptomonedas soportadas por defecto (Top 100 de CoinMarketCap)
from funciones import obtener_top_100_coinmarketcap

def CRIPTOS_DEFAULT():
    """
    Devuelve la lista específica de 9 criptomonedas predeterminadas.
    """
    return ['ADA', 'BNB', 'BTC', 'DOGE', 'DOT', 'ETH', 'SOL', 'XRP', 'USDT']

# Actualizar también CRIPTOS_NOMBRES con solo estas 9:
CRIPTOS_NOMBRES = {
    'ADA': 'Cardano',
    'BNB': 'Binance Coin', 
    'BTC': 'Bitcoin',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
    'ETH': 'Ethereum',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'USDT': 'Tether'
}

# Configuraciones de análisis
CONFIG_ANALISIS = {
    'rsi_periodo': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_periodo': 20,
    'bollinger_std': 2,
    'sma_corto': 7,
    'sma_medio': 14,
    'sma_largo': 30,
    'atr_periodo': 14,
    'estocastico_k': 14,
    'estocastico_d': 3
}

# Umbrales de decisión
UMBRALES_DECISION = {
    'compra_fuerte': 0.3,
    'compra': 0.1,
    'venta_fuerte': -0.3,
    'venta': -0.1,
    'rsi_sobrecompra': 70,
    'rsi_sobreventa': 30,
    'volatilidad_alta': 0.05,
    'volatilidad_baja': 0.02,
    'estocastico_sobrecompra': 80,
    'estocastico_sobreventa': 20
}

# Colores para gráficos
COLORES_GRAFICOS = {
    'precio': '#2196F3',
    'compra': '#4CAF50',
    'venta': '#F44336',
    'mantener': '#FFC107',
    'prediccion': '#9C27B0',
    'media': '#FF9800',
    'bollinger_upper': 'rgba(255, 152, 0, 0.3)',
    'bollinger_lower': 'rgba(255, 152, 0, 0.3)',
    'volumen': 'rgba(33, 150, 243, 0.5)',
    'rsi': '#9C27B0',
    'macd': '#2196F3',
    'signal': '#FF9800',
    'histograma_positivo': 'rgba(76, 175, 80, 0.5)',
    'histograma_negativo': 'rgba(244, 67, 54, 0.5)'
}

# Mensajes educativos expandidos
MENSAJES_EDUCATIVOS = {
    'rsi': {
        'titulo': 'RSI (Relative Strength Index)',
        'descripcion': 'Indicador de momentum que mide la velocidad y cambio de los movimientos de precio.',
        'uso': 'Identifica condiciones de sobrecompra (>70) y sobreventa (<30).',
        'niveles': {
            '0-30': 'Zona de sobreventa - posible rebote',
            '30-50': 'Zona bajista débil',
            '50': 'Nivel neutral',
            '50-70': 'Zona alcista débil',
            '70-100': 'Zona de sobrecompra - posible corrección'
        }
    },
    'macd': {
        'titulo': 'MACD',
        'descripcion': 'Convergence Divergence de Medias Móviles. Muestra la relación entre dos EMAs.',
        'uso': 'Señales de compra/venta cuando el MACD cruza la línea de señal.',
        'componentes': {
            'linea_macd': 'Diferencia entre EMA 12 y EMA 26',
            'linea_señal': 'EMA 9 de la línea MACD',
            'histograma': 'Diferencia entre MACD y señal'
        }
    },
    'bollinger': {
        'titulo': 'Bandas de Bollinger',
        'descripcion': 'Bandas de volatilidad colocadas encima y debajo de una media móvil.',
        'uso': 'El precio tiende a volver a la banda media; bandas estrechas anticipan movimientos fuertes.',
        'interpretacion': {
            'squeeze': 'Bandas estrechas = baja volatilidad, preparándose para movimiento',
            'expansion': 'Bandas amplias = alta volatilidad',
            'toque_banda': 'Toque de banda superior/inferior = posible reversión'
        }
    },
    'volumen': {
        'titulo': 'Volumen',
        'descripcion': 'Cantidad de activos negociados en un período.',
        'uso': 'Confirma la fuerza de una tendencia. Aumento de volumen + subida de precio = tendencia fuerte.',
        'patrones': {
            'volumen_creciente': 'Confirma tendencia actual',
            'volumen_decreciente': 'Debilitamiento de tendencia',
            'pico_volumen': 'Posible punto de inflexión'
        }
    },
    'medias_moviles': {
        'titulo': 'Medias Móviles',
        'descripcion': 'Promedio de precios en un período específico.',
        'uso': 'Identifican tendencia y soportes/resistencias dinámicos.',
        'tipos': {
            'sma': 'Media Móvil Simple - igual peso para todos los datos',
            'ema': 'Media Móvil Exponencial - más peso a datos recientes'
        }
    },
    'estocastico': {
        'titulo': 'Estocástico',
        'descripcion': 'Compara el precio de cierre con el rango de precios en un período.',
        'uso': 'Identifica condiciones de sobrecompra/sobreventa y divergencias.'
    },
    'atr': {
        'titulo': 'ATR',
        'descripcion': 'Average True Range - mide la volatilidad promedio.',
        'uso': 'Ajustar stop-loss dinámicos según la volatilidad del mercado.'
    },
    'fibonacci': {
        'titulo': 'Retrocesos de Fibonacci',
        'descripcion': 'Niveles basados en la secuencia de Fibonacci.',
        'uso': 'Identifican zonas potenciales de soporte y resistencia.',
        'niveles_clave': ['38.2%', '50%', '61.8%']
    },
    'ichimoku': {
        'titulo': 'Ichimoku Cloud',
        'descripcion': 'Sistema completo de análisis técnico japonés.',
        'uso': 'Proporciona información sobre tendencia, momentum, soporte y resistencia.'
    },
    'adx': {
        'titulo': 'ADX',
        'descripcion': 'Average Directional Index - mide la fuerza de la tendencia.',
        'uso': 'Determina si el mercado está en tendencia o en rango.',
        'niveles': {
            '0-20': 'Tendencia débil o inexistente',
            '20-40': 'Tendencia fuerte',
            '40+': 'Tendencia muy fuerte'
        }
    },
    'obv': {
        'titulo': 'OBV',
        'descripcion': 'On-Balance Volume - acumulación de volumen.',
        'uso': 'Confirma tendencias mediante el flujo de volumen.'
    }
}

# Configuraciones de simulación
CONFIG_SIMULACION = {
    'precio_minimo': 0.0001,
    'precio_maximo': 1000000,
    'dias_minimo': 30,
    'dias_maximo': 365,
    'volatilidad_minima': 0.001,
    'volatilidad_maxima': 0.1
}

# Tipos de alertas soportadas
TIPOS_ALERTAS = {
    'pump': {'nombre': 'Pump Detection', 'descripcion': 'Detecta subidas >10% en 1h'},
    'dump': {'nombre': 'Dump Detection', 'descripcion': 'Detecta bajadas <-10% en 1h'},
    'volumen': {'nombre': 'Volumen Anormal', 'descripcion': 'Volumen >3x el promedio'},
    'rsi': {'nombre': 'RSI Extremo', 'descripcion': 'RSI >80 o <20'},
    'precio': {'nombre': 'Precio Objetivo', 'descripcion': 'Alcanza precio específico'},
    'cambio': {'nombre': 'Cambio Porcentual', 'descripcion': 'Cambio % específico'}
}

# Configuración de temas
TEMAS = {
    'oscuro': {
        'bg_dark': '#0f172a',
        'bg_card': '#1e293b',
        'bg_sidebar': '#1e293b',
        'text_primary': '#f1f5f9',
        'text_secondary': '#94a3b8',
        'border_color': '#334155',
        'primary_color': '#2196F3',
        'success_color': '#4CAF50',
        'danger_color': '#F44336',
        'warning_color': '#FFC107'
    },
    'claro': {
        'bg_dark': '#ffffff',
        'bg_card': '#f8fafc',
        'bg_sidebar': '#e2e8f0',
        'text_primary': '#1e293b',
        'text_secondary': '#64748b',
        'border_color': '#cbd5e1',
        'primary_color': '#2563eb',
        'success_color': '#16a34a',
        'danger_color': '#dc2626',
        'warning_color': '#f59e0b'
    }
}

# Idiomas soportados
IDIOMAS = {
    'es': {
        'titulo_app': 'Cripto Analizador Pro',
        'modo_online': 'Modo Online',
        'modo_offline': 'Modo Offline',
        'dashboard': 'Dashboard',
        'graficos': 'Gráficos',
        'analisis': 'Análisis',
        'alertas': 'Alertas',
        'sentimiento': 'Sentimiento',
        'ia_explicativa': 'IA Explicativa',
        'correlacion': 'Correlación',
        'backtesting': 'Backtesting',
        'comparacion': 'Comparación',
        'sandbox': 'Sandbox Educativo',
        'simulacion': 'Simulación',
        'gestion_datos': 'Gestión de Datos',
        'exportar': 'Exportar',
        'configuracion': 'Configuración',
        'tema': 'Tema',
        'idioma': 'Idioma',
        'tema_claro': 'Claro',
        'tema_oscuro': 'Oscuro',
        'espanol': 'Español',
        'ingles': 'English',
        'precio_actual': 'Precio Actual',
        'tendencia': 'Tendencia',
        'decision': 'Decisión',
        'confianza': 'Confianza',
        'prediccion_24h': 'Predicción 24h',
        'rsi': 'RSI',
        'macd': 'MACD',
        'volumen': 'Volumen',
        'capital_inicial': 'Capital Inicial',
        'capital_final': 'Capital Final',
        'retorno_total': 'Retorno Total',
        'buy_and_hold': 'Buy & Hold',
        'max_drawdown': 'Max Drawdown',
        'operaciones': 'Operaciones',
        'ganadoras': 'Ganadoras',
        'perdedoras': 'Perdedoras',
        'compra': 'Compra',
        'venta': 'Venta',
        'mantener': 'Mantener',
        'alcista': 'Alcista',
        'bajista': 'Bajista',
        'neutral': 'Neutral',
        'sobrecompra': 'Sobrecompra',
        'sobreventa': 'Sobreventa',
        'volatilidad': 'Volatilidad',
        'momento': 'Momento',
        'sentimiento': 'Sentimiento',
        'correlacion': 'Correlación',
        'backtesting': 'Backtesting',
        'comparacion_multiple': 'Comparación Múltiple',
        'grafico_velas': 'Gráfico de Velas',
        'grafico_linea': 'Gráfico de Línea',
        'grafico_barras': 'Gráfico de Barras',
        'grafico_area': 'Gráfico de Área',
        'grafico_dispersion': 'Gráfico de Dispersión',
        'exportar_imagen': 'Exportar Imagen',
        'exportar_pdf': 'Exportar PDF',
        'exportar_csv': 'Exportar CSV',
        'exportar_json': 'Exportar JSON',
        'alerta_configurada': 'Alerta configurada correctamente',
        'error_alerta': 'Error al configurar alerta',
        'datos_actualizados': 'Datos actualizados',
        'error_datos': 'Error al actualizar datos',
        'simulacion_generada': 'Simulación generada',
        'error_simulacion': 'Error al generar simulación',
        'archivo_subido': 'Archivo subido correctamente',
        'error_archivo': 'Error al subir archivo',
        'cripto_eliminada': 'Criptomoneda eliminada',
        'error_eliminar': 'Error al eliminar criptomoneda',
        'backtesting_completado': 'Backtesting completado',
        'error_backtesting': 'Error en backtesting',
        'comparacion_generada': 'Comparación generada',
        'error_comparacion': 'Error al generar comparación',
        'idioma_cambiado': 'Idioma cambiado',
        'tema_cambiado': 'Tema cambiado',
        'configuracion_guardada': 'Configuración guardada',
        'error_configuracion': 'Error al guardar configuración'
    },
    'en': {
        'titulo_app': 'Crypto Analyzer Pro',
        'modo_online': 'Online Mode',
        'modo_offline': 'Offline Mode',
        'dashboard': 'Dashboard',
        'graficos': 'Charts',
        'analisis': 'Analysis',
        'alertas': 'Alerts',
        'sentimiento': 'Sentiment',
        'ia_explicativa': 'AI Explanation',
        'correlacion': 'Correlation',
        'backtesting': 'Backtesting',
        'comparacion': 'Comparison',
        'sandbox': 'Educational Sandbox',
        'simulacion': 'Simulation',
        'gestion_datos': 'Data Management',
        'exportar': 'Export',
        'configuracion': 'Settings',
        'tema': 'Theme',
        'idioma': 'Language',
        'tema_claro': 'Light',
        'tema_oscuro': 'Dark',
        'espanol': 'Spanish',
        'ingles': 'English',
        'precio_actual': 'Current Price',
        'tendencia': 'Trend',
        'decision': 'Decision',
        'confianza': 'Confidence',
        'prediccion_24h': '24h Prediction',
        'rsi': 'RSI',
        'macd': 'MACD',
        'volumen': 'Volume',
        'capital_inicial': 'Initial Capital',
        'capital_final': 'Final Capital',
        'retorno_total': 'Total Return',
        'buy_and_hold': 'Buy & Hold',
        'max_drawdown': 'Max Drawdown',
        'operaciones': 'Operations',
        'ganadoras': 'Winners',
        'perdedoras': 'Losers',
        'compra': 'Buy',
        'venta': 'Sell',
        'mantener': 'Hold',
        'alcista': 'Bullish',
        'bajista': 'Bearish',
        'neutral': 'Neutral',
        'sobrecompra': 'Overbought',
        'sobreventa': 'Oversold',
        'volatilidad': 'Volatility',
        'momento': 'Momentum',
        'sentimiento': 'Sentiment',
        'correlacion': 'Correlation',
        'backtesting': 'Backtesting',
        'comparacion_multiple': 'Multiple Comparison',
        'grafico_velas': 'Candlestick Chart',
        'grafico_linea': 'Line Chart',
        'grafico_barras': 'Bar Chart',
        'grafico_area': 'Area Chart',
        'grafico_dispersion': 'Scatter Chart',
        'exportar_imagen': 'Export Image',
        'exportar_pdf': 'Export PDF',
        'exportar_csv': 'Export CSV',
        'exportar_json': 'Export JSON',
        'alerta_configurada': 'Alert configured successfully',
        'error_alerta': 'Error configuring alert',
        'datos_actualizados': 'Data updated',
        'error_datos': 'Error updating data',
        'simulacion_generada': 'Simulation generated',
        'error_simulacion': 'Error generating simulation',
        'archivo_subido': 'File uploaded successfully',
        'error_archivo': 'Error uploading file',
        'cripto_eliminada': 'Cryptocurrency deleted',
        'error_eliminar': 'Error deleting cryptocurrency',
        'backtesting_completado': 'Backtesting completed',
        'error_backtesting': 'Backtesting error',
        'comparacion_generada': 'Comparison generated',
        'error_comparacion': 'Error generating comparison',
        'idioma_cambiado': 'Language changed',
        'tema_cambiado': 'Theme changed',
        'configuracion_guardada': 'Settings saved',
        'error_configuracion': 'Error saving settings'
    }
}

# Configuración de exportación
CONFIG_EXPORTAR = {
    'formatos_soportados': ['png', 'svg', 'pdf', 'csv', 'json', 'html'],
    'calidad_imagen': 300,
    'ancho_imagen': 1920,
    'alto_imagen': 1080,
    'fondo_transparente': True
}

# Configuración de gráficos
CONFIG_GRAFICOS = {
    'temas': {
        'oscuro': {
            'fondo': '#0f172a',
            'texto': '#f1f5f9',
            'grid': '#334155',
            'colores': ['#2196F3', '#4CAF50', '#F44336', '#FFC107', '#9C27B0', '#00BCD4']
        },
        'claro': {
            'fondo': '#ffffff',
            'texto': '#1e293b',
            'grid': '#e2e8f0',
            'colores': ['#2563eb', '#16a34a', '#dc2626', '#f59e0b', '#9333ea', '#0891b2']
        }
    },
    'tipos_grafico': {
        'linea': {'soportado': True, 'animacion': True},
        'velas': {'soportado': True, 'animacion': False},
        'barras': {'soportado': True, 'animacion': True},
        'area': {'soportado': True, 'animacion': True},
        'dispersion': {'soportado': True, 'animacion': True},
        'dona': {'soportado': True, 'animacion': True},
        'circular': {'soportado': True, 'animacion': True},
        'radar': {'soportado': True, 'animacion': True},
        'heatmap': {'soportado': True, 'animacion': False}
    }
}

# Configuración de alertas
CONFIG_ALERTAS = {
    'tipos': {
        'pump': {'umbral': 10, 'color': '#4CAF50', 'icono': 'fas fa-arrow-up'},
        'dump': {'umbral': -10, 'color': '#F44336', 'icono': 'fas fa-arrow-down'},
        'volumen': {'multiplicador': 3, 'color': '#FFC107', 'icono': 'fas fa-chart-bar'},
        'rsi': {'sobrecompra': 80, 'sobreventa': 20, 'color': '#9C27B0', 'icono': 'fas fa-tachometer-alt'},
        'precio': {'color': '#2196F3', 'icono': 'fas fa-dollar-sign'},
        'cambio': {'color': '#00BCD4', 'icono': 'fas fa-percentage'}
    },
    'sonidos': {
        'pump': 'alerta_pump.mp3',
        'dump': 'alerta_dump.mp3',
        'volumen': 'alerta_volumen.mp3',
        'rsi': 'alerta_rsi.mp3',
        'precio': 'alerta_precio.mp3',
        'cambio': 'alerta_cambio.mp3'
    },
    'notificaciones': {
        'desktop': True,
        'sonido': True,
        'email': False,
        'webhook': False
    }
}

# Configuración de simulación de Monte Carlo
CONFIG_MONTECARLO = {
    'iteraciones': 1000,
    'confianza': 0.95,
    'distribuciones': ['normal', 'lognormal', 'uniforme', 'exponencial'],
    'semilla': None  # None = aleatorio
}

# Configuración de backtesting
CONFIG_BACKTESTING = {
    'estrategias': {
        'rsi_macd': {'nombre': 'RSI + MACD', 'descripcion': 'Combinación de RSI y MACD'},
        'bollinger': {'nombre': 'Bollinger Bands', 'descripcion': 'Bandas de Bollinger'},
        'golden_cross': {'nombre': 'Golden Cross', 'descripcion': 'Cruce dorado SMA50/200'},
        'estocastico': {'nombre': 'Estocástico', 'descripcion': 'Oscilador estocástico'},
        'adx': {'nombre': 'ADX', 'descripcion': 'Average Directional Index'},
        'ichimoku': {'nombre': 'Ichimoku', 'descripcion': 'Sistema Ichimoku Cloud'}
    },
    'comisiones': {
        'maker': 0.001,
        'taker': 0.001
    },
    'slippage': 0.0005,
    'minimo_operaciones': 5
}

# Configuración de IA explicativa
CONFIG_IA = {
    'modelos': {
        'basico': {'profundidad': 'simple', 'tokens': 500},
        'intermedio': {'profundidad': 'medio', 'tokens': 1000},
        'avanzado': {'profundidad': 'completo', 'tokens': 2000}
    },
    'idiomas': ['es', 'en'],
    'estilos': ['tecnico', 'educativo', 'simple']
}

# Configuración de comparación múltiple
CONFIG_COMPARACION = {
    'metricas': {
        'precio': {'nombre': 'Precio', 'unidad': '$', 'tipo': 'moneda'},
        'cambio': {'nombre': 'Cambio 24h', 'unidad': '%', 'tipo': 'porcentaje'},
        'volumen': {'nombre': 'Volumen', 'unidad': '$', 'tipo': 'moneda'},
        'rsi': {'nombre': 'RSI', 'unidad': '', 'tipo': 'indicador'},
        'macd': {'nombre': 'MACD', 'unidad': '', 'tipo': 'indicador'},
        'volatilidad': {'nombre': 'Volatilidad', 'unidad': '%', 'tipo': 'porcentaje'},
        'confianza': {'nombre': 'Confianza', 'unidad': '%', 'tipo': 'porcentaje'},
        'tendencia': {'nombre': 'Tendencia', 'unidad': '', 'tipo': 'texto'}
    },
    'tipos_grafico': ['barras', 'lineas', 'radar', 'heatmap'],
    'max_elementos': 10
}

# Configuración de velas japonesas
CONFIG_VELAS = {
    'colores': {
        'alcista': '#4CAF50',
        'bajista': '#F44336',
        'sombra': '#9E9E9E',
        'cuerpo': '#FFFFFF'
    },
    'estilos': {
        'sombra': {'grosor': 1, 'estilo': 'solido'},
        'cuerpo': {'grosor': 2, 'estilo': 'solido'}
    },
    'proporciones': {
        'ancho_cuerpo': 0.8,
        'ancho_sombra': 0.3,
        'espaciado': 0.1
    }
}

# Configuración de actualización en tiempo real
CONFIG_ACTUALIZACION = {
    'intervalo_minimo': 1,  # minutos
    'intervalo_maximo': 60,  # minutos
    'intervalo_por_defecto': 5,  # minutos
    'timeout': 30,  # segundos
    'reintentos': 3,
    'espera_reintento': 5  # segundos
}

# Configuración de exportación de gráficos
CONFIG_EXPORTAR_GRAFICOS = {
    'formatos': ['png', 'svg', 'pdf'],
    'calidad': {
        'png': {'dpi': 300, 'transparente': True},
        'svg': {'optimizado': True, 'editable': True},
        'pdf': {'vectorial': True, 'comprimido': True}
    },
    'dimensiones': {
        'ancho': 1920,
        'alto': 1080,
        'ratio': '16:9'
    },
    'nombre_archivo': 'grafico_{tipo}_{fecha}_{hora}'
}

# Configuración de temas dinámicos
CONFIG_TEMAS_DINAMICOS = {
    'paleta_colores': {
        'primarios': ['#2196F3', '#4CAF50', '#F44336', '#FFC107', '#9C27B0', '#00BCD4'],
        'secundarios': ['#1976D2', '#388E3C', '#D32F2F', '#FFA000', '#7B1FA2', '#0097A7'],
        'neutros': ['#9E9E9E', '#757575', '#616161', '#424242', '#212121'],
        'acentos': ['#FF5722', '#E91E63', '#673AB7', '#3F51B5', '#009688']
    },
    'transiciones': {
        'duracion': 300,  # ms
        'curva': 'ease-in-out',
        'propiedades': ['color', 'background-color', 'border-color']
    }
}

# Configuración de rendimiento
CONFIG_RENDIMIENTO = {
    'cache': {
        'habilitado': True,
        'duracion': 300,  # segundos
        'maximo_tamano': 100,  # MB
        'limpiar_auto': True
    },
    'compresion': {
        'habilitado': True,
        'nivel': 6,
        'tipos': ['gzip', 'deflate']
    },
    'lazy_loading': True,
    'precarga': {
        'habilitada': True,
        'tiempo_espera': 1000  # ms
    }
}

# Configuración de seguridad
CONFIG_SEGURIDAD = {
    'rate_limiting': {
        'habilitado': True,
        'maximo_peticiones': 100,
        'ventana_tiempo': 3600,  # segundos
        'excluir_rutas': ['/api/health', '/api/version']
    },
    'validacion_entrada': {
        'habilitada': True,
        'sanitizar': True,
        'maximo_tamano': 1048576,  # 1MB
        'tipos_archivo': ['csv', 'json', 'txt']
    },
    'encriptacion': {
        'habilitada': True,
        'algoritmo': 'AES-256-GCM',
        'rotacion_claves': 2592000  # 30 días en segundos
    }
}

# Configuración de monitoreo y análisis
CONFIG_MONITOREO = {
    'habilitado': True,
    'nivel': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'destinos': ['archivo', 'consola', 'sistema'],
    'metricas': {
        'tiempo_respuesta': True,
        'errores': True,
        'uso_memoria': True,
        'uso_cpu': True,
        'peticiones': True
    },
    'alertas_sistema': {
        'umbral_cpu': 80,  # %
        'umbral_memoria': 85,  # %
        'umbral_disco': 90,  # %
        'umbral_errores': 10  # por hora
    }
}