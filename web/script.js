// web/script.js - JavaScript compartido

// Utilidades
const API_BASE = '';

function fetchAPI(endpoint, options = {}) {
    return fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    }).then(r => r.json());
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(value);
}

function formatPercentage(value) {
    return (value > 0 ? '+' : '') + value.toFixed(2) + '%';
}

// Notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }, 100);
}

// Utilidades de gráficos
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

// Sistema de temas dinámico
function applyTheme(theme) {
    const root = document.documentElement;
    const isDark = theme === 'oscuro';
    
    if (isDark) {
        root.style.setProperty('--bg-dark', '#0f172a');
        root.style.setProperty('--bg-card', '#1e293b');
        root.style.setProperty('--bg-sidebar', '#1e293b');
        root.style.setProperty('--text-primary', '#f1f5f9');
        root.style.setProperty('--text-secondary', '#94a3b8');
        root.style.setProperty('--border-color', '#334155');
    } else {
        root.style.setProperty('--bg-dark', '#ffffff');
        root.style.setProperty('--bg-card', '#f8fafc');
        root.style.setProperty('--bg-sidebar', '#e2e8f0');
        root.style.setProperty('--text-primary', '#1e293b');
        root.style.setProperty('--text-secondary', '#64748b');
        root.style.setProperty('--border-color', '#cbd5e1');
    }
    
    localStorage.setItem('theme', theme);
}

