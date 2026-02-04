# 📋 INSTRUCCIONES DE INSTALACIÓN - Cripto Analizador Pro

## ⚠️ IMPORTANTE: Configuración de Aplicación Desktop

Tu aplicación está configurada para ejecutarse como una **aplicación de escritorio**, no como un sitio web en navegador.

---

## 🚀 INSTALACIÓN CORRECTA

### 1. **Instalar Dependencias Python**
```bash
pip install -r requirements.txt
```

### 2. **Verificar que Eel esté instalado**
```bash
pip install Eel
```

### 3. **Ejecutar la Aplicación**
```bash
python main.py
```

---

## 📌 QUÉ ESPERAR AL EJECUTAR

Cuando ejecutes `python main.py`, deberías ver:
- ✅ Se abrirá automáticamente una **ventana de aplicación de escritorio** (no el navegador)
- ✅ La ventana tendrá el título "Cripto Analizador Pro"
- ✅ Tamaño de ventana: 1400x900 píxeles
- ✅ La consola mostrará: `Iniciando aplicación desktop con Eel...`

---

## ❌ SI SE ABRE EN NAVEGADOR (PROBLEMA)

Si se abre en el navegador en lugar de como aplicación desktop, significa que **Eel no está instalado correctamente**.

### Solución:
```bash
# Desinstalar Eel si está roto
pip uninstall Eel

# Reinstalar Eel
pip install Eel --upgrade

# Volver a ejecutar
python main.py
```

---

## 🔄 ALTERNATIVA: pywebview

Si Eel no funciona, la aplicación intentará usar **pywebview** como fallback.

Para usar pywebview explícitamente:
```bash
pip install pywebview==6.1
```

---

## 🛠️ REQUISITOS DEL SISTEMA

### Windows
- Python 3.8+
- No requiere instalación adicional de navegadores

### macOS
- Python 3.8+
- Requiere Safari (viene con macOS)

### Linux
- Python 3.8+
- Requiere GTK-3+ (Debian/Ubuntu):
  ```bash
  sudo apt-get install python3-tk python3-dev python3-gi gir1.2-gtk-3.0
  ```

---

## 📦 NOTAS IMPORTANTES

1. **No intentes abrir manualmente** `http://127.0.0.1:5000` en tu navegador
2. **La ventana se abrirá automáticamente** cuando ejecutes `python main.py`
3. **Si necesitas acceder desde otro navegador**, sí puedes abrir `http://127.0.0.1:5000`
4. **El servidor Flask corre automáticamente** en background cuando usas Eel

---

## 📱 COMPONENTES

| Componente | Descripción |
|-----------|-------------|
| **Eel** | Transforma la app en aplicación de escritorio |
| **Flask** | Backend API para procesar datos |
| **HTML/CSS/JS** | Frontend (carpeta `web/`) |
| **Pandas/NumPy** | Análisis de datos financieros |
| **yfinance** | Descarga de datos de criptomonedas |

---

## ✅ VERIFICACIÓN

Para verificar que todo esté bien instalado:
```bash
python -c "import eel; print('✓ Eel instalado')"
python -c "import flask; print('✓ Flask instalado')"
python -c "import pandas; print('✓ Pandas instalado')"
python -c "import yfinance; print('✓ yfinance instalado')"
```

---

**¡Listo! Tu aplicación debe abrir como una ventana de escritorio. 🎉**
