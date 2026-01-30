# 🚀 Cripto Analizador Pro

**Análisis técnico profesional de criptomonedas con IA explicativa**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.0+-orange.svg)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Índice

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [API](#api)
- [Tecnologías](#tecnologías)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## 🎯 Descripción

**Cripto Analizador Pro** es una plataforma profesional para análisis técnico de criptomonedas que combina datos en tiempo real, inteligencia artificial explicativa y herramientas educativas. Ofrece dos modos de operación: **Online** con datos en tiempo real y **Offline** para análisis profundo con datos locales.

### 🎯 Objetivo Principal

 Democratizar el análisis técnico de criptomonedas, haciéndolo accesible tanto para traders principiantes como profesionales, con explicaciones detalladas y educativas de cada indicador técnico.

## ✨ Características

### 🔥 Modo Online (Tiempo Real)
- ✅ **Datos en vivo** desde Yahoo Finance
- ✅ **Actualización automática** configurable
- ✅ **15+ indicadores técnicos** (RSI, MACD, Bollinger, etc.)
- ✅ **IA Explicativa** con análisis detallado en lenguaje simple
- ✅ **Alertas inteligentes** (pumps, dumps, volúmenes anormales)
- ✅ **Análisis de sentimiento** del mercado
- ✅ **Correlación entre criptomonedas**
- ✅ **Backtesting** de estrategias
- ✅ **Comparación múltiple** de métricas
- ✅ **Exportación** en PDF, CSV y JSON

### 💾 Modo Offline (Análisis Profundo)
- ✅ **Carga de archivos CSV** personalizados
- ✅ **Simulación de mercado** con Monte Carlo
- ✅ **Sandbox educativo** con explicaciones interactivas
- ✅ **Gestión completa** de datos locales
- ✅ **Análisis de correlación** offline
- ✅ **Backtesting** sobre datos históricos
- ✅ **Exportación avanzada** de informes

### 🎨 Interfaz de Usuario
- 📱 **Diseño responsive** para móviles y tablets
- 📊 **Gráficos interactivos** con Chart.js
- 📈 **Dashboard intuitivo** con métricas clave

### 🧠 Educación
- 📚 **Explicaciones detalladas** de cada indicador
- 🎓 **Conceptos clave** del trading
- ⚠️ **Errores comunes** y cómo evitarlos
- 💡 **Ejemplos prácticos** con casos reales
- 🧠 **Psicología del trading** y gestión de riesgo

## 🚀 Instalación

### 📋 Requisitos Previos

```bash
# Python 3.8 o superior
python --version

# pip actualizado
python -m pip install --upgrade pip
```

### 📥 Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/cripto-analizador-pro.git
cd cripto-analizador-pro

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear carpetas necesarias
mkdir -p datos simulacion resultados web/assets

# 5. Ejecutar la aplicación
python main.py
```

### 📦 Dependencias Principales

```txt
Flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
yfinance==0.2.28
scikit-learn==1.3.0
requests==2.31.0
beautifulsoup4==4.12.2
reportlab==4.0.4
pywebview==4.2.2
```

## 🎯 Uso

### 🌐 Iniciar la Aplicación

```bash
python main.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en:
```
http://localhost:5000
```

### 📊 Seleccionar Modo de Operación

#### 🔥 Modo Online
1. Selecciona "Modo Online" desde la página principal
2. Elige las criptomonedas a monitorear
3. Configura el intervalo de actualización
4. Activa las alertas deseadas
5. ¡Listo! Los datos se actualizarán automáticamente

#### 💾 Modo Offline
1. Selecciona "Modo Offline"
2. Sube archivos CSV con datos históricos
3. O genera simulaciones sintéticas
4. Realiza análisis profundos
5. Exporta resultados en diferentes formatos

### 📈 Funciones Principales

#### Análisis Técnico
```python
# Ejemplo de análisis rápido
from funciones import analisis_rapido_cripto

resultado = analisis_rapido_cripto('BTC', 'datos')
print(f"Decisión: {resultado['decision_info']['decision']}")
print(f"Confianza: {resultado['decision_info']['confianza']}")
```

#### Simulación de Monte Carlo
```python
# Generar datos sintéticos
from funciones import generar_datos_sinteticos

df = generar_datos_sinteticos(
    precio_inicial=50000,
    dias=90,
    volatilidad=0.03,
    tendencia=0.001
)
```

#### Backtesting
```python
# Probar estrategia RSI + MACD
from funciones import backtesting_estrategia

resultados = backtesting_estrategia(
    df=datos_historicos,
    capital_inicial=10000,
    estrategia='rsi_macd'
)
```

## 🏗️ Arquitectura

### 📁 Estructura del Proyecto

```
cripto-analizador-pro/
│
├── 📁 datos/              # CSV de criptomonedas
├── 📁 simulacion/         # Simulaciones generadas
├── 📁 resultados/         # Exportaciones (PDF, CSV, JSON)
│
├── 🐍 main.py             # Backend Flask
├── 🧮 funciones.py        # Lógica de análisis
├── ⚙️ global_data.py      # Configuraciones globales
│
└── 🌐 web/                # Frontend
    ├── 📄 index.html      # Landing page
    ├── 🔴 online.html     # Modo online
    ├── 🔵 offline.html    # Modo offline
    ├── 📜 script.js       # JavaScript
    ├── 🎨 style.css       # Estilos
    └── 📁 assets/         # Recursos
```

### 🔧 Componentes Principales

#### Backend (Python)
- **`main.py`**: Servidor Flask con rutas API
- **`funciones.py`**: Lógica de análisis técnico y utilidades
- **`global_data.py`**: Configuraciones y constantes

#### Frontend (JavaScript/HTML/CSS)
- **Interfaz moderna** con diseño glassmorphism
- **Gráficos interactivos** con Chart.js
- **Responsive design** para todos los dispositivos

## 🔌 API

### 📡 Endpoints Principales

#### Modo Online
```http
# Iniciar monitoreo
POST /api/online/iniciar

# Estado actual
GET /api/online/estado

# Actualización manual
POST /api/online/actualizar-manual

# Análisis de sentimiento
GET /api/online/sentimiento-detallado?cripto=BTC

# Detección de anomalías
GET /api/online/anomalias

# IA explicativa
POST /api/online/ia-explicacion

# Backtesting online
POST /api/online/backtesting
```

#### Modo Offline
```http
# Análisis completo
POST /api/offline/analisis

# Cargar CSV
POST /api/offline/subir-csv

# Simulación Monte Carlo
POST /api/offline/simulacion

# Correlación
POST /api/offline/correlacion

# Backtesting offline
POST /api/offline/backtesting

# Comparación múltiple
POST /api/offline/comparacion
```

## 🛠️ Tecnologías

### Backend
- **Python 3.8+** - Lenguaje principal
- **Flask** - Framework web
- **Pandas/NumPy** - Procesamiento de datos
- **Scikit-learn** - Machine learning
- **Matplotlib** - Visualizaciones
- **BeautifulSoup** - Web scraping
- **ReportLab** - Generación de PDFs

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6+** - Lógica del cliente
- **Chart.js** - Gráficos interactivos
- **Font Awesome** - Iconos
- **Inter** - Tipografía moderna

### APIs Externas
- **Yahoo Finance** - Datos de mercado
- **CoinMarketCap** - Información de criptomonedas

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Yahoo Finance** por proporcionar datos de mercado
- **Chart.js** por las visualizaciones increíbles
- **Comunidad Python** por las excelentes librerías
- **Todos los contribuyentes** que hacen esto posible

---

<div align="center">

### ⭐ Si este proyecto te fue útil, ¡dale una estrella!

### 🚀 Hecho con ❤️ para la comunidad de cripto-traders

</div>