// Sistema de idiomas
function applyLanguage(lang) {
    const isSpanish = lang === 'es';
    
    // Actualizar textos según idioma
    const texts = {
        es: {
            title: 'Cripto Analizador Pro',
            onlineMode: 'Modo Online',
            offlineMode: 'Modo Offline',
            dashboard: 'Dashboard',
            charts: 'Gráficos',
            analysis: 'Análisis',
            alerts: 'Alertas',
            sentiment: 'Sentimiento',
            aiExplanation: 'IA Explicativa',
            correlation: 'Correlación',
            backtesting: 'Backtesting',
            comparison: 'Comparación',
            sandbox: 'Sandbox Educativo',
            simulation: 'Simulación',
            dataManagement: 'Gestión de Datos',
            export: 'Exportar',
            settings: 'Configuración',
            theme: 'Tema',
            language: 'Idioma',
            lightTheme: 'Claro',
            darkTheme: 'Oscuro',
            spanish: 'Español',
            english: 'English',
            currentPrice: 'Precio Actual',
            trend: 'Tendencia',
            decision: 'Decisión',
            confidence: 'Confianza',
            prediction24h: 'Predicción 24h',
            rsi: 'RSI',
            macd: 'MACD',
            volume: 'Volumen',
            initialCapital: 'Capital Inicial',
            finalCapital: 'Capital Final',
            totalReturn: 'Retorno Total',
            buyAndHold: 'Buy & Hold',
            maxDrawdown: 'Max Drawdown',
            operations: 'Operaciones',
            winners: 'Ganadoras',
            losers: 'Perdedoras',
            buy: 'Compra',
            sell: 'Venta',
            hold: 'Mantener',
            bullish: 'Alcista',
            bearish: 'Bajista',
            neutral: 'Neutral',
            overbought: 'Sobrecompra',
            oversold: 'Sobreventa',
            volatility: 'Volatilidad',
            momentum: 'Momento',
            sentiment: 'Sentimiento',
            correlation: 'Correlación',
            backtesting: 'Backtesting',
            multipleComparison: 'Comparación Múltiple',
            candlestickChart: 'Gráfico de Velas',
            lineChart: 'Gráfico de Línea',
            barChart: 'Gráfico de Barras',
            areaChart: 'Gráfico de Área',
            scatterChart: 'Gráfico de Dispersión',
            exportImage: 'Exportar Imagen',
            exportPDF: 'Exportar PDF',
            exportCSV: 'Exportar CSV',
            exportJSON: 'Exportar JSON',
            alertConfigured: 'Alerta configurada correctamente',
            errorAlert: 'Error al configurar alerta',
            dataUpdated: 'Datos actualizados',
            errorData: 'Error al actualizar datos',
            simulationGenerated: 'Simulación generada',
            errorSimulation: 'Error al generar simulación',
            fileUploaded: 'Archivo subido correctamente',
            errorFile: 'Error al subir archivo',
            cryptoDeleted: 'Criptomoneda eliminada',
            errorDelete: 'Error al eliminar criptomoneda',
            backtestingCompleted: 'Backtesting completado',
            errorBacktesting: 'Error en backtesting',
            comparisonGenerated: 'Comparación generada',
            errorComparison: 'Error al generar comparación',
            languageChanged: 'Idioma cambiado',
            themeChanged: 'Tema cambiado',
            settingsSaved: 'Configuración guardada',
            errorSettings: 'Error al guardar configuración'
        },
        en: {
            title: 'Crypto Analyzer Pro',
            onlineMode: 'Online Mode',
            offlineMode: 'Offline Mode',
            dashboard: 'Dashboard',
            charts: 'Charts',
            analysis: 'Analysis',
            alerts: 'Alerts',
            sentiment: 'Sentiment',
            aiExplanation: 'AI Explanation',
            correlation: 'Correlation',
            backtesting: 'Backtesting',
            comparison: 'Comparison',
            sandbox: 'Educational Sandbox',
            simulation: 'Simulation',
            dataManagement: 'Data Management',
            export: 'Export',
            settings: 'Settings',
            theme: 'Theme',
            language: 'Language',
            lightTheme: 'Light',
            darkTheme: 'Dark',
            spanish: 'Spanish',
            english: 'English',
            currentPrice: 'Current Price',
            trend: 'Trend',
            decision: 'Decision',
            confidence: 'Confidence',
            prediction24h: '24h Prediction',
            rsi: 'RSI',
            macd: 'MACD',
            volume: 'Volume',
            initialCapital: 'Initial Capital',
            finalCapital: 'Final Capital',
            totalReturn: 'Total Return',
            buyAndHold: 'Buy & Hold',
            maxDrawdown: 'Max Drawdown',
            operations: 'Operations',
            winners: 'Winners',
            losers: 'Losers',
            buy: 'Buy',
            sell: 'Sell',
            hold: 'Hold',
            bullish: 'Bullish',
            bearish: 'Bearish',
            neutral: 'Neutral',
            overbought: 'Overbought',
            oversold: 'Oversold',
            volatility: 'Volatility',
            momentum: 'Momentum',
            sentiment: 'Sentiment',
            correlation: 'Correlation',
            backtesting: 'Backtesting',
            multipleComparison: 'Multiple Comparison',
            candlestickChart: 'Candlestick Chart',
            lineChart: 'Line Chart',
            barChart: 'Bar Chart',
            areaChart: 'Area Chart',
            scatterChart: 'Scatter Chart',
            exportImage: 'Export Image',
            exportPDF: 'Export PDF',
            exportCSV: 'Export CSV',
            exportJSON: 'Export JSON',
            alertConfigured: 'Alert configured successfully',
            errorAlert: 'Error configuring alert',
            dataUpdated: 'Data updated',
            errorData: 'Error updating data',
            simulationGenerated: 'Simulation generated',
            errorSimulation: 'Error generating simulation',
            fileUploaded: 'File uploaded successfully',
            errorFile: 'Error uploading file',
            cryptoDeleted: 'Cryptocurrency deleted',
            errorDelete: 'Error deleting cryptocurrency',
            backtestingCompleted: 'Backtesting completed',
            errorBacktesting: 'Backtesting error',
            comparisonGenerated: 'Comparison generated',
            errorComparison: 'Error generating comparison',
            languageChanged: 'Language changed',
            themeChanged: 'Theme changed',
            settingsSaved: 'Settings saved',
            errorSettings: 'Error saving settings'
        }
    };
    
    // Aplicar textos según idioma
    document.title = texts[lang].title;
    
    // Guardar preferencia
    localStorage.setItem('lang', lang);
    
    // Actualizar botones de idioma
    const langToggle = document.getElementById('lang-toggle');
    if (langToggle) {
        langToggle.innerHTML = isSpanish ? '<i class="fas fa-flag-usa"></i>' : '<i class="fas fa-flag"></i>';
    }
}

