# 📚 LÉCTURA PRO — PAES 2027

Aplicación web con IA para estudiantes chilenos que se preparan para la **PAES Competencia Lectora** (30 de noviembre de 2026).

---

## ¿Qué hace la app?

| Módulo | Descripción |
|---|---|
| 🏛️ **Ensayo DEMRE** | Simulador oficial de 65 preguntas con textos reales |
| ⚡ **Práctica Rápida** | Textos cortos con feedback inmediato generados por IA |
| 🎁 **Prueba Gratis** | Acceso sin registro para probar la app |
| 📋 **Ensayos Oficiales** | Pruebas DEMRE reales de años anteriores |
| 📈 **Mi Progreso** | Estadísticas por habilidad (Localizar / Interpretar / Evaluar) |
| 🕒 **Mi Historial** | Revisión pregunta a pregunta de intentos anteriores |

---

## Tecnologías

- **Frontend/Backend:** [Streamlit](https://streamlit.io/)
- **IA:** Google Gemini 2.5 Flash
- **Base de datos:** MongoDB Atlas
- **Despliegue:** Streamlit Cloud (GitHub → auto-deploy)

---

## Cómo correr la app localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/Felipe10893/lectura-paes.git
cd lectura-paes

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear archivo .env con las credenciales
MONGO_URI=tu_uri_de_mongodb_atlas
GEMINI_API_KEY=tu_api_key_de_gemini

# 4. Correr la app
streamlit run main.py
```

---

## Estructura del proyecto

```
0_App_PAES/
├── main.py               # Enrutador principal y lógica de pantallas
├── ui_components.py      # CSS, HTML, componentes visuales
├── database.py           # Conexión MongoDB Atlas
├── gemini_service.py     # Llamadas a la API de Gemini
├── evaluacion_service.py # Cálculo de estadísticas y evaluación
├── home_redesign.html    # Dashboard principal (wireframe)
├── img/                  # Videos e imágenes
├── requirements.txt      # Dependencias Python
└── .env                  # Variables de entorno (NO subir a GitHub)
```

---

## Variables de entorno requeridas

| Variable | Descripción |
|---|---|
| `MONGO_URI` | URI de conexión a MongoDB Atlas (SRV) |
| `GEMINI_API_KEY` | API Key de Google Generative AI |

---

## Historial de versiones

| Versión | Fecha | Descripción |
|---|---|---|
| v1.0 | 2026-04-26 | Lanzamiento inicial con todas las pantallas principales |

---

## Equipo

Desarrollado por **Felipe Marchant** · [@Felipe10893](https://github.com/Felipe10893)
