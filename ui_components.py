import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os
import base64

# ==============================================================================
# LIBRERÍA DE COMPONENTES VISUALES Y CSS (ESTÉTICA APPLE / NOTION / DUOLINGO)
# ==============================================================================

CSS_GLOBAL = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

/* 1. Normalización Segura y Reseteo Base */
*, *::before, *::after { box-sizing: border-box!important; }

html, body {
    margin: 0; padding: 0; overflow-x: hidden!important; touch-action: pan-y;
    transition: background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* --- SISTEMA DE DESIGN TOKENS: TEMA CLARO Y MODO OSCURO --- */
:root {
    --bg-color: #F0F4FF;
    --text-color: #000000;
    --card-bg: #FFFFFF;
    --card-border: #E2E8F0;
    --pill-marquee-bg: linear-gradient(90deg, #FF6B00, #FF8C00);
    --dark-widget-bg: #0D1117;
    --dark-widget-text: #FFFFFF;
    --dark-widget-border: #1F7AFF;
    
    /* Dashboard Modular Colors */
    --dash-alert-bg: #FEF2F2;        
    --dash-alert-border: #FCA5A5;
    --dash-alert-text: #991B1B;
    --dash-callout-bg: #F0FDF4;      
    --dash-callout-border: #86EFAC;
    --dash-callout-text: #166534;
    --dash-streak-bg: #FFF7ED;       
    --dash-streak-border: #FDBA74;
    --dash-streak-text: #C2410C;
    --dash-quote-bg: #F8FAFC;        
    --dash-quote-border: #E2E8F0;
    --dash-quote-text: #475569;
}

body.dark-mode {
    --bg-color: #111827;
    --text-color: #F3F4F6;
    --card-bg: #1F2937;
    --card-border: #374151;
    --pill-marquee-bg: linear-gradient(90deg, #CC8400, #CC5200);
    --dark-widget-bg: #03060a;
    --dark-widget-text: #E5E7EB;
    --dark-widget-border: #1F7AFF;
    
    /* Dashboard Modular Colors (Dark Mode) */
    --dash-alert-bg: #450A0A;
    --dash-alert-border: #991B1B;
    --dash-alert-text: #FECACA;
    --dash-callout-bg: #052E16;
    --dash-callout-border: #166534;
    --dash-callout-text: #BBF7D0;
    --dash-streak-bg: #431407;
    --dash-streak-border: #C2410C;
    --dash-streak-text: #FED7AA;
    --dash-quote-bg: #0F172A;
    --dash-quote-border: #334155;
    --dash-quote-text: #CBD5E1;
}

/* Modificadores de Infraestructura Streamlit */
[data-testid="stApp"] {
    background: linear-gradient(160deg, #f8f9fc 0%, #eef0f7 50%, #e4e7f2 100%) !important;
    background-attachment: fixed!important;
    color: var(--text-color); font-family: 'Plus Jakarta Sans', sans-serif; display: flex!important; flex-direction: column!important; min-height: 100vh!important; overflow-x: hidden!important;
}

[data-testid="stSidebar"] {
    background: unset!important;
    background-color: #f0f2f6!important;
    border-right: 3px solid #6366f1 !important;
}

/* OCULTAR COMPLETAMENTE TODOS LOS ELEMENTOS DE CABECERA DE STREAMLIT */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stApp > header,
header { display: none!important; height: 0!important; min-height: 0!important; overflow: hidden!important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}

/* SOBREESCRIBIR VARIABLE CSS INTERNA DE STREAMLIT QUE RESERVA ALTURA DEL HEADER */
:root,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    --header-height: 0px !important;
    --decoration-height: 0px !important;
}

/* SUBIR TODO EL CONTENIDO: margen negativo compensa la altura del header oculto */
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"] {
    margin-top: -9.5rem !important;
    padding-top: 0 !important;
}

[data-testid="stMain"],
section.main,
.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* 🛡️ FIX DEFINITIVO: FORZAR PANTALLA COMPLETA TOTAL (EDGE-TO-EDGE LIMPIO) */
div.block-container,
div[data-testid="stAppViewBlockContainer"],
div[data-testid="block-container"] {
    padding-top: 0.5rem !important;
    padding-bottom: 50px!important;
    padding-left: 2rem!important;
    padding-right: 2rem!important;
    max-width: 100%!important;
    width: 100%!important;
    background: linear-gradient(160deg, #f8f9fc 0%, #eef0f7 50%, #e4e7f2 100%) !important;
}

/* 🟢 CLASES GLOBALES DE LA BARRA SUPERIOR Y NÚMEROS DE PÁGINA */
@keyframes pulseGreen { 0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); } 70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); } 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); } }
.fixed-home { position: fixed; top: 12px; left: 2rem; z-index: 9999; display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: #475569; font-family: 'Plus Jakarta Sans', sans-serif; }
.fixed-home .home-tag { background: rgba(255,255,255,0.85); border: 1px solid #e2e8f0; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); color: #475569; padding: 6px 14px; border-radius: 8px; }
.fixed-clock { position: fixed; top: 8px; left: 50%; transform: translateX(-50%); z-index: 9999; display: flex; flex-direction: column; align-items: center; background: rgba(255,255,255,0.85); border: 1px solid #e2e8f0; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); padding: 6px 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-family: 'Plus Jakarta Sans', sans-serif; }
.fixed-clock .clock-time { font-size: 13px; font-weight: 800; color: #1e1b4b; }
.fixed-clock .clock-countdown { font-size: 11px; font-weight: 800; color: #ef4444; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 2px; }
.fixed-status { position: fixed; top: 12px; right: 180px; z-index: 9999; display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 800; color: #475569; background: rgba(255,255,255,0.85); border: 1px solid #e2e8f0; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); padding: 6px 14px; border-radius: 20px; letter-spacing: 0.5px; font-family: 'Plus Jakarta Sans', sans-serif; }
.fixed-status .status-dot { width: 8px; height: 8px; background-color: #22C55E; border-radius: 50%; animation: pulseGreen 2s infinite; }

/* 🟢 COMPONENTE NÚMERO DE PÁGINA */
.page-badge {
    background: linear-gradient(135deg, #1F7AFF, #8A2BE2);
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-left: 8px;
    box-shadow: 0 2px 6px rgba(31, 122, 255, 0.3);
    display: inline-block;
}

/* --- ARQUITECTURA DEL DASHBOARD SUPERIOR --- */
.top-dashboard-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px!important;
    margin-bottom: 60px!important;
    margin-top: 25px!important;
    width: 100%;
}

.dash-card {
    border-radius: 16px;
    padding: 24px!important; 
    min-height: 200px!important; 
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.dash-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.15);
}

.dash-title { 
    font-size: 16px!important; 
    font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; 
    margin-bottom: 14px!important; display: flex; align-items: center; gap: 8px; 
}
.dash-content { 
    font-size: 15px!important; 
    font-weight: 500; line-height: 1.5!important; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;
}
.dash-highlight { font-weight: 800; }

.card-alert { background-color: var(--dash-alert-bg); border: 1px solid var(--dash-alert-border); color: var(--dash-alert-text); }
.card-callout { background-color: var(--dash-callout-bg); border: 1px solid var(--dash-callout-border); color: var(--dash-callout-text); border-left: 5px solid #22C55E; }
.card-streak { background-color: var(--dash-streak-bg); border: 1px solid var(--dash-streak-border); color: var(--dash-streak-text); }
.card-quote { background-color: var(--dash-quote-bg); border: 1px solid var(--dash-quote-border); color: var(--dash-quote-text); border-left: 5px solid #1F7AFF; }

@keyframes fireBounce {
    0%, 100% { transform: scale(1) translateY(0); filter: drop-shadow(0 0 4px rgba(249, 115, 22, 0.4)); }
    50% { transform: scale(1.15) translateY(-3px); filter: drop-shadow(0 0 12px rgba(249, 115, 22, 0.85)); }
}
.fire-icon {
    display: inline-block; font-size: 20px; animation: fireBounce 1.5s infinite ease-in-out; transform-origin: bottom center; will-change: transform, filter; 
}

.xp-bar-container { width: 100%; height: 8px; background-color: rgba(0,0,0,0.08); border-radius: 4px; margin-top: 10px; overflow: hidden; position: relative; }
body.dark-mode .xp-bar-container { background-color: rgba(255,255,255,0.1); }
.xp-bar-fill { height: 100%; background: linear-gradient(90deg, #F59E0B, #F97316); border-radius: 4px; width: 85%; box-shadow: inset 0 -2px 0 rgba(0,0,0,0.15); position: relative; }

.badge-cupos {
    background: #DC2626; color: white; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 900; 
    position: absolute; top: 16px; right: 16px; animation: pulseRed 2s infinite cubic-bezier(0.4, 0, 0.6, 1); letter-spacing: 0.5px;
}
@media (max-width: 1024px) { .top-dashboard-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) {
    .block-container, [data-testid="block-container"], [data-testid="stAppViewBlockContainer"] { padding-left: 1rem!important; padding-right: 1rem!important; }
    .stColumns { flex-direction: column!important; gap: 1rem!important; }
    div[data-testid="stColumn"] { width: 100%!important; margin-bottom: 0.5rem; }
    .top-dashboard-grid { grid-template-columns: 1fr; gap: 12px; margin-top: 15px; margin-bottom: 20px; }
    .header-container { flex-direction: column; align-items: flex-start; gap: 10px; }
    .tarjeta-apple { min-height: 120px!important; }
    h1[style*="font-size:clamp"] { font-size: 26px!important; margin-bottom: 8px!important; }
}
</style>
"""

# ==============================================================================
# BLOQUES AUXILIARES RECUPERADOS
# ==============================================================================

CSS_CONFIGURACION = """
<style>
.back-btn-wrapper button { border-radius: 999px!important; width: auto!important; height: 45px!important; padding: 0 24px!important; display: inline-flex!important; align-items: center!important; justify-content: center!important; font-size: 16px!important; font-weight: 800!important; background: var(--card-bg)!important; color: #475569!important; border: 2px solid var(--card-border)!important; box-shadow: 0 2px 4px rgba(0,0,0,0.02)!important; transition: all 0.3s ease!important; letter-spacing: 0.5px!important; }
.back-btn-wrapper button:hover { background: var(--bg-color)!important; border-color: #1F7AFF!important; color: #1F7AFF!important; box-shadow: 0 4px 12px rgba(31, 122, 255, 0.15)!important; transform: translateY(-2px)!important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { background-color: var(--card-bg)!important; border: none!important; border-radius: 12px!important; padding: 16px!important; font-family: 'Plus Jakarta Sans', sans-serif!important; font-size: 16px!important; line-height: 1.6!important; color: var(--text-color)!important; font-weight: 500!important; box-shadow: none!important; outline: none!important; }
.stTextInput > div > div, .stTextArea > div > div { background-color: var(--card-bg)!important; border: 1px solid var(--card-border)!important; border-radius: 12px!important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)!important; }
.stTextInput > div > div:focus-within, .stTextArea > div > div:focus-within { border-color: #1F7AFF!important; box-shadow: 0 0 0 3px rgba(31, 122, 255, 0.15), 0 0 15px rgba(31, 122, 255, 0.2)!important; }
</style>
"""

CABECERA_PREMIUM = """
<div style="background: var(--card-bg); padding: 25px 30px; border-radius: 20px; border: 1px solid var(--card-border); box-shadow: 0 10px 30px -10px rgba(31, 122, 255, 0.1); margin-top: -15px;">
<h2 style='margin: 0; font-weight: 900; font-size: 30px; display: flex; align-items: center; gap: 12px; background: linear-gradient(135deg, #1F7AFF, #8A2BE2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
<span style="font-size: 32px; -webkit-text-fill-color: initial;">🧠</span> Entrenamiento PAES Activo
</h2>
<p style='margin: 8px 0 0 0; color: #64748B; font-size: 16px; font-weight: 600; line-height: 1.6;'>Configura tu motor de Inteligencia Artificial. Al pegar tu material de estudio, el entorno inmersivo de lectura profunda se abrirá automáticamente.</p>
</div>
"""

HEADER_MATERIAL_ESTUDIO = """
<div style="display: flex; align-items: center; gap: 18px; margin-bottom: 20px;">
<div style="background: linear-gradient(135deg, #FEF3C7, #FDE68A); width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5), 0 4px 6px rgba(0,0,0,0.05);">
<span style="font-size: 24px;">📝</span>
</div>
<div>
<h3 style="margin: 0; color: var(--text-color); font-size: 20px; font-weight: 800; letter-spacing: -0.5px;">Material de Estudio</h3>
<p style="margin: 2px 0 0 0; color: #64748B; font-size: 15px; font-weight: 500;">Pega el texto a analizar. La IA iniciará el entorno sola.</p>
</div>
</div>
"""

BTN_NUEVO_TEXTO_CSS = """
<style>
.btn-nuevo-texto button { border-radius: 12px!important; font-weight: 800!important; color: #EF4444!important; background: #FEF2F2!important; border: 1px solid #FCA5A5!important; height: 45px!important; margin-top: 5px!important; transition: all 0.3s ease!important; }
.btn-nuevo-texto button:hover { background: #FEE2E2!important; transform: translateY(-2px)!important; }
</style>
"""

JS_SENSOR_PASTE = """
<script>
const doc = window.parent.document;
const observer = new MutationObserver(() => {
    const textarea = doc.querySelector('textarea');
    if (textarea && !textarea.dataset.listenerSet) {
        textarea.dataset.listenerSet = "true";
        textarea.addEventListener('paste', () => { setTimeout(() => { textarea.blur(); }, 100); });
    }
});
observer.observe(doc.body, { childList: true, subtree: true });
</script>
"""

CSS_BTN_ENTRADA = """
<style>
@keyframes pulseGiant { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(31, 122, 255, 0.7); } 50% { transform: scale(1.03); box-shadow: 0 0 30px 10px rgba(31, 122, 255, 0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(31, 122, 255, 0); } }
.stButton > button { animation: pulseGiant 1.5s infinite cubic-bezier(0.4, 0, 0.2, 1)!important; height: 4em!important; font-size: 20px!important; font-weight: 900!important; border-radius: 16px!important; background: linear-gradient(135deg, #1F7AFF, #8A2BE2)!important; border: 2px solid #FFFFFF!important; color: white!important; text-transform: uppercase!important; letter-spacing: 1px!important; margin-top: 15px!important; }
</style>
"""

CSS_SPLIT_VIEW = """
<style>
/* Estilos vitales para la vista de ensayo dividido */
.scrollable-text-panel { 
    background-color: var(--card-bg); border: 1px solid var(--card-border); 
    border-radius: 16px; padding: 35px 45px; height: 65vh; overflow-y: auto; 
    position: sticky; top: 10px; font-family: 'Merriweather', serif; 
    line-height: 1.8; color: var(--text-color); box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); 
}
.scrollable-text-panel::-webkit-scrollbar { width: 8px; }
.scrollable-text-panel::-webkit-scrollbar-thumb { background-color: #CBD5E1; border-radius: 10px; }

/* Tarjetas de opciones en preguntas */
.stRadio > div { gap: 12px; }
.stRadio > div > label {
    background-color: var(--card-bg); border: 1px solid var(--card-border);
    padding: 15px 20px; border-radius: 12px; cursor: pointer; transition: all 0.2s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02); font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 500;
}
.stRadio > div > label:hover { border-color: #1F7AFF; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(31,122,255,0.1); }

/* Resultados Feedbacks */
.result-card { padding: 24px; border-radius: 16px; margin-bottom: 20px; background: var(--card-bg); border: 1px solid var(--card-border); box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
.result-card.correct { border-left: 8px solid #22C55E; }
.result-card.incorrect { border-left: 8px solid #EF4444; }
.explanation-box { background: var(--bg-color); border-radius: 8px; padding: 15px; margin-top: 15px; border: 1px dashed var(--card-border); font-size: 14px; color: var(--text-color); }
</style>
"""

def obtener_html_lector_activo(texto_html_seguro):
    return f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;800&family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">
<style>
html, body {{ background-color: var(--bg-color); margin: 0; padding: 0; height: 100vh; overflow: hidden; color: var(--text-color); }}
.layout-master {{ display: flex; gap: 40px; max-width: 100%; width: 100%; margin: 0 auto; padding: 20px 40px; height: 100%; box-sizing: border-box; align-items: flex-start; }}
.contenedor-hoja {{ flex: 1; min-width: 0; height: 100%; overflow-y: auto; padding-right: 20px; padding-bottom: 60px; }}
.panel-lateral {{ width: 320px; flex-shrink: 0; }}
.caja-instrucciones {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 20px; padding: 30px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }}
.caja-instrucciones h4 {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 800; color: var(--text-color); margin: 0 0 15px 0; display: flex; align-items: center; gap: 8px; }}
.caja-instrucciones p {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #64748B; line-height: 1.6; margin: 0 0 25px 0; }}
.btn-tool {{ font-family: 'Plus Jakarta Sans', sans-serif; background: var(--card-bg); border: 2px solid var(--card-border); border-radius: 12px; padding: 14px 18px; font-size: 16px; font-weight: 800; color: #475569; cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); display: flex; align-items: center; gap: 12px; width: 100%; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
.btn-tool:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.06); color: #1F7AFF; border-color: #1F7AFF; }}
.btn-tool.yellow:hover {{ border-color: #FDE047; color: #CA8A04; background: #FEF9C3; }}
.btn-tool.circle:hover {{ border-color: #FCA5A5; color: #DC2626; background: #FEF2F2; }}
.btn-tool.clear:hover {{ border-color: #9CA3AF; color: var(--text-color); background: #F3F4F6; }}
.hoja-lectura {{ background: var(--card-bg); border-radius: 20px; padding: 60px 80px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.05); border: 1px solid var(--card-border); font-family: 'Merriweather', 'Georgia', serif; font-size: 20px; line-height: 2.0; color: var(--text-color); text-align: justify; text-justify: inter-word; margin-bottom: 40px; }}
.highlight-yellow {{ background-color: rgba(253, 224, 71, 0.85); border-radius: 4px; padding: 2px 4px; box-shadow: 0 1px 3px rgba(253, 224, 71, 0.5); transition: background-color 0.2s; }}
.highlight-circle {{ border: 2px solid #EF4444; border-radius: 50%; padding: 2px 6px; display: inline-block; color: #B91C1C; font-weight: bold; background-color: rgba(239, 68, 68, 0.05); box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2); }}
</style>
</head>
<body>
<div class="layout-master">
<div class="contenedor-hoja"><div class="hoja-lectura" id="content-lectura">{texto_html_seguro}</div></div>
<div class="panel-lateral">
<div class="caja-instrucciones">
<h4><span style="font-size: 24px;">🛠️</span> Estudio Activo</h4>
<p><b>1.</b> Selecciona el texto.<br><b>2.</b> Aplica una herramienta.</p>
<button class="btn-tool yellow" onclick="applyFormat('highlight-yellow')"><span style="font-size:18px;">🟡</span> Destacar Idea</button>
<button class="btn-tool circle" onclick="applyFormat('highlight-circle')"><span style="font-size:18px;">⭕</span> Circular Conector</button>
<hr style="border: 0; border-top: 1px solid var(--card-border); margin: 20px 0;">
<p style="margin-bottom: 15px; color: #9CA3AF; font-size: 13px;">¿Te equivocaste?</p>
<button class="btn-tool clear" onclick="removeFormat()"><span style="font-size:18px;">🧹</span> Borrar Marca</button>
</div>
</div>
</div>
<script>
try {{
const theme = window.parent.localStorage.getItem('theme-lectura');
if (theme === 'dark') {{ document.body.classList.add('dark-mode'); }}
}} catch(e) {{}}

const contentDiv = document.getElementById('content-lectura');
const saveKey = 'lectura_pro_save';
try {{
const savedHtml = window.parent.localStorage.getItem(saveKey);
if(savedHtml && savedHtml.trim().length > 0) {{ contentDiv.innerHTML = savedHtml; }}
}} catch(e) {{ console.log("Memoria bloqueada"); }}

function saveState() {{ try {{ window.parent.localStorage.setItem(saveKey, contentDiv.innerHTML); }} catch(e) {{}} }}

function applyFormat(className) {{
const sel = window.getSelection(); 
if (!sel.rangeCount || sel.isCollapsed) return;

const range = sel.getRangeAt(0);
try {{
const span = document.createElement('span'); 
span.className = className; 
span.appendChild(range.extractContents()); 
range.insertNode(span); 
sel.removeAllRanges(); 
saveState();
}} catch(e) {{ 
alert("💡 Asegúrate de destacar oraciones dentro de un mismo párrafo."); 
}}
}}

function removeFormat() {{
const sel = window.getSelection(); 
if (!sel.rangeCount) return; 
let node = sel.anchorNode;

while(node && node !== contentDiv && node.nodeName !== "BODY") {{
if(node.nodeType === 1 && (node.classList.contains('highlight-yellow') || node.classList.contains('highlight-circle'))) {{
const textNode = document.createTextNode(node.textContent); 
node.parentNode.replaceChild(textNode, node); 
saveState(); 
return;
}}
node = node.parentNode;
}}
alert("💡 Instrucción: Selecciona encima del texto destacado y presiona Borrar Marca.");
}}
</script>
</body>
</html>
"""

# ==============================================================================
# CSS FINAL DE ENSAMBLADO (TAMAÑOS AJUSTADOS AL EQUILIBRIO)
# ==============================================================================

CSS_ESTILOS = CSS_GLOBAL + """
<style>
/* Diseño de la Tarjeta de Menú: PALETA SUAVE COORDINADA CON DASHBOARD */
.tarjeta-apple {
    border-radius: 20px;
    padding: 20px 10px;
    text-align: center;
    transition: all 0.2s ease;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    min-height: 135px; margin-bottom: 0!important;
    position: relative; overflow: hidden;
}

div[data-testid="stColumn"]:hover .tarjeta-apple,
div[data-testid="column"]:hover .tarjeta-apple {
    transform: translateY(-4px)!important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1)!important;
}
div[data-testid="stColumn"]:active .tarjeta-apple,
div[data-testid="column"]:active .tarjeta-apple {
    transform: translateY(2px) scale(0.98)!important; transition: all 0.1s ease;
}

/* Fondo y borde izquierdo por tarjeta */
.tarjeta-historial { background: #FEF2F2!important; border-left: 4px solid #FCA5A5!important; }
.tarjeta-lectura   { background: #FFF7ED!important; border-left: 4px solid #FDBA74!important; }
.tarjeta-demre     { background: #F0FDF4!important; border-left: 4px solid #86EFAC!important; }
.tarjeta-progreso  { background: #F0FDF4!important; border-left: 4px solid #86EFAC!important; }
.tarjeta-descargas { background: #F8FAFC!important; border-left: 4px solid #E2E8F0!important; }
.tarjeta-config    { background: #F8FAFC!important; border-left: 4px solid #E2E8F0!important; }

.icon-wrapper {
    font-size: 28px; margin-bottom: 8px;
    width: 52px; height: 52px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.3s ease;
}
div[data-testid="stColumn"]:hover .icon-wrapper { transform: scale(1.1) rotate(5deg); }
.title-text { font-weight: 800; font-size: 15px; color: #1a1a2e!important; margin-bottom: 4px; letter-spacing: -0.3px; }
.desc-text { font-size: 12px; color: #64748b!important; line-height: 1.3; font-weight: 500; }

/* ALINEACIÓN DEL BOTÓN INVISIBLE AJUSTADO AL NUEVO ALTO */
[data-testid="stButton"] { margin-top: -145px!important; position: relative!important; z-index: 999!important; }
[data-testid="stButton"] button { height: 145px!important; width: 100%!important; opacity: 0!important; cursor: pointer!important; padding: 0!important; margin: 0!important; }

/* btn_entrar: puente JS→Python, sin espacio visual */
[data-testid="stMarkdown"]:has(#btn-entrar-anchor) + * [data-testid="stButton"],
[data-testid="stMarkdown"]:has(#btn-entrar-anchor) + * [data-testid="stButton"] button {
    height: 0!important; min-height: 0!important; overflow: hidden!important;
    margin: 0!important; padding: 0!important; opacity: 0!important; pointer-events: none!important;
}

/* Altura y fuentes de las tarjetas base inferiores ajustadas */
.dash-card { min-height: 220px!important; padding: 24px!important; border-radius: 20px!important; }
.top-dashboard-grid { margin-top: 25px!important; margin-bottom: 50px!important; gap: 20px!important; }
.dash-title { font-size: 17px!important; margin-bottom: 14px!important; letter-spacing: -0.3px; }
.dash-content { font-size: 14.5px!important; }

/* Marquesina Header */
@keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.header-container { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-bottom: 10px; margin-top: -10px; }
.pill-marquee { flex: 1; overflow: hidden; background: var(--pill-marquee-bg); padding: 4px 20px; border-radius: 50px; border: 2px solid rgba(255, 255, 255, 0.4); box-shadow: inset 0 2px 4px rgba(0,0,0,0.1), 0 4px 10px rgba(255, 107, 0, 0.2); }
.marquee-track { display: flex; width: 200%; animation: marquee 20s linear infinite; }
.marquee-content { color: white; font-weight: 900; white-space: nowrap; width: 50%; letter-spacing: 1px; font-size: 13.5px; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }
</style>
"""

# ==============================================================================
# FUNCIÓN DE RENDERIZADO: LANDING PAGE (PANTALLA DE BIENVENIDA)
# ==============================================================================

def render_landing_page():
    """Pantalla de bienvenida. Se muestra antes del dashboard principal."""

    st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
div.block-container, div[data-testid="stAppViewBlockContainer"], div[data-testid="block-container"] {
    padding: 0 !important; max-width: 100% !important;
}
iframe { width: 100% !important; }
.stApp { padding: 0 !important; }
div[data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

    # Leer imagen de fondo y convertir a base64
    _img_data = ""
    _img_mime = "image/jpeg"
    for _p in ["img/fondo.jpg", "img/fondo.png"]:
        if os.path.exists(_p):
            with open(_p, "rb") as _f:
                _img_data = base64.b64encode(_f.read()).decode()
            _img_mime = "image/png" if _p.endswith(".png") else "image/jpeg"
            break
    _bg = (
        f"background-image:url('data:{_img_mime};base64,{_img_data}');"
        "background-size:cover;background-position:center;background-repeat:no-repeat;"
        if _img_data else
        "background:linear-gradient(160deg,#e8eaf6 0%,#9fa8da 100%);"
    )

    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap" rel="stylesheet">
<style>
html, body {{ margin: 0; padding: 0; height: 100%; overflow: hidden; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #111318; }}

/* NAVBAR */
.nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 10;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(255,255,255,0.35);
    padding: 18px 48px;
    display: flex; align-items: center; justify-content: space-between;
}}
.logo-wrap {{ display: flex; align-items: center; gap: 10px; }}
.logo-icon {{
    width: 36px; height: 36px; background: #1a237e; border-radius: 8px;
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; gap: 5px; padding: 9px; flex-shrink: 0;
}}
.logo-line {{ width: 100%; height: 2px; background: white; border-radius: 1px; }}
.logo-text {{ font-size: 16px; font-weight: 800; color: #1a237e; letter-spacing: -0.3px; }}
.nav-btn {{
    background: linear-gradient(135deg,#1a237e,#7c3aed); color: white; border: none;
    border-radius: 25px; padding: 10px 20px;
    font-size: 13px; font-weight: 700; cursor: pointer;
    font-family: 'Plus Jakarta Sans', sans-serif;
    transition: all 0.2s ease; white-space: nowrap;
}}
.nav-btn:hover {{ opacity: 0.9; transform: translateY(-1px); }}

/* HERO */
.hero {{
    height: 100vh; min-height: 1080px; width: 100%;
    position: relative;
    display: flex; align-items: center; justify-content: center;
}}
.hero-photo {{
    position: absolute; inset: 0;
    {_bg}
    background-size: cover; background-position: center;
    height: 100%; min-height: 1080px; width: 100%;
    filter: brightness(1.0);
    opacity: 0.16;
}}

.hero-content {{
    position: relative; z-index: 1;
    text-align: center; width: 100%; height: 100%;
}}
.hero-title {{
    font-size: 72px; font-weight: 900;
    color: #ffffff; letter-spacing: -1px; line-height: 1.15;
    margin-bottom: 20px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.45);
}}
.hero-sub {{
    font-size: 18px; color: #dce4ff; font-weight: 400;
    line-height: 1.7; margin-bottom: 40px;
    text-shadow: none;
}}
.btn-hero {{
    background: linear-gradient(135deg,#1a237e,#7c3aed); color: #ffffff; border: none;
    border-radius: 30px; padding: 18px 56px;
    font-size: 17px; font-weight: 800; letter-spacing: 0.6px;
    cursor: pointer; font-family: 'Plus Jakarta Sans', sans-serif;
    box-shadow: 0 4px 25px rgba(124,58,237,0.5);
    transition: all 0.2s ease; text-transform: uppercase;
}}
.btn-hero:hover {{ background: linear-gradient(135deg,#283593,#6d28d9); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(124,58,237,0.65); }}
.hero-welcome-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.45);
    border-radius: 999px;
    padding: 6px 18px;
    font-size: 12px; font-weight: 700; letter-spacing: 1.2px;
    color: white; text-transform: uppercase;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    margin-bottom: 6px;
}}
.hero-testimonial {{
    font-family: 'Caveat', cursive;
    font-size: 32px; font-weight: 700;
    color: #1a237e;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.8);
    margin-top: 10px;
}}
</style>
</head>
<body>

<div class="nav">
    <div class="logo-wrap">
        <div class="logo-icon">
            <div class="logo-line"></div>
            <div class="logo-line"></div>
            <div class="logo-line"></div>
        </div>
        <span class="logo-text">PAES Lenguaje</span>
    </div>
    <button class="nav-btn" onclick="window.parent.document.querySelectorAll('[data-testid=stButton] button')[0].click()">
        Crear Cuenta Gratuita
    </button>
</div>

<div class="hero">
    <div class="hero-photo"></div>
<div class="hero-content">
        <div style="position:absolute; left:3%; right:3%; top:45%; transform:translateY(-50%); background:rgba(13,27,90,0.45); padding-top:70px; padding-bottom:70px; padding-left:80px; padding-right:80px; width:94%; box-sizing:border-box; border-radius:24px;">
<h1 class="hero-title">Lenguaje PAES<br>Prepárate para el éxito</h1>
            <p class="hero-sub">Domina la comprensión lectora con ensayos oficiales DEMRE, práctica dirigida por IA y seguimiento de progreso en tiempo real.</p>
            <div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:32px;">
                <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:6px 16px; color:white; font-size:13px; font-weight:600;">Ensayos DEMRE</span>
                <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:6px 16px; color:white; font-size:13px; font-weight:600;">Motor IA Gemini</span>
                <span style="background:rgba(255,255,255,0.15); border-radius:20px; padding:6px 16px; color:white; font-size:13px; font-weight:600;">Análisis por Habilidad</span>
            </div>
            <button class="btn-hero" onclick="window.parent.document.querySelectorAll('[data-testid=stButton] button')[0].click()">
                INGRESA AQUÍ
            </button>
            <p style="color:rgba(255,255,255,0.5);font-size:13px;margin-top:14px">Acceso gratuito · Sin registro necesario</p>
        </div>
    </div>
    <div style="position:absolute; bottom:5%; left:50%; transform:translateX(-50%); width:80%; background:rgba(13,27,90,0.65); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); border-radius:16px; padding:28px 40px; display:flex; justify-content:space-around; align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:28px; font-weight:900; color:white; line-height:1.1;">+2.500</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.7); margin-top:6px; text-transform:uppercase; letter-spacing:0.5px;">Estudiantes</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:28px; font-weight:900; color:white; line-height:1.1;">850+</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.7); margin-top:6px; text-transform:uppercase; letter-spacing:0.5px;">Puntaje promedio</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:28px; font-weight:900; color:white; line-height:1.1;">65</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.7); margin-top:6px; text-transform:uppercase; letter-spacing:0.5px;">Preguntas</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:28px; font-weight:900; color:white; line-height:1.1;">100%</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.7); margin-top:6px; text-transform:uppercase; letter-spacing:0.5px;">DEMRE</div>
        </div>
    </div>
</div>

</body>
</html>
""", height=1050, scrolling=False)

    st.markdown("<style>div[data-testid='stButton']{position:fixed;bottom:-100px;opacity:0;pointer-events:none}</style>", unsafe_allow_html=True)
    if st.button("Entrar", key="btn_entrar"):
        st.session_state.pagina_actual = 'dashboard'
        st.rerun()
    st.stop()


# ==============================================================================
# FUNCIÓN DE RENDERIZADO DEL PANEL PRINCIPAL
# ==============================================================================


def render_interfaz_principal():
    from pathlib import Path

    # Ocultar botones proxy ANTES de que aparezcan en pantalla
    components.html("""<script>
(function(){
  function hideProxy(){
    try{
      window.parent.document.querySelectorAll('button').forEach(function(b){
        if((b.textContent||'').trim().startsWith('__NAV__')){
          var w=b.closest('[data-testid="stButton"]')||b.parentElement;
          if(w) w.style.cssText='height:0!important;overflow:hidden!important;margin:0!important;padding:0!important;min-height:0!important;';
        }
      });
    }catch(e){}
  }
  hideProxy();
  setTimeout(hideProxy,30);
  setTimeout(hideProxy,150);
  setTimeout(hideProxy,500);
})();
</script>""", height=0)

    # ------------------------------------------------------------------
    # BOTONES PROXY OCULTOS — el listener JS los clickea desde el iframe
    # ------------------------------------------------------------------
    NAV_MAP = [
        ("__NAV__Ensayos DEMRE",      "nav_demre",  "Ensayos DEMRE"),
        ("__NAV__Modo Lectura",        "nav_lect",   "Modo Lectura"),
        ("__NAV__Mi Historial",        "nav_hist",   "Mi Historial"),
        ("__NAV__Mi Progreso",         "nav_prog",   "Mi Progreso"),
        ("__NAV__Mis Descargas",       "nav_desc",   "Mis Descargas"),
        ("__NAV__Nivel de Dificultad", "nav_conf",   "Nivel de Dificultad"),
        ("__NAV__Prueba Gratis",        "nav_prueba",  "Prueba Gratis"),
        ("__NAV__Repositorio Admin",   "nav_repo",    "Repositorio Admin"),
        ("__NAV__Ensayos Oficiales",   "nav_ofic",    "Ensayos Oficiales"),
        ("__NAV__Practica Rapida",      "nav_pr",      "Practica Rapida"),
    ]
    for label, key, destino in NAV_MAP:
        if st.button(label, key=key):
            st.session_state.menu_actual = destino
            st.rerun()

    # ------------------------------------------------------------------
    # ATAJOS DE NAVEGACIÓN (fila superior, antes del wireframe)
    # ------------------------------------------------------------------
    sc1, sc2, sc3, sc4 = st.columns(4)
    nav_shortcuts = [
        (sc1, "🕒  Mi Historial",     "h_bt", "Mi Historial"),
        (sc2, "📈  Mi Avance",         "p_bt", "Mi Progreso"),
        (sc3, "🏆  Desafíos",          "d_bt", "Mis Descargas"),
        (sc4, "⚙️  Configuración",    "c_bt", "Nivel de Dificultad"),
    ]
    for col, label, key, screen in nav_shortcuts:
        with col:
            if st.button(label, key=key, use_container_width=True):
                st.session_state.menu_actual = screen
                st.rerun()

    # ------------------------------------------------------------------
    # WIREFRAME (diseño sketch con Kalam)
    # ------------------------------------------------------------------
    html_path = Path(__file__).parent / "home_redesign.html"
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        # Inyectar "video final.mp4" como base64 en el placeholder del hero
        video_path = Path(__file__).parent / "img" / "video final.mp4"
        if video_path.exists():
            import base64 as _b64
            video_b64 = _b64.b64encode(video_path.read_bytes()).decode()
            video_html = (
                f'<video autoplay loop muted playsinline '
                f'style="width:100%;height:100%;object-fit:cover;display:block;">'
                f'<source src="data:video/mp4;base64,{video_b64}" type="video/mp4">'
                f'</video>'
            )
            html_content = html_content.replace("<!--HERO_VIDEO_PLACEHOLDER-->", video_html)
        for jsx_file in ["design-canvas.jsx", "tweaks-panel.jsx", "sketch-kit.jsx",
                         "web-screens.jsx", "mobile-screens.jsx"]:
            jsx_path = Path(__file__).parent / jsx_file
            if jsx_path.exists():
                jsx_content = jsx_path.read_text(encoding="utf-8")
                html_content = html_content.replace(
                    f'<script type="text/babel" src="{jsx_file}"></script>',
                    f'<script type="text/babel">{jsx_content}</script>'
                )
        components.html(html_content, height=2200, scrolling=True)

    # ------------------------------------------------------------------
    # OYENTE: recibe postMessage del wireframe → clickea botón proxy
    # El wireframe ya envía: window.parent.postMessage({type:'lectoPAES_navigate', page:...})
    # ------------------------------------------------------------------
    components.html("""
<script>
(function () {
  var PREFIX = '__NAV__';

  // Mapeo de nombres usados en el wireframe → nombres de Streamlit
  var PAGE_MAP = {
    'Ensayos DEMRE':      'Ensayos DEMRE',
    'Modo Lectura':       'Modo Lectura',
    'Historial':          'Mi Historial',
    'Mi Progreso':        'Mi Progreso',
    'Desafios':           'Mis Descargas',
    'Perfil':             'Nivel de Dificultad',
    'Configuracion':      'Nivel de Dificultad',
    'Prueba Gratis':      'Prueba Gratis',
    'Ensayos Oficiales':  'Ensayos Oficiales',
    'Practica Rapida':    'Practica Rapida'
  };

  function hideProxyBtns() {
    try {
      window.parent.document.querySelectorAll('button').forEach(function (btn) {
        var txt = (btn.textContent || '').trim();
        if (txt.indexOf(PREFIX) === 0) {
          var wrap = btn.closest('[data-testid="stButton"]') || btn.parentElement;
          if (wrap) {
            wrap.style.cssText = 'height:0!important;overflow:hidden!important;'
              + 'margin:0!important;padding:0!important;line-height:0!important;';
          }
        }
      });
    } catch (e) {}
  }

  function clickProxy(streamlitPage) {
    try {
      var btns = window.parent.document.querySelectorAll('button');
      for (var i = 0; i < btns.length; i++) {
        if ((btns[i].textContent || '').trim() === PREFIX + streamlitPage) {
          btns[i].click();
          return;
        }
      }
    } catch (e) {}
  }

  // Ocultar botones proxy en cuanto carga el DOM
  setTimeout(hideProxyBtns, 100);
  setTimeout(hideProxyBtns, 500);
  setTimeout(hideProxyBtns, 1500);

  // Eliminar franja vacía superior directamente en el DOM padre
  function removeTopSpace() {
    try {
      var pd = window.parent.document;
      var hideSelectors = [
        '[data-testid="stHeader"]',
        '[data-testid="stToolbar"]',
        '[data-testid="stDecoration"]',
        '[data-testid="stStatusWidget"]'
      ];
      hideSelectors.forEach(function(sel) {
        var el = pd.querySelector(sel);
        if (el) el.style.cssText = 'display:none!important;height:0!important;min-height:0!important;overflow:hidden!important;';
      });
      var zeroSelectors = [
        '[data-testid="stMain"]',
        '[data-testid="stMainBlockContainer"]',
        'div.block-container'
      ];
      zeroSelectors.forEach(function(sel) {
        var el = pd.querySelector(sel);
        if (el) { el.style.paddingTop = '0px'; el.style.marginTop = '0px'; }
      });
    } catch(e) {}
  }
  setTimeout(removeTopSpace, 50);
  setTimeout(removeTopSpace, 300);
  setTimeout(removeTopSpace, 1000);

  // Escuchar mensajes enviados al padre por el wireframe
  try {
    window.parent.addEventListener('message', function (e) {
      if (!e.data || e.data.type !== 'lectoPAES_navigate') return;
      var page = PAGE_MAP[e.data.page] || e.data.page;
      clickProxy(page);
    });
  } catch (ex) {}
})();
</script>
""", height=0)



# ==============================================================================
# FUNCIÓN ENSAYOS DEMRE — SIMULADOR OFICIAL
# ==============================================================================

def render_ensayos_demre():
    from evaluacion_service import evaluar_respuestas

    fase = st.session_state.get("fase_examen", "configuracion")

    # ----------------------------------------------------------------
    # FASE 1 — BIBLIOTECA: seleccionar ensayo
    # ----------------------------------------------------------------
    if fase == "configuracion":
        st.markdown(
            "<h4 style='color: #64748B; margin-bottom: 20px; font-weight: 600;'>"
            "Selecciona un ensayo para comenzar tu entrenamiento:</h4>",
            unsafe_allow_html=True,
        )

        if not st.session_state.get("db_conectada", False):
            st.warning("⚠️ Sin conexión a la base de datos. No se pueden cargar los ensayos.")
            return

        ensayos = list(
            st.session_state.ensayos_oficiales_col.find(
                {"$or": [
                    {"tipo": "ensayo_completo"},
                    {"tipo": {"$exists": False}}
                ]}
            ).sort("_id", -1)
        )

        if not ensayos:
            st.info(
                "No hay ensayos oficiales cargados aún. El Administrador debe generar uno desde 'Configuración'."
            )
            return

        cols = st.columns(3, gap="large")
        for i, ens in enumerate(ensayos):
            eid = str(ens["_id"])
            titulo = ens.get("titulo", f"Ensayo Oficial #{i+1}")
            tiempo = ens.get("tiempo_limite", "02:30:00")
            num_preguntas = len(ens.get("preguntas", []))
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 16px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.3s; margin-bottom: 15px;">
                    <div style="background: #FEF2F2; color: #991B1B; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: 900; display: inline-block; margin-bottom: 15px; letter-spacing: 0.5px;">OFICIAL DEMRE</div>
                    <h3 style="margin: 0 0 10px 0; font-size: 20px; font-weight: 900; color: var(--text-color);">{titulo}</h3>
                    <p style="font-size: 13px; color: #64748B; margin: 0 0 25px 0; font-weight: 500;">⏱️ {tiempo} &nbsp; • &nbsp; 📝 {num_preguntas} Preguntas</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Iniciar Simulación 🚀", key=f"iniciar_ens_{eid}", type="primary", use_container_width=True):
                    st.session_state.ensayo_actual = ens
                    st.session_state.respuestas_usuario = {}
                    st.session_state.fase_examen = "ejecucion"
                    st.rerun()

    # ----------------------------------------------------------------
    # FASE 2 — EJECUCIÓN: responder el ensayo
    # ----------------------------------------------------------------
    elif fase == "ejecucion":
        ens = st.session_state.get("ensayo_actual")
        if not ens:
            st.session_state.fase_examen = "configuracion"
            st.rerun()
            return

        textos = ens.get("textos", {})
        preguntas = ens.get("preguntas", [])

        col_titulo, col_abandon = st.columns([4, 1])
        with col_titulo:
            st.markdown(f"## 📄 {ens.get('titulo', 'Ensayo DEMRE')}")
            respondidas = len(st.session_state.respuestas_usuario)
            st.caption(f"Respondidas: {respondidas} / {len(preguntas)}")
        with col_abandon:
            if st.button("⬅️ Abandonar", use_container_width=True):
                st.session_state.fase_examen = "configuracion"
                st.rerun()

        st.markdown("<hr style='border-top:1px dashed var(--card-border);margin:10px 0 20px 0;'>", unsafe_allow_html=True)

        tab_labels = [f"Texto {k}" for k in sorted(textos.keys(), key=lambda x: int(x) if x.isdigit() else x)]
        tabs = st.tabs(tab_labels) if tab_labels else []

        for tab_obj, t_key in zip(tabs, sorted(textos.keys(), key=lambda x: int(x) if x.isdigit() else x)):
            t_data = textos[t_key]
            pregs_texto = [p for p in preguntas if str(p.get("texto_id")) == str(t_key)]

            with tab_obj:
                col_texto, col_preguntas = st.columns([1.2, 1], gap="large")

                with col_texto:
                    st.markdown(
                        f"<h3 style='margin-bottom:16px;'>{t_data.get('titulo', f'Texto {t_key}')}</h3>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<div class='scrollable-text-panel'>{t_data.get('contenido', '')}</div>",
                        unsafe_allow_html=True,
                    )

                with col_preguntas:
                    st.markdown(f"#### Preguntas ({len(pregs_texto)})")
                    for i, p in enumerate(pregs_texto):
                        pid = p["id"]
                        display_num = preguntas.index(p) + 1 if p in preguntas else i + 1
                        with st.container(border=True):
                            st.markdown(f"**{display_num}. {p['enunciado']}**")
                            saved_val = st.session_state.respuestas_usuario.get(pid)
                            idx_guardado = None
                            if saved_val in p["opciones"]:
                                idx_guardado = p["opciones"].index(saved_val)
                            respuesta = st.radio(
                                f"Op P{display_num}",
                                p["opciones"],
                                index=idx_guardado,
                                key=f"radio_demre_{pid}",
                                label_visibility="collapsed",
                            )
                            if respuesta:
                                st.session_state.respuestas_usuario[pid] = respuesta

        st.markdown("<br>", unsafe_allow_html=True)
        col_ev1, col_ev2, col_ev3 = st.columns([1, 2, 1])
        with col_ev2:
            respondidas = len(st.session_state.respuestas_usuario)
            sin_responder = len(preguntas) - respondidas
            if sin_responder > 0:
                st.warning(f"⚠️ Tienes {sin_responder} pregunta(s) sin responder. Puedes entregar igual.")
            if st.button("✅ ENTREGAR ENSAYO", type="primary", use_container_width=True):
                resultado = evaluar_respuestas(preguntas, st.session_state.respuestas_usuario)
                record = {
                    "usuario": st.session_state.usuario_actual,
                    "ensayo_id": str(ens.get("_id", "")),
                    "texto_id": "completo",
                    "titulo_ensayo": ens.get("titulo", "Ensayo DEMRE"),
                    "fecha": datetime.now(),
                    "puntaje": resultado["correctas"],
                    "total": resultado["total"],
                    "nota": resultado["nota"],
                    "dificultad": "DEMRE Oficial",
                    "preguntas_data": preguntas,
                    "respuestas_usuario": st.session_state.respuestas_usuario,
                    "habilidades": resultado.get("habilidades", {}),
                }
                if st.session_state.get("db_conectada"):
                    try:
                        st.session_state.ensayos_col.insert_one(record)
                    except Exception as e:
                        print(f"DB Error silenciado: {e}")
                st.session_state.resultado_ensayo = record
                st.session_state.fase_examen = "resultados"
                st.rerun()

    # ----------------------------------------------------------------
    # FASE 3 — RESULTADOS: puntaje y revisión
    # ----------------------------------------------------------------
    elif fase == "resultados":
        record = st.session_state.get("resultado_ensayo", {})

        col_titulo, col_volver = st.columns([4, 1])
        with col_titulo:
            st.markdown("## 📊 Resultado del Ensayo DEMRE")
        with col_volver:
            if st.button("⬅️ Volver a Biblioteca", use_container_width=True):
                st.session_state.fase_examen = "configuracion"
                st.rerun()

        puntaje = record.get("puntaje", 0)
        total = record.get("total", 1)
        nota = record.get("nota", "N/A")
        precision = int((puntaje / total) * 100) if total > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje Logrado", f"{puntaje} / {total}")
        c2.metric("Nota Final", nota)
        c3.metric("Precisión Global", f"{precision}%")

        if puntaje == total:
            st.balloons()
            st.success("¡Puntaje Perfecto! Rendimiento sobresaliente. 🌟")
        elif precision >= 60:
            st.info("Buen resultado. Sigue repasando los textos en que fallaste. 👍")
        else:
            st.error("Necesitas reforzar. Revisa las explicaciones abajo. 📚")

        habilidades = record.get("habilidades", {})
        if habilidades:
            st.markdown("<hr style='margin:16px 0;'>", unsafe_allow_html=True)
            st.markdown("### 🎯 Desglose por Habilidad")
            hcols = st.columns(len(habilidades))
            for hcol, (hab, datos) in zip(hcols, habilidades.items()):
                pct = int((datos.get("acierto", 0) / datos["total"]) * 100) if datos.get("total", 0) > 0 else 0
                hcol.metric(hab, f"{pct}%", f"{datos.get('acierto',0)}/{datos.get('total',0)}")

        st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📝 Análisis Pregunta por Pregunta")

        preguntas = record.get("preguntas_data", [])
        respuestas_u = record.get("respuestas_usuario", {})

        aciertos, fallos = [], []
        for i, p in enumerate(preguntas):
            pid = p["id"]
            r_user = respuestas_u.get(pid)
            r_idx = p.get("correcta", 0)
            r_correcta_str = p["opciones"][r_idx] if isinstance(r_idx, int) and r_idx < len(p["opciones"]) else "N/A"
            es_ok = r_user == r_correcta_str
            entry = {
                "num": i + 1,
                "enunciado": p["enunciado"],
                "tu_respuesta": r_user or "Sin responder",
                "correcta": r_correcta_str,
                "explicacion": p.get("explicacion", "Sin explicación."),
                "ok": es_ok,
            }
            (aciertos if es_ok else fallos).append(entry)

        tab_ok, tab_mal = st.tabs([f"✅ Correctas ({len(aciertos)})", f"❌ Incorrectas ({len(fallos)})"])

        with tab_ok:
            if not aciertos:
                st.info("No tuviste aciertos.")
            for p in aciertos:
                with st.expander(f"✅ Pregunta {p['num']}: {p['enunciado'][:60]}..."):
                    st.markdown(f"**{p['enunciado']}**")
                    st.markdown(f"<span style='color:#22C55E'>**Tu respuesta:** {p['tu_respuesta']}</span>", unsafe_allow_html=True)
                    st.info(f"**💡 Explicación:** {p['explicacion']}")

        with tab_mal:
            if not fallos:
                st.success("¡Sin errores! Rendimiento perfecto.")
            for p in fallos:
                with st.expander(f"❌ Pregunta {p['num']}: {p['enunciado'][:60]}..."):
                    st.markdown(f"**{p['enunciado']}**")
                    st.markdown(f"<span style='color:#EF4444'>**Tu respuesta:** {p['tu_respuesta']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#22C55E'>**Respuesta correcta:** {p['correcta']}</span>", unsafe_allow_html=True)
                    st.info(f"**💡 Explicación:** {p['explicacion']}")

