# 🚀 Cripto Analizador Pro

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-brightgreen?logo=python&logoColor=white)](https://pep8.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?logo=check-circle&logoColor=white)](https://github.com/tu-usuario/cripto-analizador-pro)

**Sistema profesional de análisis de criptomonedas** con capacidades avanzadas de trading, simulación Monte Carlo, backtesting y sandbox educativo integrado.

![Dashboard Preview](https://via.placeholder.com/800x400/2d3748/ffffff?text=Cripto+Analizador+Pro+Dashboard)

## 📋 Tabla de Contenidos
- [✨ Características](#-características)
- [🚀 Instalación Rápida](#-instalación-rápida)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🎮 Guía de Uso](#-guía-de-uso-paso-a-paso)
- [📊 API Endpoints](#-api-endpoints)
- [🎓 Sandbox Educativo](#-sandbox-educativo)
- [⚙️ Configuración Avanzada](#️-configuración-avanzada)
- [📄 Licencia](#-licencia)
- [⚠️ Descargo de Responsabilidad](#️-descargo-de-responsabilidad)

## ✨ Características

### 📈 **Análisis Técnico Avanzado**
![Criptos](https://img.shields.io/badge/9-Criptomonedas%20Soportadas-blueviolet?logo=bitcoin&logoColor=white)
![Indicadores](https://img.shields.io/badge/5%2B-Indicadores%20Técnicos-9cf?logo=chart-line&logoColor=white)
- **9 criptomonedas principales**: BTC, ETH, BNB, XRP, ADA, SOL, DOGE, DOT, USDT
- **Indicadores técnicos completos**: RSI, MACD, Bandas de Bollinger, EMA, SMA
- **Detección de tendencias** automática con análisis de soporte/resistencia
- **Predicción de precios** usando regresión lineal y aprendizaje automático

### 🎮 **Dos Modos de Operación**
![Online](https://img.shields.io/badge/MODO-ONLINE-success?logo=wifi&logoColor=white)
![Offline](https://img.shields.io/badge/MODO-OFFLINE-informational?logo=database&logoColor=white)
- **🔴 Modo Online**: Datos en tiempo real via Yahoo Finance
- **💾 Modo Offline**: Análisis de datos históricos desde archivos CSV
- **Cambio instantáneo** entre modos sin reiniciar la aplicación

### 🎯 **Simulaciones Profesionales**
![Monte Carlo](https://img.shields.io/badge/Simulación-Monte_Carlo-important?logo=dice&logoColor=white)
![Backtesting](https://img.shields.io/badge/Backtesting-Strategies-blue?logo=trending-up&logoColor=white)
- **Simulación Monte Carlo** con múltiples trayectorias de precios
- **Backtesting completo** de estrategias de trading personalizadas
- **Generación de datos sintéticos** realistas para testing

### 📊 **Visualización y Reportes**
![Export](https://img.shields.io/badge/Exportación-4_Formatos-9cf?logo=file-export&logoColor=white)
![Charts](https://img.shields.io/badge/Gráficos-Interactivos-yellow?logo=chart-bar&logoColor=white)
- **Gráficos interactivos** con Chart.js
- **Exportación profesional** a PDF, CSV, JSON y HTML
- **Dashboard ejecutivo** con métricas clave en tiempo real
- **Reportes corporativos** con diseño profesional

### 🎓 **Sandbox Educativo Integrado**
![Education](https://img.shields.io/badge/Sandbox-Educativo-brightgreen?logo=graduation-cap&logoColor=white)
![Cards](https://img.shields.io/badge/20%2B-Tarjetas%20Educativas-orange?logo=book&logoColor=white)
- **4 categorías educativas** completas
- **Tarjetas interactivas** con ejemplos prácticos
- **Explicaciones para principiantes** generadas por IA

### 🔔 **Sistema Inteligente de Alertas**
![Alerts](https://img.shields.io/badge/Alertas-Configurables-yellowgreen?logo=bell&logoColor=white)
![Persistent](https://img.shields.io/badge/Persistentes-JSON%20Storage-lightgrey?logo=save&logoColor=white)
- **Alertas configurables** por precio, volumen y tendencias
- **Notificaciones en tiempo real** en la interfaz web
- **Persistencia en JSON** para mantener alertas entre sesiones

### 🌐 **Interfaz Web Profesional**
![Themes](https://img.shields.io/badge/Temas-Oscuro%2FClaro-ff69b4?logo=paint-brush&logoColor=white)
![Languages](https://img.shields.io/badge/Idiomas-2-important?logo=language&logoColor=white)
![Responsive](https://img.shields.io/badge/100%25-Responsive-success?logo=mobile-alt&logoColor=white)
- **Tema oscuro/claro** automático o manual
- **Soporte multi-idioma** (Español/Inglés)
- **Diseño 100% responsive** para móviles y escritorio

## 🚀 Instalación Rápida

### Prerrequisitos
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![pip](https://img.shields.io/badge/pip-Instalado-3776AB?logo=pypi&logoColor=white)

### Método 1: Instalación Estándar
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/cripto-analizador-pro.git
cd cripto-analizador-pro

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python main.py
```

### Método 2: Script de Instalación Automática
```bash
# Linux/macOS
chmod +x install.sh
./install.sh

# Windows (ejecutar como administrador)
install.bat
```

### Método 3: Usando Docker
```bash
# Construir imagen Docker
docker build -t cripto-analizador .

# Ejecutar contenedor
docker run -p 5000:5000 cripto-analizador
```

### 📋 Dependencias Principales
```txt
flask==2.3.3
pandas==2.0.3
numpy==1.24.3
yfinance==0.2.28
scikit-learn==1.3.0
matplotlib==3.7.2
reportlab==4.0.4
pywebview==4.2.2
```

## 📁 Estructura del Proyecto

```
cripto-analizador-pro/
├── 📄 main.py                 # Punto de entrada principal
├── 📄 funciones.py           # Funciones de análisis y lógica de negocio
├── 📄 global_data.py         # Variables globales y configuración
├── 📄 script.js              # Frontend JavaScript completo
├── 📄 requirements.txt       # Dependencias de Python
├── 📄 index.html            # Interfaz web principal
├── 📄 config.json           # Configuración de la aplicación
│
├── 📂 data/                 # Datos históricos (CSV)
│   ├── 📊 btc_data.csv
│   ├── 📊 eth_data.csv
│   └── ...
│
├── 📂 alertas/              # Alertas guardadas (JSON)
├── 📂 exportaciones/        # Reportes exportados
│   ├── 📑 pdf/
│   ├── 📊 csv/
│   ├── 📝 json/
│   └── 🌐 html/
│
├── 📂 static/               # Recursos estáticos
│   ├── 📂 css/
│   ├── 📂 js/
│   └── 📂 images/
│
└── 📂 docs/                 # Documentación adicional
    ├── 📄 api.md           # Documentación API
    ├── 📄 user_guide.md    # Guía de usuario
    └── 📄 examples/        # Ejemplos de uso
```

## 🎮 Guía de Uso Paso a Paso

### 1. **Inicio Rápido desde Python**
```python
from funciones import AnalizadorCripto

# Crear analizador
analizador = AnalizadorCripto(modo="online")

# Analizar Bitcoin
resultados = analizador.analizar_cripto("BTC")

# Ver resultados
print(f"Precio actual: ${resultados['precio_actual']:,.2f}")
print(f"Tendencia: {resultados['tendencia']}")
print(f"Recomendación: {resultados['recomendacion']}")
```

### 2. **Modo Online (Tiempo Real)**
1. **Seleccionar** "Modo Online" en el dashboard
2. **Elegir** criptomoneda de la lista desplegable
3. **Configurar** parámetros de análisis personalizados
4. **Ver** resultados actualizados cada 60 segundos

### 3. **Modo Offline (Datos Históricos)**
```python
# Cargar datos desde CSV
datos = analizador.cargar_datos_csv("data/btc_2023.csv")

# Analizar período específico
analisis = analizador.analizar_periodo(
    datos=datos,
    inicio="2023-01-01",
    fin="2023-12-31",
    indicadores=['rsi', 'macd', 'bollinger']
)
```

### 4. **Simulación Monte Carlo**
```python
# Generar simulación avanzada
simulacion = analizador.simular_monte_carlo(
    precio_actual=50000,
    dias=30,
    simulaciones=1000,
    volatilidad=0.02,
    drift=0.0005
)

# Analizar resultados
prob_ganancia = simulacion['probabilidad_ganancia']
precio_esperado = simulacion['precio_medio_final']

print(f"Probabilidad de ganancia: {prob_ganancia:.1f}%")
print(f"Precio esperado en 30 días: ${precio_esperado:,.2f}")
```

### 5. **Backtesting de Estrategias**
```python
# Estrategia personalizada
def estrategia_cruce_medias(datos, corta=20, larga=50):
    # Lógica de trading
    return señales

# Probar estrategia
resultados = analizador.backtesting_estrategia(
    datos=datos_historicos,
    estrategia=estrategia_cruce_medias,
    parametros={'corta': 20, 'larga': 50},
    capital_inicial=10000,
    comision=0.001
)

print(f"Rentabilidad: {resultados['rentabilidad']:.2f}%")
print(f"Sharpe Ratio: {resultados['sharpe_ratio']:.2f}")
```

## 📊 API Endpoints

### 🔍 **Endpoints Principales**

| Método | Endpoint | Descripción | Status |
|--------|----------|-------------|---------|
| `GET` | `/api/analizar/<cripto>` | Análisis completo | ✅ Activo |
| `POST` | `/api/simular` | Simulación Monte Carlo | ✅ Activo |
| `GET` | `/api/alertas` | Listar alertas | ✅ Activo |
| `POST` | `/api/alertas` | Crear alerta | ✅ Activo |
| `GET` | `/api/exportar/<formato>` | Exportar datos | ✅ Activo |
| `GET` | `/api/educacion/<categoria>` | Contenido educativo | ✅ Activo |

### 📝 **Ejemplos de Uso API**

#### Análisis de Criptomoneda
```bash
curl -X GET "http://localhost:5000/api/analizar/BTC"
```

**Respuesta:**
```json
{
  "status": "success",
  "data": {
    "criptomoneda": "BTC",
    "precio_actual": 51234.56,
    "tendencia": "alcista",
    "rsi": 65.4,
    "macd": {"valor": 123.45, "senal": 120.12},
    "bollinger": {"superior": 52000, "inferior": 49000},
    "recomendacion": "COMPRAR",
    "confianza": 78.5,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

#### Crear Alerta Personalizada
```bash
curl -X POST "http://localhost:5000/api/alertas" \
  -H "Content-Type: application/json" \
  -d '{
    "cripto": "ETH",
    "tipo": "precio",
    "operador": ">=",
    "valor": 3000,
    "mensaje": "ETH superó $3000",
    "activa": true
  }'
```

## 🎓 Sandbox Educativo

### 📚 **Categorías Disponibles**

#### 📊 **Análisis Técnico** (5 Temas)
- **RSI (Relative Strength Index)**: Indicador de sobrecompra/sobreventa
- **Bandas de Bollinger**: Volatilidad y niveles clave
- **MACD**: Convergencia/divergencia de medias móviles
- **Soporte/Resistencia**: Niveles psicológicos del mercado
- **Volumen**: Confirmación de tendencias

#### 🛡️ **Gestión de Riesgo** (5 Temas)
- **Stop Loss**: Protección automática del capital
- **Take Profit**: Objetivos realistas de ganancia
- **Riesgo por Trade**: Control de exposición máxima
- **Drawdown**: Medición y control de pérdidas
- **Apalancamiento**: Uso responsable

#### 🧠 **Psicología del Trading** (5 Temas)
- **FOMO (Fear Of Missing Out)**: Evitar decisiones impulsivas
- **FUD (Fear, Uncertainty, Doubt)**: Manejo de noticias
- **Overtrading**: Control de frecuencia de operaciones
- **Sesgo de Confirmación**: Análisis objetivo
- **Disciplina**: Seguimiento del plan de trading

#### 📈 **Términos del Mercado** (5 Temas)
- **Volatilidad**: Medición de variaciones de precio
- **Liquidez**: Capacidad de ejecución rápida
- **Pump and Dump**: Esquemas fraudulentos
- **Correlación**: Relación entre diferentes activos
- **Tendencia**: Dirección del mercado

## ⚙️ Configuración Avanzada

### 🔧 **Variables de Entorno**
Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env file
CRYPTO_ANALYZER_MODE="online"
YAHOO_FINANCE_TIMEOUT=30
MAX_SIMULATIONS=5000
DEFAULT_LANGUAGE="es"
THEME="auto"
ENABLE_EMAIL_ALERTS=false
API_PORT=5000
DEBUG_MODE=false
```

### 🎛️ **Archivo de Configuración**
`config.json` permite personalizar el comportamiento:

```json
{
  "api": {
    "yahoo_finance": {
      "timeout": 30,
      "retries": 3,
      "cache_duration": 300
    },
    "port": 5000,
    "debug": false
  },
  "analisis": {
    "rsi_periodo": 14,
    "macd_rapida": 12,
    "macd_lenta": 26,
    "bollinger_periodo": 20,
    "bollinger_desviaciones": 2,
    "ema_periodo_corta": 9,
    "ema_periodo_larga": 21
  },
  "alertas": {
    "email_notifications": false,
    "sound_alerts": true,
    "price_change_threshold": 5.0,
    "volume_spike_multiplier": 3.0,
    "check_interval_seconds": 60
  },
  "exportacion": {
    "pdf_quality": "high",
    "csv_delimiter": ",",
    "html_template": "modern",
    "default_format": "pdf"
  },
  "interfaz": {
    "theme": "auto",
    "language": "es",
    "refresh_interval": 60000,
    "chart_animation": true
  }
}
```

### 🔍 **Solución de Problemas Comunes**

1. **Error: "Módulo no encontrado"**
```bash
# Asegúrate de tener todas las dependencias
pip install -r requirements.txt --upgrade
```

2. **Error de conexión con Yahoo Finance**
```bash
# Verifica tu conexión a internet
# O cambia a modo offline temporalmente
```

3. **La aplicación no inicia**
```bash
# Verifica que el puerto 5000 esté libre
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/macOS
```

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Ver [`LICENSE`](LICENSE) para más información.

```
MIT License

Copyright (c) 2024 Cripto Analizador Pro

Se concede permiso, libre de cargos, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados...
```

## ⚠️ Descargo de Responsabilidad

**ESTE SOFTWARE ES PARA FINES EDUCATIVOS Y DE ANÁLISIS ÚNICAMENTE**

- ❌ **NO** es asesoramiento financiero
- ❌ **NO** garantiza ganancias
- ❌ **NO** se hace responsable de pérdidas
- ✅ **SÍ** es una herramienta educativa
- ✅ **SÍ** ayuda a entender el mercado
- ✅ **SÍ** promueve el trading responsable

**El trading de criptomonedas conlleva riesgos significativos de pérdida de capital. Nunca invierta más de lo que puede permitirse perder. Consulte con un asesor financiero profesional antes de tomar cualquier decisión de inversión.**

---

<div align="center">

## ⭐ ¡Dale una estrella al proyecto!

[![Star History Chart](https://api.star-history.com/svg?repos=tu-usuario/cripto-analizador-pro&type=Date)](https://star-history.com/#tu-usuario/cripto-analizador-pro&Date)

**Hecho con ❤️ para la comunidad cripto**

</div>
```
