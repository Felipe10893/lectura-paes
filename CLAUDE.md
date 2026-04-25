# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LÉCTURA PRO - PAES 2027** is an AI-powered web app for Chilean high school students preparing for the PAES reading comprehension exam (scheduled November 30, 2026). It combines Gemini AI-generated practice content, official DEMRE exam simulation, and MongoDB-persisted student history.

## Commands

```bash
# Run the app
streamlit run main.py

# Install dependencies
pip install -r requirements.txt

# Create a backup ZIP (excludes .venv, __pycache__, .git)
python hacer_respaldo.py
```

**Required environment variables** (in `.env`):
- `MONGO_URI` — MongoDB Atlas SRV connection string
- `GEMINI_API_KEY` — Google Generative AI API key

## Architecture

The app is a **Streamlit monolith** with session-state-based navigation. There are no separate page files — routing is handled in `main.py` via `st.session_state["pantalla_actual"]`.

### Core Files

| File | Role |
|---|---|
| `main.py` | Entry point, page router, Gemini AI calls, admin panel |
| `ui_components.py` | All CSS/HTML injection, component renderers, dark mode system |
| `database.py` | MongoDB Atlas connection with DNS workaround and `@st.cache_resource` |

### Navigation / Screen States

The app routes between 6 screens via `st.session_state["pantalla_actual"]`:
1. `"principal"` — Dashboard with countdown to PAES, XP bar, streak
2. `"ensayos_demre"` — Official exam simulator (3-state machine: biblioteca → ejecución → resultados)
3. `"modo_lectura"` — AI-generated or banco express practice (targeted by skill weakness)
4. `"historial"` — Past attempts with question-by-question review
5. `"progreso"` — Analytics stub (placeholder)
6. `"configuracion"` — Difficulty settings + admin panel (password: `ADMIN_DEMRE_2027`)

### Data Layer (MongoDB)

Database: `paes_lectura_db` on MongoDB Atlas.

Collections:
- `ensayos_historial` — Student test/practice attempt records (score, answers, skill breakdown)
- `ensayos_oficiales` — Official DEMRE exam templates (65 questions, stored as structured documents)

Connection uses custom DNS (8.8.8.8) to bypass Chilean ISP blocking of MongoDB SRV records.

### AI Integration (Gemini)

`main.py` calls `google.generativeai` (model: `gemini-2.5-flash`) to:
- Generate full 65-question official-style exams (admin panel)
- Generate 3-question targeted practice texts on demand (Modo Lectura → Práctica Dirigida)
- Generate express banco texts in batch

All Gemini calls return strict JSON. There is exponential backoff retry logic (max 5 retries) for rate-limit errors.

### Session State Conventions

All user data lives in `st.session_state`. Key state variables:
- `estudiante_nombre`, `estudiante_rut` — Multi-tenant user identity (no auth system)
- `modo_ensayo_estado` — Controls the 3-state machine within Ensayos DEMRE (`"biblioteca"`, `"ejecucion"`, `"resultados"`)
- `respuestas_actuales` — Dict of question index → selected answer during active test
- `xp_total`, `racha_dias` — Gamification state

### Styling System

All CSS lives in `ui_components.py` and is injected via `st.markdown(..., unsafe_allow_html=True)`. The design system uses CSS custom properties for theming (light/dark mode). Dark mode is toggled via session state and persisted in localStorage via injected JS.

### DEMRE Skill Taxonomy

Content is tagged by official PAES learning objectives:
- `localizar` — Locate explicit information
- `interpretar` — Interpret meaning and inference
- `evaluar` — Evaluate and critically assess text

Skill performance is tracked per attempt and used by Práctica Dirigida to target weak areas.

---

## Protocolo de Auditoría Total

Estas reglas se aplican a **todas** las respuestas en este proyecto, sin excepción.

### 1. Código completo — cero placeholders

Nunca escribir comentarios como `# ... resto del código`, `# igual que antes`, `# tu código aquí`, o cualquier omisión implícita. Cada bloque de código entregado debe ser **ejecutable tal como está**. Si un archivo tiene 800 líneas y hay que cambiar 3, se entrega el archivo completo con el cambio aplicado.

### 2. Formato de Reemplazo (usuario no programador)

El usuario no sabe dónde pegar fragmentos de código. Por eso, cada modificación se entrega así:

```
ARCHIVO: nombre_del_archivo.py
REEMPLAZA EXACTAMENTE ESTO:
<bloque original, copiable>SS

POR ESTO:
<bloque nuevo, copiable>
```

Si el cambio es en un archivo completo, se indica `REEMPLAZA EL ARCHIVO COMPLETO` y se entrega el contenido íntegro. Nunca asumir que el usuario sabe identificar el lugar correcto por contexto.

### 3. Estética Apple / Notion

Todo elemento visual nuevo debe respetar el sistema de diseño existente en `ui_components.py`:
- Colores definidos como CSS custom properties (`--color-*`)
- Tipografía: SF Pro / Inter / sistema sans-serif
- Bordes redondeados (`border-radius: 12px–20px`), sombras sutiles (`box-shadow` con baja opacidad)
- Sin gradientes agresivos; usar glassmorphism con moderación
- Dark mode compatible por defecto — todo color hardcodeado es un error
- Animaciones suaves (`transition: 0.2s ease`), nunca llamativas

### 4. Antes de cualquier cambio: leer primero

Siempre leer el archivo completo antes de proponer modificaciones. No sugerir cambios basados en suposiciones sobre el contenido actual.

### 5. Cierre obligatorio de cada tarea

Al finalizar cualquier tarea, una vez que todos los cambios hayan sido aplicados, terminar SIEMPRE la respuesta con esta línea exacta:

✅ TODO LISTO - Puedes recargar el navegador con F5

### 6. Modo de Ejecución Automática

- Siempre usar auto-accept para todos los cambios sin pedir confirmación
- Nunca preguntar "Do you want to proceed?" ni "Do you want to make this edit?"
- Ejecutar todos los cambios directamente sin interrupciones
- El usuario siempre aprueba, nunca es necesario confirmar

### 7. Códigos de Respuesta del Usuario

El usuario usa códigos numéricos cortos para dar feedback sin escribir texto largo:

- **1** = Continúa / procede con el siguiente paso
- **4** = Así quedó bien / aprobado
- **7** = No lo veo / no funcionó / hay un problema

Al final de **CADA** respuesta siempre incluir este recordatorio en una línea separada:

---
1 continúa | 4 así quedó | 7 no lo veo