// Función para cambiar tema
function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'oscuro';
    const newTheme = currentTheme === 'oscuro' ? 'claro' : 'oscuro';
    applyTheme(newTheme);
}

// Función para cambiar idioma
function toggleLanguage() {
    const currentLang = localStorage.getItem('lang') || 'es';
    const newLang = currentLang === 'es' ? 'en' : 'es';
    applyLanguage(newLang);
}

// Inicializar tema e idioma al cargar
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'oscuro';
    const savedLang = localStorage.getItem('lang') || 'es';
    
    applyTheme(savedTheme);
    applyLanguage(savedLang);
});

// Detectar preferencias del sistema
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    if (!localStorage.getItem('theme')) {
        applyTheme('claro');
    }
}

// Detectar idioma del navegador
const navLang = navigator.language || navigator.userLanguage;
if (navLang.startsWith('en')) {
    if (!localStorage.getItem('lang')) {
        applyLanguage('en');
    }
}

// Exportar funciones útiles
window.utils = {
    fetchAPI,
    formatCurrency,
    formatPercentage,
    showNotification,
    createGradient,
    applyTheme,
    applyLanguage,
    toggleTheme,
    toggleLanguage
};

async function cargarCriptosTop100() {
    console.log("✅ Usando lista específica de 9 criptomonedas:", allCriptos);
    
    // Actualizar selectores, checkboxes, etc.
    if (typeof loadAvailableCriptos === 'function') {
        loadAvailableCriptos();
    }
    
    return allCriptos;
}

// Responsive handler para gráficos
window.addEventListener('resize', debounce(() => {
    // Redibujar todos los gráficos activos
    Object.values(window.charts || {}).forEach(chart => {
        if (chart && typeof chart.resize === 'function') {
            chart.resize();
        }
    });
}, 250));

