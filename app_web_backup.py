import mimetypes
mimetypes.add_type('application/javascript', '.js')

import time
import re
import json
import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import base64
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from PIL import Image
import certifi
import dns.resolver  # INYECCIÓN: Librería para controlar redes
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st

# ==============================================================================
# 🗄️ CONFIGURACIÓN DE BASE DE DATOS - MONGODB ATLAS
# ==============================================================================

# 🛡️ BYPASS DE DNS (HACK): Forzamos el uso de Google DNS (8.8.8.8) 
# Esto evita que los proveedores de internet chilenos bloqueen la conexión SRV.
try:
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    dns.resolver.default_resolver = resolver
    print("🌐 Bypass de DNS de Google activado con éxito.")
except Exception as e:
    print(f"⚠️ No se pudo aplicar el Bypass DNS: {e}")

# ⚠️ URL ORIGINAL CONFIRMADA (con el número 1 en t1vh4u9)
MONGO_URI = "mongodb+srv://marchantfelipe_db_user:RLxaJ7ptH1kH2cKg@paes-lecturapro.t1vh4u9.mongodb.net/?appName=Paes-LecturaPro"

@st.cache_resource
def conectar_db():
    try:
        client = MongoClient(
            MONGO_URI, 
            server_api=ServerApi('1'), 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        return client, None
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error de conexión de seguridad: {error_msg}")
        return None, error_msg

# ==============================================================================
# INICIALIZACIÓN DE VARIABLES Y CONEXIÓN INMEDIATA      
# ==============================================================================
if 'db_conectada' not in st.session_state:
    cliente_mongo, error_db = conectar_db()
    if cliente_mongo:
        try:
            # Forzamos la creación de la base de datos y la colección
            st.session_state.db_conectada = True
            db = cliente_mongo['paes_lectura_db']
            st.session_state.ensayos_col = db['ensayos_historial']
            
            # Prueba de fuego: Intentar un conteo rápido para asegurar acceso
            st.session_state.ensayos_col.count_documents({})
            st.session_state.db_error = None
            
            print("\n" + "="*30)
            print("✅ CONEXIÓN EXITOSA A MONGODB")
            print("="*30 + "\n")
        except Exception as e:
            st.session_state.db_conectada = False
            st.session_state.db_error = str(e)
            print(f"❌ Error al acceder a las tablas: {e}")
    else:
        st.session_state.db_conectada = False
        st.session_state.db_error = error_db

if 'menu_actual' not in st.session_state: st.session_state.menu_actual = 'Home'
if 'ensayo_actual' not in st.session_state: st.session_state.ensayo_actual = None
if 'texto_input' not in st.session_state: st.session_state.texto_input = ""
if 'ensayo_evaluado' not in st.session_state: st.session_state.ensayo_evaluado = False
if 'api_key' not in st.session_state: st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "") 
if 'respuestas_usuario' not in st.session_state: st.session_state.respuestas_usuario = {}
if 'nivel_dificultad' not in st.session_state: st.session_state.nivel_dificultad = "Nivel DEMRE (Oficial)"
if 'fase_examen' not in st.session_state: st.session_state.fase_examen = 'configuracion' 
if 'auto_generar' not in st.session_state: st.session_state.auto_generar = False

# ==============================================================================
# DISEÑO CSS UI/UX PRO (PIXEL PERFECT & VIEWPORT MANAGEMENT)
# ==============================================================================

