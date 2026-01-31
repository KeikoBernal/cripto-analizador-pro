# 🚀 Cripto Analizador Pro

**Plataforma moderna de análisis técnico de criptomonedas con React, Next.js y Recharts**

[![Next.js](https://img.shields.io/badge/Next.js-16.0+-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19.2+-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.1+-06B6D4.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Stack Tecnológico](#stack-tecnológico)
- [Desarrollo](#desarrollo)
- [Licencia](#licencia)

## 🎯 Descripción

**Cripto Analizador Pro** es una aplicación web moderna construida con Next.js 16 y React 19 que proporciona análisis técnico profesional de criptomonedas. La plataforma combina gráficos interactivos en tiempo real, indicadores técnicos avanzados e interfaces intuitivas para traders de todos los niveles.

### 🎯 Objetivo Principal

Democratizar el análisis técnico de criptomonedas con una interfaz moderna, responsive y fácil de usar que eduque a principiantes y proporcione herramientas profesionales para traders experimentados.

## ✨ Características

### 📊 Análisis Técnico
- ✅ **Gráficos interactivos** con Recharts
- ✅ **15+ indicadores técnicos** (RSI, MACD, Bollinger Bands, etc.)
- ✅ **Análisis de tendencias** en múltiples timeframes
- ✅ **Detección de patrones** automática
- ✅ **Comparación múltiple** de criptomonedas

### 🎨 Interfaz de Usuario
- 📱 **Diseño 100% responsive** para móviles, tablets y desktops
- 🌓 **Modo oscuro/claro** integrado con next-themes
- ⚡ **Interfaz moderna** con shadcn/ui y Tailwind CSS
- 🎯 **UX intuitiva** y fácil de navegar
- ♿ **Accesible** (WCAG compliant)

### ⚙️ Infraestructura Moderna
- 🚀 **Next.js 16** con App Router
- ⚛️ **React 19.2** con características canary
- 📦 **Turbopack** como bundler por defecto
- 🔧 **TypeScript** para type safety
- 📊 **Recharts** para visualizaciones

### 🧠 Funcionalidades Avanzadas
- 📚 **Explicaciones educativas** de indicadores
- 💡 **Señales de compra/venta** automáticas
- 🔔 **Sistema de alertas** configurable
- 📈 **Backtesting** de estrategias
- 📋 **Exportación de datos** en múltiples formatos

## 📋 Requisitos Previos

- **Node.js** 18.17.0 o superior
- **npm** 9.0 o **yarn** 4.0 o **pnpm** 9.0
- Navegador moderno (Chrome, Firefox, Safari, Edge)

## 🚀 Instalación

### Opción 1: Con shadcn CLI (Recomendado)

```bash
# Instalar globalmente shadcn CLI
npm install -g shadcn-ui

# Crear nuevo proyecto
shadcn-ui init

# Cuando solicite, clonar este repositorio
# o descargar el ZIP y extraerlo
```

### Opción 2: Clonación Manual

```bash
# Clonar el repositorio
git clone https://github.com/KeikoBernal/cripto-analizador-pro.git
cd cripto-analizador-pro

# Instalar dependencias
npm install
# o
yarn install
# o
pnpm install

# Ejecutar servidor de desarrollo
npm run dev
# o
yarn dev
# o
pnpm dev
```

La aplicación estará disponible en `http://localhost:3000`

### Instalación en GitHub

También puedes usar este repositorio como template:

```bash
# Crear repo desde template
gh repo create tu-nuevo-repo --template KeikoBernal/cripto-analizador-pro
```

## 📁 Estructura del Proyecto

```
cripto-analizador-pro/
│
├── 📁 app/                    # Next.js App Router
│   ├── layout.tsx             # Layout raíz
│   ├── page.tsx               # Página principal
│   └── ...
│
├── 📁 components/             # Componentes React
│   ├── 📁 ui/                 # Componentes shadcn/ui
│   ├── dashboard/             # Componentes del dashboard
│   ├── charts/                # Componentes de gráficos
│   └── ...
│
├── 📁 hooks/                  # Custom React hooks
│   ├── use-mobile.ts          # Detectar dispositivo móvil
│   └── use-toast.ts           # Sistema de notificaciones
│
├── 📁 lib/                    # Utilidades y funciones
│   ├── utils.ts               # Funciones auxiliares
│   └── ...
│
├── 📁 public/                 # Archivos estáticos
│
├── 🎨 app/globals.css         # Estilos globales con Tailwind v4
├── 📝 package.json            # Dependencias del proyecto
├── ⚙️ next.config.mjs         # Configuración de Next.js
├── 📘 tsconfig.json           # Configuración de TypeScript
└── 📖 README.md               # Este archivo
```

## 💻 Uso

### Modo Desarrollo

```bash
# Iniciar servidor con hot reload
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

### Modo Producción

```bash
# Compilar aplicación
npm run build

# Iniciar servidor producción
npm run start
```

### Linting

```bash
# Revisar código
npm run lint
```

## 🛠️ Stack Tecnológico

### Frontend
- **Next.js 16** - Framework React con SSR/SSG
- **React 19.2** - UI library con características canary
- **TypeScript 5** - Type safety
- **Tailwind CSS 4** - Utility-first CSS framework
- **shadcn/ui** - Componentes de UI reutilizables
- **Recharts 2** - Gráficos y visualizaciones

### UI & Estilos
- **Radix UI** - Primitivos accesibles
- **Lucide React** - Iconografía
- **Sonner** - Sistema de notificaciones (toasts)
- **next-themes** - Soporte de modo oscuro/claro
- **tailwindcss-animate** - Animaciones

### Validación & Formularios
- **React Hook Form 7** - Gestión de formularios
- **Zod 3** - Validación de esquemas TypeScript
- **@hookform/resolvers** - Integradores de validadores

### Componentes Especializados
- **Embla Carousel** - Carruseles accesibles
- **React Day Picker** - Selectores de fecha
- **React Resizable Panels** - Paneles redimensionables
- **cmdk** - Menú de comandos
- **vaul** - Drawers (paneles deslizables)

## 🔨 Desarrollo

### Scripts Disponibles

```bash
# Desarrollo con hot reload
npm run dev

# Compilación para producción
npm run build

# Iniciar servidor producción
npm run start

# Análisis y linting
npm run lint
```

### Agregar Componentes shadcn/ui

```bash
# Instalar componente específico
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
# ... y más
```

### Variables de Entorno

Crear archivo `.env.local`:

```env
# Agregar variables según sea necesario
# Ejemplo:
# NEXT_PUBLIC_API_URL=https://api.ejemplo.com
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Vercel** por Next.js y Vercel AI
- **React** por la excelente library
- **Shadcn** por los componentes increíbles
- **Recharts** por las visualizaciones
- **Tailwind Labs** por Tailwind CSS
- **La comunidad open source** por las herramientas y librerías

---

<div align="center">

### ⭐ Si este proyecto te fue útil, ¡dale una estrella!

### 🚀 Hecho con ❤️ para la comunidad de crypto traders

**Conecta:** [Twitter](https://twitter.com) | [LinkedIn](https://linkedin.com) | [GitHub](https://github.com/KeikoBernal)

</div>