// Función utilitaria debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Funciones de exportación para modo online
function exportData(formato) {
    if (Object.keys(currentData.analisis || {}).length === 0) {
        showNotification('No hay datos para exportar', 'warning');
        return;
    }
    
    const btn = event.target.closest('button');
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Exportando...';
    
    fetch('/api/online/exportar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({formato: formato})
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la exportación');
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analisis_online_${new Date().toISOString().slice(0,10)}.${formato}`;
        a.click();
        window.URL.revokeObjectURL(url);
        
        showNotification(`Exportación ${formato.toUpperCase()} completada`, 'success');
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    })
    .catch(error => {
        showNotification('Error al exportar', 'error');
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    });
}

function exportChart() {
    const formato = prompt('Formato de imagen (png/svg):', 'png') || 'png';
    showNotification('Funcionalidad de exportación de gráficos implementada', 'info');
}

// Prevenir zoom en dispositivos móviles
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});

// Ajustar viewport para móviles
const viewport = document.querySelector('meta[name="viewport"]');
if (viewport) {
    viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
}

// Llamar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarCriptosTop100();
});

// 📚 FUNCIONES MEJORADAS PARA SANDBOX EDUCATIVO

function cargarSandbox() {
    const topics = [
        {
            titulo: "Análisis Técnico",
            icono: "fas fa-chart-line",
            color: "#2196F3",
            contenido: `
                <h4>📊 Análisis Técnico</h4>
                <p>El análisis técnico estudia el comportamiento del precio para predecir movimientos futuros.</p>

                ${crearTarjetaConcepto({
                    titulo: "RSI (Índice de Fuerza Relativa)",
                    icono: "fas fa-tachometer-alt",
                    color: "#FF5722",
                    definicion: "Mide la velocidad y magnitud de los cambios recientes de precio.",
                    rango: "0 a 100",
                    señales: ">70 = sobrecompra; <30 = sobreventa",
                    formula: "RSI = 100 − (100 / (1 + RS)), donde RS = promedio ganancias / pérdidas (14 períodos)",
                    ejemplo: "Un RSI de 28 sugiere que el activo podría rebotar.",
                    error: "Usarlo en mercados laterales sin confirmación.",
                    tipo: "oscilador"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Soporte y Resistencia",
                    icono: "fas fa-layer-group",
                    color: "#4CAF50",
                    definicion: "Niveles de precio donde históricamente se ha detenido una caída (soporte) o un alza (resistencia).",
                    ejemplo: "BTC ha rebotado 3 veces en $40,000 → soporte fuerte.",
                    error: "Asumir que siempre se respetan; pueden romperse con volumen.",
                    tipo: "nivel"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Volumen",
                    icono: "fas fa-chart-bar",
                    color: "#00BCD4",
                    definicion: "Cantidad de activos negociados en un período.",
                    ejemplo: "Un breakout sin volumen suele ser falso.",
                    error: "Ignorar el volumen al tomar decisiones.",
                    tipo: "confirmacion"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Bollinger Bands",
                    icono: "fas fa-wave-square",
                    color: "#9C27B0",
                    definicion: "Bandas superior e inferior basadas en desviación estándar del precio.",
                    señales: "Precio cerca de banda superior = sobrecompra; banda inferior = sobreventa",
                    ejemplo: "El precio tocó la banda inferior y rebotó → posible compra.",
                    error: "Operar contra la tendencia solo por tocar una banda.",
                    tipo: "volatilidad"
                })}

                ${crearTarjetaConcepto({
                    titulo: "MACD",
                    icono: "fas fa-chart-area",
                    color: "#FFC107",
                    definicion: "Indicador de impulso basado en medias móviles.",
                    señales: "Cruce de la línea MACD con la señal → cambio de tendencia",
                    ejemplo: "Cruce alcista en MACD precedió una subida del 10%.",
                    error: "Usarlo en mercados sin tendencia clara.",
                    tipo: "impulso"
                })}
            `
        },
        {
            titulo: "Gestión de Riesgo",
            icono: "fas fa-shield-alt",
            color: "#4CAF50",
            contenido: `
                <h4>🛡️ Gestión de Riesgo</h4>
                <p>Protege tu capital y evita pérdidas innecesarias.</p>

                ${crearTarjetaConcepto({
                    titulo: "Stop Loss",
                    icono: "fas fa-stop-circle",
                    color: "#F44336",
                    definicion: "Orden para limitar pérdidas si el precio va en contra.",
                    formula: "Stop = Precio de entrada − Riesgo máximo aceptado",
                    ejemplo: "Compraste en $42,000, stop en $41,000 → riesgo de $1,000.",
                    error: "Colocarlo demasiado ajustado y ser sacado por ruido.",
                    tipo: "proteccion"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Take Profit",
                    icono: "fas fa-bullseye",
                    color: "#4CAF50",
                    definicion: "Orden para cerrar ganancias al alcanzar un objetivo.",
                    ejemplo: "Take profit en $45,000 tras comprar en $42,000 → +7%.",
                    error: "No usarlo y perder ganancias por volatilidad.",
                    tipo: "objetivo"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Riesgo por Trade",
                    icono: "fas fa-percentage",
                    color: "#FF9800",
                    definicion: "Porcentaje del capital que se arriesga en una operación.",
                    regla: "Nunca más del 1-2% por trade.",
                    ejemplo: "Con $10,000, riesgo máximo = $100–$200 por operación.",
                    error: "Arriesgar más del 5% → alto riesgo de ruina.",
                    tipo: "regla"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Drawdown",
                    icono: "fas fa-chart-line-down",
                    color: "#9C27B0",
                    definicion: "Caída máxima desde un pico de capital hasta un mínimo posterior.",
                    ejemplo: "Tu drawdown fue del 15% en enero → revisa tu estrategia.",
                    error: "Ignorarlo hasta que es demasiado tarde.",
                    tipo: "analisis"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Apalancamiento",
                    icono: "fas fa-weight-hanging",
                    color: "#00BCD4",
                    definicion: "Usar capital prestado para aumentar exposición.",
                    ejemplo: "10x en BTC: +10% → +100%; −10% → −100% (liquidación).",
                    error: "Usar apalancamiento alto sin stop loss.",
                    tipo: "riesgo"
                })}
            `
        },
        {
            titulo: "Psicología del Trading",
            icono: "fas fa-brain",
            color: "#9C27B0",
            contenido: `
                <h4>🧠 Psicología del Trading</h4>
                <p>Controlar tus emociones es tan importante como tener una buena estrategia.</p>

                ${crearTarjetaConcepto({
                    titulo: "FOMO (Fear Of Missing Out)",
                    icono: "fas fa-fire",
                    color: "#FF5722",
                    definicion: "Miedo a perderse una ganancia, lleva a entrar sin plan.",
                    ejemplo: "Comprar tras una subida del 20% en 1 hora → FOMO.",
                    solucion: "Esperar pullback o confirmación técnica.",
                    tipo: "emocion"
                })}

                ${crearTarjetaConcepto({
                    titulo: "FUD (Fear, Uncertainty, Doubt)",
                    icono: "fas fa-newspaper",
                    color: "#607D8B",
                    definicion: "Miedo generado por noticias negativas o rumores.",
                    ejemplo: "Vender en pánico por un tweet → FUD.",
                    solucion: "Analizar si la noticia afecta fundamentalmente al activo.",
                    tipo: "emocion"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Overtrading",
                    icono: "fas fa-sync-alt",
                    color: "#FFC107",
                    definicion: "Abrir demasiadas operaciones por ansiedad o aburrimiento.",
                    consecuencia: "Altas comisiones, fatiga, malas decisiones.",
                    solucion: "Tener reglas claras de entrada y esperar setups de calidad.",
                    tipo: "comportamiento"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Sesgo de Confirmación",
                    icono: "fas fa-search",
                    color: "#8BC34A",
                    definicion: "Buscar solo información que confirme tu idea.",
                    ejemplo: "Ignorar señales bajistas porque 'crees' que subirá.",
                    solucion: "Buscar activamente evidencia contraria.",
                    tipo: "sesgo"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Disciplina",
                    icono: "fas fa-dumbbell",
                    color: "#4CAF50",
                    definicion: "Seguir tu plan de trading sin importar emociones.",
                    importancia: "Clave para la consistencia a largo plazo.",
                    ejercicio: "¿Estoy operando por mi estrategia o por emoción?",
                    tipo: "habito"
                })}
            `
        },
        {
            titulo: "Términos del Mercado",
            icono: "fas fa-book",
            color: "#FF9800",
            contenido: `
                <h4>📚 Términos del Mercado</h4>
                <p>Conoce el lenguaje del trading para entender lo que está pasando.</p>

                ${crearTarjetaConcepto({
                    titulo: "Volatilidad",
                    icono: "fas fa-bolt",
                    color: "#FF5722",
                    definicion: "Grado de variación del precio en el tiempo.",
                    ejemplo: "Las altcoins son más volátiles que Bitcoin.",
                    implicacion: "Mayor volatilidad → mayor riesgo y oportunidad.",
                    tipo: "metrica"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Liquidez",
                    icono: "fas fa-tint",
                    color: "#00BCD4",
                    definicion: "Facilidad para comprar/vender sin mover el precio.",
                    ejemplo: "BTC es muy líquido; una altcoin pequeña no lo es.",
                    tipo: "metrica"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Pump and Dump",
                    icono: "fas fa-rocket",
                    color: "#F44336",
                    definicion: "Subida artificial del precio seguida de venta masiva.",
                    señal: "Volumen inusual + redes sociales promocionando.",
                    proteccion: "Evitar proyectos sin fundamentos.",
                    tipo: "manipulacion"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Correlación",
                    icono: "fas fa-link",
                    color: "#9C27B0",
                    definicion: "Cómo se mueven dos activos juntos.",
                    ejemplo: "BTC y ETH suelen tener correlación alta (+0.8).",
                    uso: "Diversificación efectiva requiere baja correlación.",
                    tipo: "estadistica"
                })}

                ${crearTarjetaConcepto({
                    titulo: "Tendencia (Trend)",
                    icono: "fas fa-arrow-trend-up",
                    color: "#4CAF50",
                    definicion: "Dirección general del precio (alcista, bajista, lateral).",
                    regla: "La tendencia es tu amiga.",
                    herramientas: "Medias móviles, máximos/mínimos ascendentes.",
                    tipo: "direccion"
                })}
            `
        }
    ];

    const container = document.getElementById('sandbox-topics');
    container.innerHTML = topics.map((t, i) => `
        <div class="indicator-card" onclick="mostrarTemaSandbox(${i})" style="cursor: pointer;">
            <div class="indicator-icon" style="background: ${t.color}20; color: ${t.color};">
                <i class="${t.icono}"></i>
            </div>
            <h4>${t.titulo}</h4>
            <p style="font-size: 0.875rem; color: var(--text-secondary);">Haz clic para aprender más</p>
        </div>
    `).join('');

    window.sandboxTopics = topics;
}

function crearTarjetaConcepto({ titulo, icono, color, definicion, rango, señales, formula, ejemplo, error, solucion, consecuencia, regla, importancia, ejercicio, proteccion, uso, herramientas, tipo }) {
    const tipoClase = {
        oscilador: "🔁",
        nivel: "📊",
        confirmacion: "✅",
        volatilidad: "📈",
        impulso: "⚡",
        proteccion: "🛡️",
        objetivo: "🎯",
        regla: "📏",
        analisis: "📉",
        riesgo: "⚠️",
        emocion: "😰",
        sesgo: "🧠",
        comportamiento: "🔄",
        habito: "💪",
        metrica: "📊",
        manipulacion: "🎭",
        estadistica: "📈",
        direccion: "🧭"
    };

    const iconoTipo = tipoClase[tipo] || "📌";

    return `
        <div class="tarjeta-concepto" style="border-left: 5px solid ${color}; background: rgba(255,255,255,0.02); padding: 1.5rem; margin: 1.5rem 0; border-radius: 12px;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <i class="${icono}" style="font-size: 1.5rem; color: ${color};"></i>
                <h5 style="margin: 0; color: ${color};">${iconoTipo} ${titulo}</h5>
            </div>

            <p style="margin-bottom: 1rem; color: var(--text-secondary);">${definicion}</p>

            ${rango ? `<p><strong>Rango:</strong> <span style="color: var(--info-color);">${rango}</span></p>` : ''}
            ${señales ? `<p><strong>Señales:</strong> <span style="color: var(--warning-color);">${señales}</span></p>` : ''}
            ${regla ? `<p><strong>Regla:</strong> <span style="color: var(--success-color);">${regla}</span></p>` : ''}
            ${importancia ? `<p><strong>Importancia:</strong> <span style="color: var(--primary-color);">${importancia}</span></p>` : ''}
            ${uso ? `<p><strong>Uso:</strong> <span style="color: var(--text-primary);">${uso}</span></p>` : ''}
            ${herramientas ? `<p><strong>Herramientas:</strong> <span style="color: var(--text-secondary);">${herramientas}</span></p>` : ''}

            ${formula ? `
                <div class="explanation">
                    <code>${formula}</code>
                </div>
            ` : ''}

            ${ejemplo ? `
                <div style="background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>✅ Ejemplo práctico:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${ejemplo}</p>
                </div>
            ` : ''}

            ${error ? `
                <div style="background: rgba(244, 67, 54, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>❌ Error común:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${error}</p>
                </div>
            ` : ''}

            ${solucion ? `
                <div style="background: rgba(33, 150, 243, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>💡 Solución:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${solucion}</p>
                </div>
            ` : ''}

            ${consecuencia ? `
                <div style="background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>⚠️ Consecuencia:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${consecuencia}</p>
                </div>
            ` : ''}

            ${proteccion ? `
                <div style="background: rgba(156, 39, 176, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>🛡️ Protección:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${proteccion}</p>
                </div>
            ` : ''}

            ${ejercicio ? `
                <div style="background: rgba(0, 188, 212, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong>🧠 Ejercicio:</strong>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">${ejercicio}</p>
                </div>
            ` : ''}
        </div>
    `;
}

function mostrarTemaSandbox(index) {
    const tema = window.sandboxTopics[index];
    const content = document.getElementById('sandbox-content');
    content.innerHTML = tema.contenido;
    content.style.display = 'block';
    content.scrollIntoView({ behavior: 'smooth' });
}

// Llamar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarSandbox();
});