st.markdown("""
    <!-- Escalado Responsivo Estricto para Dispositivos Móviles -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

    /* 1. Normalización Segura (Sin destruir la cuadrícula nativa de Streamlit) */
    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    html, body {
        margin: 0;
        padding: 0;
        overflow-x: hidden !important;
        width: 100vw !important;
        height: 100vh !important;
        touch-action: pan-y; /* Previene el zoom táctil indeseado */
    }

    /* Estética General (Fondo claro neutro para contraste con las tarjetas oscuras) */
    [data-testid="stApp"] {
        background-color: #F8FAFC; 
        color: #000000; 
        font-family: 'Plus Jakarta Sans', sans-serif;
        /* Viewport Management: Contenedor Flex Principal */
        display: flex !important;
        flex-direction: column !important;
        min-height: 100vh !important;
        overflow-x: hidden !important;
    }
    
    /* CONFIGURACIÓN DE PANTALLA COMPLETA Y DISTRIBUCIÓN DE ESPACIO */
    .block-container {
        padding-top: 2.5rem !important; /* Respiro perfecto desde el techo */
        padding-bottom: 70px !important; /* Espacio exacto para el footer naranja fijo */
        padding-left: 2rem !important; 
        padding-right: 2rem !important;
        max-width: 100% !important; 
        width: 100% !important;
        /* Área central flexible */
        flex: 1 1 auto !important; 
        display: flex !important;
        flex-direction: column !important;
    }

    /* Aseguramos que el layout vertical interno también se expanda */
    [data-testid="stVerticalBlock"] {
        flex: 1 1 auto !important;
        display: flex;
        flex-direction: column;
    }

    [data-testid="stHeader"], [data-testid="stDecoration"], .stApp > header {
        display: none !important;
        height: 0px !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Modificación de contenedores con borde */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }

    /* Inputs y Textareas Base */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #1F7AFF !important;
        box-shadow: 0 0 0 1px #1F7AFF !important;
        background-color: #FFFFFF !important;
    }

    /* Animaciones Generales */
    @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
    
    /* Animación de Parpadeo/Latido (Específica para el Modo Lectura) */
    @keyframes pulseBlink {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.5); }
        50% { transform: scale(1.12); box-shadow: 0 0 25px 10px rgba(255, 255, 255, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    
    .fade-in-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

    /* TARJETAS DE ACCIÓN RÁPIDA (AZUL ELÉCTRICO VIBRANTE) */
    .glass-card {
        background: linear-gradient(135deg, #1F7AFF, #0044CC) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 24px 20px !important;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 220px !important;
        width: 100% !important;
        position: relative;
        box-shadow: 0 15px 25px -5px rgba(31, 122, 255, 0.4), inset 0 2px 10px rgba(255,255,255,0.2) !important;
        margin-bottom: 8px !important;
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02) !important;
        background: linear-gradient(135deg, #3385FF, #0055FF) !important;
        box-shadow: 0 20px 30px -10px rgba(31, 122, 255, 0.6) !important;
    }
    .glass-card h3 { color: #FFFFFF !important; font-size: 18px !important; font-weight: 800 !important; margin-bottom: 6px !important; letter-spacing: -0.3px; }
    .glass-card p { color: #E2E8F0 !important; font-size: 13px !important; line-height: 1.4 !important; margin: 0 !important; text-wrap: balance; }

    .card-icon-wrapper {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Clase inyectada exclusivamente para destacar el icono Modo Lectura */
    .icon-lectura-destacado {
        animation: pulseBlink 2s infinite cubic-bezier(0.4, 0, 0.2, 1);
        width: 60px !important;
        height: 60px !important;
        background: rgba(255, 255, 255, 0.25) !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
    }

    /* Botones bajo las tarjetas */
    .stButton > button {
        background: rgba(241, 245, 249, 0.9) !important;
        color: #1F7AFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 2.5em !important;
        font-size: 11px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        margin-top: -10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    .stButton > button:hover {
        background: #FFFFFF !important;
        color: #0044CC !important;
        border-color: #1F7AFF !important;
        box-shadow: 0 6px 10px -2px rgba(31, 122, 255, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# LÓGICA DE NAVEGACIÓN Y COMPONENTES
# ==============================================================================

def navegar_a(pantalla):
    st.session_state.menu_actual = pantalla
    st.rerun()

# ==============================================================================
# 🟢 PANTALLA 1: HOME (DASHBOARD PRINCIPAL RESTAURADO PIXEL-PERFECT)
# ==============================================================================
if st.session_state.menu_actual == 'Home':
    
    # --- INSIGNIA VISUAL PANTALLA 1 ---
    st.markdown('<div style="background: rgba(31,122,255,0.1); color: #1F7AFF; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 5px; border: 1px solid rgba(31,122,255,0.3);">🟢 PANTALLA 1: PANEL PRINCIPAL</div>', unsafe_allow_html=True)
    
    # --- HEADER UNIFICADO Y RESPONSIVO (TÍTULO + MARQUESINA NARANJA VIBRANTE) ---
    st.markdown("""
        <style>
        .responsive-header {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            margin-top: 5px; 
            margin-bottom: 30px; /* Separación hacia las tarjetas azules */
            width: 100%;
        }
        .header-title {
            font-size: 28px !important; 
            font-weight: 900 !important;
            color: #0F172A !important;
            letter-spacing: -0.5px !important;
            margin: 0 !important;
            padding: 0 !important;
            white-space: nowrap;
            line-height: 1 !important;
        }
        .pill-marquee {
            flex: 1;
            min-width: 0;
            height: 50px;
            display: flex;
            align-items: center;
            overflow: hidden;
            background: linear-gradient(90deg, #FF6B00, #FF8C00); /* Naranja Apple/Duolingo */
            padding: 0 30px;
            border-radius: 999px;
            border: 2px solid #FFD1A9;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.2), 0 6px 20px rgba(255, 107, 0, 0.3);
            box-sizing: border-box;
        }
        .marquee-track {
            display: flex;
            width: 200%;
            animation: marquee-desktop 25s linear infinite;
        }
        .marquee-text {
            color: #FFFFFF;
            font-size: 16px;
            font-weight: 900;
            white-space: nowrap;
            width: 50%;
            letter-spacing: 1.5px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            line-height: 1;
        }
        
        /* Reglas Responsivas Estrictas (Móvil) */
        @media (max-width: 768px) {
            .responsive-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            .pill-marquee { padding: 0 20px; width: 100%; }
            .marquee-track { animation: marquee-mobile 12s linear infinite; }
            .marquee-text { font-size: 13px; }
        }
        
        @keyframes marquee-desktop { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        @keyframes marquee-mobile { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        </style>
        
        <div class="fade-in-up responsive-header">
            <h2 class="header-title">Panel Principal</h2>
            <div class="pill-marquee">
                <div class="marquee-track">
                    <span class="marquee-text">EMPRENDIMIENTO FAMILIA MARCHANT - PONCE - REVUELTA &nbsp;&nbsp;&nbsp;&nbsp; ★ &nbsp;&nbsp;&nbsp;&nbsp; ADMISIÓN 2027 &nbsp;&nbsp;&nbsp;&nbsp; ★ &nbsp;&nbsp;&nbsp;&nbsp;</span>
                    <span class="marquee-text">EMPRENDIMIENTO FAMILIA MARCHANT - PONCE - REVUELTA &nbsp;&nbsp;&nbsp;&nbsp; ★ &nbsp;&nbsp;&nbsp;&nbsp; ADMISIÓN 2027 &nbsp;&nbsp;&nbsp;&nbsp; ★ &nbsp;&nbsp;&nbsp;&nbsp;</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- ALERTA VISUAL DE FALLO DE BASE DE DATOS (NUEVO) ---
    if st.session_state.get('db_error') and not st.session_state.get('db_conectada'):
        st.error(f"""
        🚨 **Modo Offline Activado (Base de Datos Inaccesible):** Tus resultados temporales se guardarán solo en esta sesión.
        
        **Diagnóstico del Servidor:** `{st.session_state.db_error}`
        
        **👉 Plan de Acción Inmediato:**
        1. **Despierta tu Servidor:** Ingresa a la web de MongoDB Atlas. Si tu base de datos dice "Paused" o "Hibernating", haz clic en el botón verde **Resume**.
        2. **Verifica la URL:** En Atlas, ve a *Connect -> Drivers -> Python* y revisa si la URL es `t1vh4u9` (con número uno) o `tlvh4u9` (con letra ele minúscula). Modifica la línea `MONGO_URI` en este código para que coincida exactamente.
        """)

    # --- GRID DE 5 TARJETAS ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('''
            <div class="glass-card fade-in-up" style="animation-delay: 0.1s;">
                <div class="card-icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                </div>
                <h3>Mi Historial</h3>
                <p>Repasa tus resultados anteriores y mejora tu rendimiento.</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("VER HISTORIAL", key="h_bt", use_container_width=True): navegar_a('Mi Historial')
        
    with col2:
        # Se inyecta la clase icon-lectura-destacado y se redimensiona el SVG a 34x34
        st.markdown('''
            <div class="glass-card fade-in-up" style="animation-delay: 0.2s;">
                <div class="card-icon-wrapper icon-lectura-destacado">
                    <svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </div>
                <h3>Modo Lectura</h3>
                <p>Simulacro IA con retroalimentación inmediata.</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("ENTRENAR LECTURA", key="t_bt", use_container_width=True): navegar_a('Modo Lectura')
        
    with col3:
        st.markdown('''
            <div class="glass-card fade-in-up" style="animation-delay: 0.3s;">
                <div class="card-icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                </div>
                <h3>Mi Progreso</h3>
                <p>Visualiza tu avance mediante gráficos interactivos.</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("ESTADÍSTICAS", key="p_bt", use_container_width=True): navegar_a('Mi Progreso')

    with col4:
        st.markdown('''
            <div class="glass-card fade-in-up" style="animation-delay: 0.4s;">
                <div class="card-icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.88 18.09A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.29"/><polyline points="12 12 12 21"/><polyline points="8 17 12 21 16 17"/></svg>
                </div>
                <h3>Descargas</h3>
                <p>Exporta tus resultados en PDF o CSV.</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("BAJAR REPORTES", key="d_bt", use_container_width=True): navegar_a('Mis Descargas')
        
    with col5:
        st.markdown('''
            <div class="glass-card fade-in-up" style="animation-delay: 0.5s;">
                <div class="card-icon-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                </div>
                <h3>Nivel IA</h3>
                <p>Configura la exigencia técnica del motor de IA.</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("DIFICULTAD IA", key="c_bt", use_container_width=True): navegar_a('Nivel de Dificultad')

    st.markdown("<hr style='border-color: #E2E8F0; margin: 30px 0;'>", unsafe_allow_html=True)

    # --- SECCIÓN INFERIOR (2 PANELES PRINCIPALES) ---
    col_t, col_w = st.columns([1.1, 1.9], gap="large")
    
    with col_t:
        st.markdown("""
            <div class='fade-in-up' style='padding: 20px 0; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                <div style="
                    display: inline-block;
                    background: #8A2BE2;
                    color: #FFFFFF;
                    font-size: 13px;
                    font-weight: 800;
                    padding: 8px 18px;
                    border-radius: 999px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    margin-bottom: 25px;
                    box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
                ">
                    ADMISIÓN 2027
                </div>
                <h1 style="
                    font-size: clamp(40px, 4.5vw, 64px);
                    font-weight: 900;
                    line-height: 1.05;
                    letter-spacing: -2px;
                    margin-bottom: 25px;
                    color: #8A2BE2;
                ">
                    LÉCTURA PRO<br>PAES LENGUAJE
                </h1>
                <p style='
                    font-size: 18px; 
                    color: #888888; 
                    font-weight: 500; 
                    line-height: 1.7; 
                    max-width: 95%; 
                    margin-bottom: 0;
                '>
                    La plataforma de entrenamiento PAES más avanzada de Chile. Domina la Competencia Lectora con algoritmos de IA de última generación.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_w:
        # --- WIDGET DARK CON NEON ---
        st.components.v1.html("""
            <div class="fade-in-up" style="
                background: #0D1117;
                border-radius: 28px;
                color: #FFFFFF;
                display: flex;
                flex-wrap: wrap; 
                justify-content: space-between; 
                align-items: center; 
                padding: 40px 45px;
                border: 2px solid #1F7AFF;
                box-shadow: 0 0 25px rgba(31, 122, 255, 0.25), inset 0 0 20px rgba(31, 122, 255, 0.1);
                width: 100%;
                box-sizing: border-box;
                font-family: 'Plus Jakarta Sans', sans-serif;
                position: relative;
            ">
                <!-- Columna Izquierda: Oferta y Beneficios -->
                <div style="flex: 1; min-width: 260px; padding-right: 25px;">
                    <div style="
                        background: #111827;
                        color: #FFFFFF;
                        font-size: 12px;
                        font-weight: 800;
                        padding: 8px 16px;
                        border-radius: 6px;
                        display: inline-block;
                        margin-bottom: 25px;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        border: 1px solid #1F7AFF;
                    ">
                        OFERTA EXCLUSIVA PAES 2027
                    </div>
                    <h1 style="font-size: clamp(38px, 4vw, 52px); font-weight: 900; margin: 0; line-height: 1.1; letter-spacing: -1px; color: #FFFFFF;">
                        DESBLOQUEA TODO
                    </h1>
                    <h2 style="font-size: clamp(30px, 3.5vw, 44px); font-weight: 900; color: #00FF00; margin: 10px 0 30px 0; text-shadow: 0 0 20px rgba(0, 255, 0, 0.4);">
                        POR SOLO $3.000
                    </h2>
                    <div style="display: flex; flex-direction: column; gap: 15px;">
                        <div style="display: flex; align-items: center; gap: 12px; font-size: 16px; font-weight: 600; color: #FFFFFF;">
                            <span style="font-size: 22px;">✅ 🚀</span> Ensayos Oficiales DEMRE Ilimitados
                        </div>
                        <div style="display: flex; align-items: center; gap: 12px; font-size: 16px; font-weight: 600; color: #FFFFFF;">
                            <span style="font-size: 22px;">🚀 🚀</span> Análisis de IA en Tiempo Real
                        </div>
                    </div>
                </div>

                <!-- Columna Derecha: Tarjeta de Puntaje y Botón -->
                <div style="width: 300px; display: flex; flex-direction: column; gap: 20px; flex-shrink: 0; z-index: 10;">
                    <div style="
                        background: rgba(255, 255, 255, 0.03);
                        border-radius: 20px;
                        padding: 35px 25px;
                        text-align: center;
                        border: 1px solid rgba(31, 122, 255, 0.3);
                        box-shadow: inset 0 0 20px rgba(31, 122, 255, 0.05);
                        background-image: 
                            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
                        background-size: 20px 20px;
                        position: relative;
                    ">
                        <div style="display: flex; align-items: baseline; justify-content: center; gap: 8px;">
                            <span style="font-size: 64px; font-weight: 900; line-height: 1; color: #FFFFFF; text-shadow: 0 0 15px rgba(255,255,255,0.2);">860</span>
                            <span style="font-size: 20px; font-weight: 800; color: #888888;">Ptos</span>
                        </div>
                        <div style="font-size: 12px; font-weight: 800; color: #888888; letter-spacing: 1px; margin-top: 10px;">
                            PROYECCIÓN DE MEJORA
                        </div>
                        <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; margin-top: 25px; position: relative; overflow: hidden;">
                            <div style="position: absolute; left: 0; top: 0; height: 100%; width: 86%; background: #1F7AFF; border-radius: 4px; box-shadow: 0 0 15px #1F7AFF;"></div>
                        </div>
                    </div>
                    <button style="
                        background: linear-gradient(135deg, #0044CC, #1F7AFF);
                        color: #FFFFFF;
                        border: 1px solid #1F7AFF;
                        border-radius: 14px;
                        padding: 20px 0;
                        font-size: 15px;
                        font-weight: 900;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        cursor: pointer;
                        box-shadow: 0 0 20px rgba(31, 122, 255, 0.5);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        transition: all 0.2s;
                    " onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 0 30px rgba(31, 122, 255, 0.8)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 0 20px rgba(31, 122, 255, 0.5)';">
                        SUSCRIBIRME AHORA <span style="font-size: 20px;">⚡</span>
                    </button>
                </div>
            </div>
            
            <style>
                @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
                .fade-in-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
            </style>
        """, height=420)

    # --- MARQUESINA INFERIOR (PIXEL PERFECT: FUERA DEL FLUJO / FOOTER FIJO) ---
    st.markdown("""
        <div class="fade-in-up" style="
            position: fixed; 
            bottom: 0; 
            left: 0; 
            width: 100vw; 
            overflow: hidden; 
            background: #FFA500; 
            padding: 12px 0; 
            border-top: 2px solid #CC8400; 
            box-shadow: 0 -5px 20px rgba(255, 165, 0, 0.3); 
            z-index: 99999;
        ">
            <div style="display: flex; width: 200%; animation: marquee 30s linear infinite;">
                <span style="color: #000000; font-size: 15px; font-weight: 900; white-space: nowrap; width: 50%; letter-spacing: 2px;">
                    ... E CHILE | U. DE CONCEPCIÓN | USACH | U. ADOLFO IBÁÑEZ | U. DEL DESARROLLO | PUCV | U. ANDRÉS BELLO ...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </span>
                <span style="color: #000000; font-size: 15px; font-weight: 900; white-space: nowrap; width: 50%; letter-spacing: 2px;">
                    ... E CHILE | U. DE CONCEPCIÓN | USACH | U. ADOLFO IBÁÑEZ | U. DEL DESARROLLO | PUCV | U. ANDRÉS BELLO ...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# FLUJO MODO LECTURA (CONTIENE PANTALLAS 2, 3 Y 4)
# ==============================================================================
elif st.session_state.menu_actual == 'Modo Lectura':
    
    # ---------------------------------------------------------
    # 🟢 PANTALLA 3: MODO ENFOQUE LECTOR (DISEÑO ANTI-FATIGA + HERRAMIENTAS ACTIVAS)
    # ---------------------------------------------------------
    if st.session_state.fase_examen == 'lectura':
        
        # --- INSIGNIA VISUAL PANTALLA 3 ---
        st.markdown('<div style="background: rgba(31,122,255,0.1); color: #1F7AFF; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(31,122,255,0.3);">🟢 PANTALLA 3: ESTUDIO ACTIVO</div>', unsafe_allow_html=True)
        
        # --- HEADER FLOTANTE DE LA VISTA STREAMLIT ---
        col_espacio, col_close = st.columns([5, 1.5])
        with col_close:
            if st.button("✖ Salir al Panel", use_container_width=True):
                st.session_state.fase_examen = 'configuracion'
                st.rerun()
                
        # --- PRE-PROCESAMIENTO ANTI-PDF Y ESCAPADO SEGURO ---
        texto_procesado = st.session_state.texto_input.replace('\r\n', '\n')
        texto_procesado = re.sub(r'\n{2,}', '<br><br>', texto_procesado)
        texto_procesado = texto_procesado.replace('\n', ' ')
        
        # Escapado seguro para inyección de variables Python en JS/HTML
        texto_html_seguro = texto_procesado.replace("{", "&#123;").replace("}", "&#125;")

        # --- MOTOR DE LECTURA ACTIVA (HTML/JS + LOCALSTORAGE + PANEL FIJO) ---
        html_lector_activo = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;800&family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">
            <style>
                /* Ocultar barras de scroll del body y fijar altura al 100% del iframe */
                html, body {{
                    background-color: #F8FAFC; 
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    overflow: hidden; /* Esto congela el fondo y el panel derecho */
                }}
                
                /* Layout Flexbox: Contenedor estricto que llena la pantalla */
                .layout-master {{
                    display: flex;
                    gap: 30px;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    height: 100%;
                    box-sizing: border-box;
                    align-items: flex-start;
                }}

                /* HOJA DE LECTURA (CON MOTOR DE SCROLL AISLADO) */
                .contenedor-hoja {{
                    flex: 1;
                    min-width: 0; 
                    height: 100%;
                    overflow-y: auto; /* Magia: Solo esta parte hace scroll */
                    padding-right: 15px;
                    padding-bottom: 60px;
                }}
                
                /* Scrollbar minimalista tipo macOS para la zona de lectura */
                .contenedor-hoja::-webkit-scrollbar {{ width: 8px; }}
                .contenedor-hoja::-webkit-scrollbar-track {{ background: transparent; }}
                .contenedor-hoja::-webkit-scrollbar-thumb {{ background-color: #CBD5E1; border-radius: 10px; }}
                .contenedor-hoja::-webkit-scrollbar-thumb:hover {{ background-color: #94A3B8; }}

                /* PANEL LATERAL (100% CONGELADO) */
                .panel-lateral {{
                    width: 280px;
                    flex-shrink: 0;
                    /* No necesita position absolute ni fixed porque el contenedor layout-master no scrollea */
                }}

                /* Diseño de la Caja de Instrucciones */
                .caja-instrucciones {{
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 20px;
                    padding: 24px;
                    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
                }}

                .caja-instrucciones h4 {{
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    font-size: 16px;
                    font-weight: 800;
                    color: #0F172A;
                    margin: 0 0 12px 0;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}

                .caja-instrucciones p {{
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    font-size: 13px;
                    color: #64748B;
                    line-height: 1.6;
                    margin: 0 0 20px 0;
                }}

                /* Estética de los Botones (Premium) */
                .btn-tool {{
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    background: #FFFFFF;
                    border: 2px solid #E2E8F0;
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-weight: 800;
                    color: #475569;
                    cursor: pointer;
                    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    width: 100%;
                    margin-bottom: 12px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                }}

                .btn-tool:last-child {{
                    margin-bottom: 0;
                }}

                .btn-tool:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 12px rgba(0,0,0,0.06);
                }}

                .btn-tool.yellow:hover {{ border-color: #FDE047; color: #CA8A04; background: #FEF9C3; }}
                .btn-tool.circle:hover {{ border-color: #FCA5A5; color: #DC2626; background: #FEF2F2; }}
                .btn-tool.clear:hover {{ border-color: #9CA3AF; color: #1F2937; background: #F3F4F6; }}

                /* Estructura de la Hoja de Lectura */
                .hoja-lectura {{
                    background: #FDFCF8; /* Crema Anti-fatiga */
                    border-radius: 20px;
                    padding: 50px 60px;
                    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.05);
                    border: 1px solid rgba(0,0,0,0.03);
                    font-family: 'Merriweather', 'Georgia', serif;
                    font-size: 17px;
                    line-height: 1.9;
                    color: #374151;
                    text-align: justify;
                    text-justify: inter-word;
                    margin-bottom: 40px; /* Margen extra al final para scroll holgado */
                }}

                /* ESTILOS DE DESTACADO INTERACTIVO */
                .highlight-yellow {{
                    background-color: rgba(253, 224, 71, 0.85); /* Amarillo vivo */
                    border-radius: 4px;
                    padding: 2px 4px;
                    box-shadow: 0 1px 3px rgba(253, 224, 71, 0.5);
                    transition: background-color 0.2s;
                }}
                .highlight-circle {{
                    border: 2px solid #EF4444; /* Rojo/Naranja fuerte */
                    border-radius: 50%;
                    padding: 2px 6px;
                    display: inline-block;
                    color: #B91C1C;
                    font-weight: bold;
                    background-color: rgba(239, 68, 68, 0.05);
                    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
                }}

                /* Adaptabilidad Inteligente para Móviles (Responsive) */
                @media (max-width: 900px) {{
                    html, body {{ height: auto; overflow: visible; }} /* Liberar el body en móviles */
                    .layout-master {{ flex-direction: column; height: auto; padding: 20px 10px; }}
                    .contenedor-hoja {{ overflow-y: visible; padding-right: 0; }}
                    .panel-lateral {{ width: 100%; position: sticky; top: 0; z-index: 100; }}
                    .hoja-lectura {{ padding: 30px 20px; font-size: 18px; }}
                    .btn-tool {{ padding: 10px 14px; font-size: 13px; }}
                }}
            </style>
        </head>
        <body>
            <div class="layout-master">
                <!-- Columna Izquierda: El Texto Principal (Scroll Inteligente) -->
                <div class="contenedor-hoja">
                    <div class="hoja-lectura" id="content-lectura">
                        {texto_html_seguro}
                    </div>
                </div>
                
                <!-- Columna Derecha: Panel de Herramientas (Congelado) -->
                <div class="panel-lateral">
                    <div class="caja-instrucciones">
                        <h4><span style="font-size: 20px;">🛠️</span> Estudio Activo</h4>
                        <p><b>1.</b> Selecciona el texto.<br><b>2.</b> Aplica una herramienta.</p>
                        
                        <button class="btn-tool yellow" onclick="applyFormat('highlight-yellow')">
                            <span style="font-size:16px;">🟡</span> Destacar Idea
                        </button>
                        <button class="btn-tool circle" onclick="applyFormat('highlight-circle')">
                            <span style="font-size:16px;">⭕</span> Circular Conector
                        </button>
                        
                        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
                        <p style="margin-bottom: 12px; color: #9CA3AF; font-size: 12px;">¿Te equivocaste?</p>
                        
                        <button class="btn-tool clear" onclick="removeFormat()">
                            <span style="font-size:16px;">🧹</span> Borrar Marca
                        </button>
                    </div>
                </div>
            </div>

            <script>
                const contentDiv = document.getElementById('content-lectura');
                const saveKey = 'lectura_pro_save';

                // 1. CARGA INTELIGENTE DESDE LOCALSTORAGE (Pestaña del Navegador)
                try {{
                    const savedHtml = window.parent.localStorage.getItem(saveKey);
                    // Solo restaurar si hay algo guardado
                    if(savedHtml && savedHtml.trim().length > 0) {{
                        contentDiv.innerHTML = savedHtml;
                    }}
                }} catch(e) {{ console.log("Memoria bloqueada por el navegador."); }}

                // 2. FUNCIÓN DE GUARDADO AUTOMÁTICO
                function saveState() {{
                    try {{
                        window.parent.localStorage.setItem(saveKey, contentDiv.innerHTML);
                    }} catch(e) {{}}
                }}

                // 3. APLICAR FORMATO AL TEXTO SELECCIONADO
                function applyFormat(className) {{
                    const sel = window.getSelection();
                    if (!sel.rangeCount || sel.isCollapsed) return;
                    
                    const range = sel.getRangeAt(0);
                    try {{
                        const span = document.createElement('span');
                        span.className = className;
                        // Extraemos el contenido de la selección y lo envolvemos en el span
                        span.appendChild(range.extractContents());
                        range.insertNode(span);
                        // Limpiar la selección para que el usuario vea el cambio
                        sel.removeAllRanges();
                        saveState(); // Guardar el nuevo HTML en memoria
                    }} catch(e) {{
                        alert("💡 Arquitectura de Texto: Para evitar errores, asegúrate de destacar oraciones dentro de un mismo párrafo.");
                    }}
                }}

                // 4. ELIMINAR FORMATO (BORRADOR INTELIGENTE)
                function removeFormat() {{
                    const sel = window.getSelection();
                    if (!sel.rangeCount) return;
                    let node = sel.anchorNode;
                    
                    // Escanear hacia arriba buscando si el usuario hizo clic dentro de un área destacada
                    while(node && node !== contentDiv && node.nodeName !== "BODY") {{
                        if(node.nodeType === 1 && (node.classList.contains('highlight-yellow') || node.classList.contains('highlight-circle'))) {{
                            // Extraer solo el texto puro
                            const textNode = document.createTextNode(node.textContent);
                            // Reemplazar la etiqueta contenedora por el texto puro
                            node.parentNode.replaceChild(textNode, node);
                            saveState(); // Guardar estado limpio
                            return;
                        }}
                        node = node.parentNode;
                    }}
                    alert("💡 Instrucción: Para borrar, selecciona (o haz doble clic) encima del texto que ya está destacado y presiona el botón Borrar Marca.");
                }}
            </script>
        </body>
        </html>
        """
        
        # --- RENDERIZADO DEL COMPONENTE INMERSIVO ---
        st.components.v1.html(html_lector_activo, height=780, scrolling=False) # Se apaga el scroll nativo de Streamlit, usamos el nuestro
        
        # --- ACCIÓN FINAL E INTELIGENCIA EN SEGUNDO PLANO ---
        st.markdown("<br>", unsafe_allow_html=True)
        col_espacio1, col_btn_examen, col_espacio2 = st.columns([1, 2, 1])
        
        # Si venimos de la transición automática, procesamos la IA aquí mismo
        if st.session_state.get('auto_generar', False):
            with st.status("🧠 IA Generando preguntas nivel DEMRE en paralelo...", expanded=False) as status:
                try:
                    genai.configure(api_key=st.session_state.api_key)
                    modelo = genai.GenerativeModel('gemini-2.5-flash') 
                    prompt = f"Actúa como un profesor experto PAES. Genera 5 preguntas de selección múltiple (A, B, C, D) con rigor DEMRE sobre este texto: {st.session_state.texto_input}. Responde exclusivamente en formato JSON: [{{'pregunta': '...', 'opciones': ['A)...', 'B)...', 'C)...', 'D)...'], 'respuesta_correcta': '...', 'explicacion': '...'}}]"
                    
                    response = modelo.generate_content(prompt)
                    match = re.search(r'\[.*\]', response.text, re.DOTALL)
                    if match:
                        st.session_state.ensayo_actual = json.loads(match.group(0))
                        st.session_state.ensayo_evaluado = False
                        st.session_state.respuestas_usuario = {}
                        st.session_state.start_time = time.time()
                        st.session_state.auto_generar = False # Tarea completada
                        status.update(label="✅ Examen preparado con éxito", state="complete")
                    else:
                        st.error("Error en formato IA. Intenta pegar el texto nuevamente.")
                except Exception as e:
                    st.error(f"🚨 Error de conexión: {e}")

        with col_btn_examen:
            if st.button("🚀 COMENZAR PREGUNTAS", type="primary", use_container_width=True):
                if st.session_state.ensayo_actual:
                    st.session_state.fase_examen = 'preguntas'
                    st.rerun()
                else:
                    st.warning("Espera a que la IA termine de preparar tus preguntas.")

    # ---------------------------------------------------------
    # 🟢 PANTALLA 2: CONFIGURACIÓN (CON AUTODISPARADOR CERO BOTONES)
    # ---------------------------------------------------------
    elif st.session_state.fase_examen == 'configuracion':
        
        # --- INSIGNIA VISUAL PANTALLA 2 ---
        st.markdown('<div style="background: rgba(31,122,255,0.1); color: #1F7AFF; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(31,122,255,0.3);">🟢 PANTALLA 2: CONFIGURACIÓN IA</div>', unsafe_allow_html=True)

        # --- INYECCIÓN CSS EXCLUSIVA PARA ESTA PANTALLA (AISLAMIENTO TOTAL) ---
        st.markdown("""
            <style>
            /* Botón Volver Rediseñado (Estilo Apple / Modern Pill) */
            .back-btn-wrapper button {
                border-radius: 999px !important;
                width: auto !important;
                height: 45px !important;
                padding: 0 24px !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 16px !important;
                font-weight: 800 !important;
                background: #FFFFFF !important;
                color: #475569 !important;
                border: 2px solid #E2E8F0 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
                transition: all 0.3s ease !important;
                letter-spacing: 0.5px !important;
            }
            .back-btn-wrapper button:hover {
                background: #F8FAFC !important;
                border-color: #1F7AFF !important;
                color: #1F7AFF !important;
                box-shadow: 0 4px 12px rgba(31, 122, 255, 0.15) !important;
                transform: translateY(-2px) !important;
            }

            /* Step Cards Refinement (Más suaves y elegantes) */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #F8FAFC !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 16px !important;
                box-shadow: inset 0 2px 4px rgba(255,255,255,0.8), 0 2px 8px rgba(0,0,0,0.02) !important;
                padding: 24px !important;
            }

            /* Modern Input - Base state (Cero fatiga visual y fuente más grande) */
            .stTextInput > div > div > input, .stTextArea > div > div > textarea {
                background-color: #FFFFFF !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 16px !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-size: 16px !important;
                line-height: 1.6 !important;
                color: #1E293B !important;
                font-weight: 500 !important;
                box-shadow: none !important;
                outline: none !important;
            }
            /* Custom Input Wrapper */
            .stTextInput > div > div, .stTextArea > div > div {
                background-color: #FFFFFF !important;
                border: 1px solid #CBD5E1 !important;
                border-radius: 12px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            /* Disable Streamlit default pink border completely */
            div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
                box-shadow: none !important;
                border-color: transparent !important;
            }
            /* Apply neon and blue border ONLY on our wrapper when focused */
            .stTextInput > div > div:focus-within, .stTextArea > div > div:focus-within {
                border-color: #1F7AFF !important;
                box-shadow: 0 0 0 3px rgba(31, 122, 255, 0.15), 0 0 15px rgba(31, 122, 255, 0.2) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Ajuste de columnas para que el botón volver se expanda naturalmente
        col_izq, col_der = st.columns([1.5, 5.5])
        with col_izq:
            st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
            if st.button("⬅ Volver", use_container_width=False): 
                st.session_state.fase_examen = 'configuracion'
                navegar_a('Home')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --- NUEVA CABECERA PREMIUM (CON GRADIENTE TEXTUAL Y FUENTE MAYOR) ---
        with col_der:
            st.markdown("""
                <div style="background: #FFFFFF; padding: 25px 30px; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 10px 30px -10px rgba(31, 122, 255, 0.1); margin-top: -15px;">
                    <h2 style='margin: 0; font-weight: 900; font-size: 30px; display: flex; align-items: center; gap: 12px; background: linear-gradient(135deg, #1F7AFF, #8A2BE2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                        <span style="font-size: 32px; -webkit-text-fill-color: initial;">🧠</span> Entrenamiento PAES Activo
                    </h2>
                    <p style='margin: 8px 0 0 0; color: #475569; font-size: 16px; font-weight: 600; line-height: 1.6;'>Configura tu motor de Inteligencia Artificial. Al pegar tu material de estudio, el entorno inmersivo de lectura profunda se abrirá automáticamente.</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        # --- TARJETA ÚNICA DE MATERIAL DE ESTUDIO (VERSIÓN PRODUCCIÓN / COMERCIAL) ---
        with st.container(border=True):
            
            # --- NUEVO ENCABEZADO CON BOTÓN "NUEVO TEXTO" INCORPORADO ---
            col_hdr1, col_hdr2 = st.columns([3, 1])
            with col_hdr1:
                st.markdown("""
                    <div style="display: flex; align-items: center; gap: 18px; margin-bottom: 20px;">
                        <div style="background: linear-gradient(135deg, #FEF3C7, #FDE68A); width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5), 0 4px 6px rgba(0,0,0,0.05);">
                            <span style="font-size: 24px;">📝</span>
                        </div>
                        <div>
                            <h3 style="margin: 0; color: #0F172A; font-size: 20px; font-weight: 800; letter-spacing: -0.5px;">Material de Estudio</h3>
                            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 15px; font-weight: 500;">Pega el texto a analizar. La IA iniciará el entorno sola.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col_hdr2:
                # Si hay texto, mostramos el botón Nuevo Texto arriba a la derecha
                if len(st.session_state.texto_input) > 0:
                    st.markdown("""
                        <style>
                        .btn-nuevo-texto button {
                            border-radius: 12px !important;
                            font-weight: 800 !important;
                            color: #EF4444 !important;
                            background: #FEF2F2 !important;
                            border: 1px solid #FCA5A5 !important;
                            height: 45px !important;
                            margin-top: 5px !important;
                            transition: all 0.3s ease !important;
                        }
                        .btn-nuevo-texto button:hover {
                            background: #FEE2E2 !important;
                            transform: translateY(-2px) !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="btn-nuevo-texto">', unsafe_allow_html=True)
                    if st.button("🗑️ NUEVO TEXTO", use_container_width=True):
                        st.session_state.texto_input = ""
                        st.session_state.ensayo_actual = None
                        # Script invisible para borrar la memoria (highlights) del navegador
                        st.components.v1.html("<script>try{ window.parent.localStorage.removeItem('lectura_pro_save'); } catch(e){}</script>", height=0)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # --- SENSOR DE AUTO-ACTIVACIÓN (MAGIC PASTE) ---
            st.components.v1.html("""
                <script>
                const doc = window.parent.document;
                const observer = new MutationObserver(() => {
                    const textarea = doc.querySelector('textarea[aria-label="Texto de estudio:"]');
                    if (textarea && !textarea.dataset.listenerSet) {
                        textarea.dataset.listenerSet = "true";
                        textarea.addEventListener('paste', () => {
                            setTimeout(() => { 
                                textarea.blur(); 
                            }, 100);
                        });
                    }
                });
                observer.observe(doc.body, { childList: true, subtree: true });
                </script>
            """, height=0)

            # Text Area principal
            texto_actual = st.text_area("Texto de estudio:", height=250, value=st.session_state.texto_input, label_visibility="collapsed", placeholder="Pega tu texto aquí... ¡El aviso de lectura aparecerá solo!")
            
            # LÓGICA DE DETECCIÓN INSTANTÁNEA Y PERSISTENCIA
            if texto_actual != st.session_state.texto_input:
                st.session_state.texto_input = texto_actual
                st.session_state.ensayo_actual = None # Invalida el ensayo anterior si cambian 1 letra
                # Borra la caché visual si editan el texto
                st.components.v1.html("<script>try{ window.parent.localStorage.removeItem('lectura_pro_save'); } catch(e){}</script>", height=0)
                st.rerun()
            
            if 0 < len(st.session_state.texto_input) < 50:
                st.warning("⚠️ El texto es demasiado corto para un ensayo oficial. (Mínimo 50 caracteres)")

            # --- BOTÓN DE ENTRADA ÚNICO (CENTRALIZADO) ---
            if len(st.session_state.texto_input) >= 50:
                st.markdown("""
                    <style>
                    @keyframes pulseGiant {
                        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(31, 122, 255, 0.7); }
                        50% { transform: scale(1.03); box-shadow: 0 0 30px 10px rgba(31, 122, 255, 0); }
                        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(31, 122, 255, 0); }
                    }
                    [data-testid="baseButton-primary"] {
                        animation: pulseGiant 1.5s infinite cubic-bezier(0.4, 0, 0.2, 1) !important;
                        height: 4em !important;
                        font-size: 20px !important;
                        font-weight: 900 !important;
                        border-radius: 16px !important;
                        background: linear-gradient(135deg, #1F7AFF, #8A2BE2) !important;
                        border: 2px solid #FFFFFF !important;
                        text-transform: uppercase !important;
                        letter-spacing: 1px !important;
                        margin-top: 15px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                st.success("✅ **Texto validado y listo en memoria.**")
                
                if st.button("🚀 IR A MODO LECTURA", type="primary", use_container_width=True, key="go_lectura_popup"):
                    st.session_state.fase_examen = 'lectura'
                    # Ahorro de Tokens: Solo autogeneramos si es un texto nuevo sin ensayo previo
                    if not st.session_state.ensayo_actual:
                        st.session_state.auto_generar = True
                    st.rerun()

    # ---------------------------------------------------------
    # 🟢 PANTALLA 4: PREGUNTAS (EVALUACIÓN DEL ENSAYO)
    # ---------------------------------------------------------
    # --- 1. ESTILOS CSS PARA EL SPLIT VIEW ---
    st.markdown("""
        <style>
        .split-container {
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }
        .scrollable-text-panel {
            background-color: #FDFCF8;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 30px;
            height: 80vh;
            overflow-y: auto;
            position: sticky;
            top: 10px;
            font-family: 'Merriweather', serif;
            line-height: 1.8;
            color: #1E293B;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
        }
        /* Tarjeta de Respuesta Premium */
        .result-card {
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            background: white;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .result-card.correct { border-left: 8px solid #22C55E; }
        .result-card.incorrect { border-left: 8px solid #EF4444; }
        
        .explanation-box {
            background: #F8FAFC;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border: 1px dashed #CBD5E1;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. LAYOUT DE COLUMNAS (IZQ: PREGUNTAS | DER: TEXTO) ---
    col_content, col_text_guide = st.columns([1.1, 0.9], gap="large")

    with col_text_guide:
        st.markdown("<p style='font-weight:800; color:#64748B; font-size:12px; margin-bottom:5px;'>📖 TEXTO DE REFERENCIA</p>", unsafe_allow_html=True)
        # Mostramos el texto en un panel con scroll propio
        # NOTA: Para mantener lo destacado, usamos el texto_input procesado
        texto_limpio = st.session_state.texto_input.replace('\n', '<br>')
        st.markdown(f"""<div class="scrollable-text-panel">{texto_limpio}</div>""", unsafe_allow_html=True)

    with col_content:
        # --- CASO A: RESOLVIENDO EL EXAMEN ---
        if not st.session_state.ensayo_evaluado:
            st.markdown("### 📝 Responde las preguntas")
            if st.session_state.ensayo_actual:
                for i, p in enumerate(st.session_state.ensayo_actual):
                    with st.container(border=True):
                        st.markdown(f"**PREGUNTA {i+1}**")
                        st.markdown(f"*{p['pregunta']}*")
                        st.session_state.respuestas_usuario[i] = st.radio(
                            f"Opciones P{i}", p['opciones'], 
                            key=f"radio_q_{i}", index=None, label_visibility="collapsed"
                        )

                if st.button("✅ FINALIZAR Y EVALUAR", type="primary", use_container_width=True):
                    # Lógica de cálculo
                    puntos = 0
                    for i, p in enumerate(st.session_state.ensayo_actual):
                        resp = st.session_state.respuestas_usuario.get(i)
                        if resp and resp.strip().startswith(p['respuesta_correcta']):
                            puntos += 1
                    
                    st.session_state.ultimo_puntaje = puntos
                    st.session_state.ultima_nota = round((puntos / len(st.session_state.ensayo_actual)) * 7.0, 1)
                    
                    # Guardado en Mongo
                    if st.session_state.get('db_conectada', False):
                        try:
                            st.session_state.ensayos_col.insert_one({
                                "fecha": datetime.now(),
                                "puntaje": puntos,
                                "total": len(st.session_state.ensayo_actual),
                                "nota": st.session_state.ultima_nota,
                                "dificultad": st.session_state.nivel_dificultad,
                                "preguntas_data": st.session_state.ensayo_actual,
                                "respuestas_usuario": st.session_state.respuestas_usuario,
                                "texto_referencia": st.session_state.texto_input # Guardamos el texto también
                            })
                        except: pass
                    
                    st.session_state.ensayo_evaluado = True
                    st.rerun()

        # --- CASO B: RESULTADOS (DISEÑO PREMIUM SOLICITADO) ---
        else:
            if st.session_state.ultima_nota >= 6.0: st.balloons()
            
            st.markdown(f"## Tu Nota: {st.session_state.ultima_nota}")
            
            for i, p in enumerate(st.session_state.ensayo_actual):
                resp_user = st.session_state.respuestas_usuario.get(i)
                correcta = p['respuesta_correcta']
                es_correcta = resp_user.startswith(correcta) if resp_user else False
                
                clase = "correct" if es_correcta else "incorrect"
                badge = "✅" if es_correcta else "❌"
                
                st.markdown(f"""
                    <div class="result-card {clase}">
                        <p style="font-weight:800; color:#64748B; font-size:11px; margin:0;">PREGUNTA {i+1}</p>
                        <h4 style="margin: 10px 0;">{p['pregunta']}</h4>
                        <div style="display:flex; gap:10px; font-size:14px;">
                            <div style="flex:1;"><b>Tu respuesta:</b><br><span style="color:{'#22C55E' if es_correcta else '#EF4444'}">{resp_user}</span></div>
                            <div style="flex:1;"><b>Correcta:</b><br><span style="color:#22C55E">Opción {correcta}</span></div>
                        </div>
                        <div class="explanation-box">
                            <b>💡 Explicación Técnica:</b><br>
                            {p['explicacion']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔄 NUEVO ENSAYO"):
                st.session_state.fase_examen = 'configuracion'
                st.session_state.ensayo_evaluado = False
                st.rerun()
# ==============================================================================
# 🟢 PANTALLAS SECUNDARIAS (RESUMIDAS)
# ==============================================================================
elif st.session_state.menu_actual == 'Mi Historial':
    # --- VENTANA FLOTANTE DE REVISIÓN ---
    @st.dialog("📋 REVISIÓN DETALLADA", width="large")
    def mostrar_detalle(datos):
        st.write(f"### Resumen del {datos['fecha'].strftime('%d/%m/%Y %H:%M')}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje", f"{datos['puntaje']}/{datos['total']}")
        c2.metric("Nota", datos['nota'])
        c3.markdown(f"**Nivel:** \n{datos.get('dificultad', 'DEMRE')}")
        
        st.divider()
        st.subheader("📝 Revisión de Preguntas")

        # Recuperar datos guardados
        preguntas = datos.get('preguntas_data', [])
        respuestas_u = datos.get('respuestas_usuario', {})

        if not preguntas:
            st.warning("Este registro no tiene el detalle de preguntas (fue guardado antes de la actualización).")
        else:
            for idx, p in enumerate(preguntas):
                # Mongo guarda las llaves de dict como texto, por eso usamos str(idx)
                r_usuario = respuestas_u.get(str(idx))
                r_correcta = p['respuesta_correcta']
                
                # Determinamos si fue correcta para el estilo
                es_correcta = r_usuario.startswith(r_correcta) if r_usuario else False
                icono = "✅" if es_correcta else "❌"
                
                with st.expander(f"{icono} Pregunta {idx+1}: {p['pregunta'][:60]}..."):
                    st.write(f"**Pregunta:** {p['pregunta']}")
                    st.write(f"---")
                    
                    if es_correcta:
                        st.success(f"**Tu respuesta:** {r_usuario} (Correcta)")
                    else:
                        st.error(f"**Tu respuesta:** {r_usuario}")
                        st.info(f"**Respuesta Correcta:** {r_correcta}")
                    
                    st.markdown(f"**💡 Explicación:** {p['explicacion']}")
        
        if st.button("CERRAR VENTANA"): st.rerun()

    # --- DISEÑO DE LISTADO PRINCIPAL ---
    st.markdown('<div style="background: rgba(138,43,226,0.1); color: #8A2BE2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(138,43,226,0.3);">🟣 PANEL DE RESULTADOS HISTÓRICOS</div>', unsafe_allow_html=True)
    
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ VOLVER"): navegar_a('Home')
    with col_title:
        st.markdown("## 🕒 Mi Historial de Ensayos")

    if st.session_state.get('db_conectada', False):
        try:
            registros = list(st.session_state.ensayos_col.find().sort("fecha", -1).limit(15))
            if not registros:
                st.info("No hay ensayos registrados.")
            else:
                for reg in registros:
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                        with c1:
                            st.markdown(f"📅 **{reg['fecha'].strftime('%d/%m/%Y | %H:%M')}**")
                            st.caption(f"🎯 {reg.get('dificultad', 'Nivel DEMRE')}")
                        with c2: st.metric("Aciertos", f"{reg['puntaje']}/{reg['total']}")
                        with c3:
                            n = reg.get('nota', 0.0)
                            color = "#22C55E" if n >= 4.0 else "#EF4444"
                            st.markdown(f"<div style='text-align:center'><p style='margin:0; font-size:12px; color:#64748B;'>NOTA</p><h2 style='margin:0; color:{color};'>{n}</h2></div>", unsafe_allow_html=True)
                        with c4:
                            if st.button("📄 DETALLE", key=f"det_{reg['_id']}", use_container_width=True):
                                mostrar_detalle(reg)
        except Exception as e:
            st.error(f"❌ Error al cargar historial: {e}")

elif st.session_state.menu_actual == 'Mi Progreso':
    st.markdown('<div style="background: rgba(138,43,226,0.1); color: #8A2BE2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(138,43,226,0.3);">🟣 PANTALLA SECUNDARIA</div>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"): navegar_a('Home')
    st.markdown("## 📈 Mi Progreso")
    st.warning("Completa ensayos para ver estadísticas.")

elif st.session_state.menu_actual == 'Mis Descargas':
    st.markdown('<div style="background: rgba(138,43,226,0.1); color: #8A2BE2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(138,43,226,0.3);">🟣 PANTALLA SECUNDARIA</div>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"): navegar_a('Home')
    st.markdown("## 📥 Descargas")
    st.info("Reportes listos para bajar.")

elif st.session_state.menu_actual == 'Nivel de Dificultad':
    st.markdown('<div style="background: rgba(138,43,226,0.1); color: #8A2BE2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(138,43,226,0.3);">🟣 PANTALLA SECUNDARIA</div>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"): navegar_a('Home')
    st.markdown("## ⚙️ Configuración")
    st.select_slider("Dificultad:", options=["Básico", "Intermedio", "DEMRE", "Avanzado"], value=st.session_state.nivel_dificultad)

# ==============================================================================
# FIN DEL CÓDIGO FUENTE
# ==============================================================================