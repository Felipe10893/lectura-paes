import streamlit as st

# 🛡️ FIX: CONFIGURACIÓN DE PANTALLA COMPLETA (WIDE MODE)
# Debe ser el primer comando de Streamlit en ejecutarse
st.set_page_config(
    page_title="LÉCTURA PRO - PAES 2027", 
    page_icon="🧠", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

import mimetypes
from ui_components import render_interfaz_principal

mimetypes.add_type('application/javascript', '.js')

import time
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import base64
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from PIL import Image

# ==============================================================================
# IMPORTACIONES DE LA NUEVA ARQUITECTURA MODULAR
# ==============================================================================
from database import conectar_db
import ui_components as ui
import streamlit.components.v1 as components
from gemini_service import llamar_gemini, parsear_json_respuesta
from evaluacion_service import calcular_estadisticas_habilidades, evaluar_respuestas

# ==============================================================================
# INICIALIZACIÓN DE VARIABLES Y CONEXIÓN INMEDIATA      
# ==============================================================================
if 'db_conectada' not in st.session_state:
    cliente_mongo, error_db = conectar_db()
    if cliente_mongo:
        try:
            st.session_state.db_conectada = True
            db = cliente_mongo['paes_lectura_db']
            st.session_state.ensayos_col = db['ensayos_historial']
            st.session_state.ensayos_oficiales_col = db['ensayos_oficiales']
            st.session_state.ensayos_col.count_documents({})
            st.session_state.db_error = None
            print("\n" + "="*30)
            print("[OK] CONEXION EXITOSA A MONGODB")
            print("="*30 + "\n")
        except Exception as e:
            st.session_state.db_conectada = False
            st.session_state.db_error = str(e)
            print(f"[ERROR] Error al acceder a las tablas: {e}")
    else:
        st.session_state.db_conectada = False
        st.session_state.db_error = error_db

# 🛡️ INICIALIZACIÓN DEL PERFIL DEL ESTUDIANTE (MULTI-TENANT)
if 'usuario_actual' not in st.session_state: st.session_state.usuario_actual = "Estudiante Invitado"

if 'menu_actual' not in st.session_state: st.session_state.menu_actual = 'Home'
if 'ensayo_actual' not in st.session_state: st.session_state.ensayo_actual = None
if 'texto_input' not in st.session_state: st.session_state.texto_input = ""
if 'ensayo_evaluado' not in st.session_state: st.session_state.ensayo_evaluado = False
if 'api_key' not in st.session_state: st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "") 
if 'respuestas_usuario' not in st.session_state: st.session_state.respuestas_usuario = {}

if 'nivel_dificultad' not in st.session_state: st.session_state.nivel_dificultad = "DEMRE"

if 'fase_examen' not in st.session_state: st.session_state.fase_examen = 'configuracion'
if 'fase_express' not in st.session_state: st.session_state.fase_express = 'configuracion'
if 'auto_generar' not in st.session_state: st.session_state.auto_generar = False
if 'limpiar_cache_js' not in st.session_state: st.session_state.limpiar_cache_js = False
if 'pagina_actual' not in st.session_state: st.session_state.pagina_actual = 'landing'

# Aplicar el CSS principal desde el módulo UI
st.markdown(ui.CSS_GLOBAL, unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR: SISTEMA DE IDENTIFICACIÓN DE ALUMNOS
# ==============================================================================
with st.sidebar:
    st.markdown("### 👤 Perfil del Estudiante")
    st.markdown("<p style='font-size: 12px; color: #64748B;'>Identifícate para guardar tu progreso de forma individual.</p>", unsafe_allow_html=True)
    nuevo_usuario = st.text_input("Tu Nombre o RUT:", value=st.session_state.usuario_actual)
    if nuevo_usuario and nuevo_usuario != st.session_state.usuario_actual:
        st.session_state.usuario_actual = nuevo_usuario
        st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.success(f"Sesión activa:\n**{st.session_state.usuario_actual}**")

# ==============================================================================
# LÓGICA DE NAVEGACIÓN Y COMPONENTES
# ==============================================================================

def navegar_a(pantalla):
    st.session_state.menu_actual = pantalla
    st.rerun()

# ==============================================================================
# 🟢 LANDING PAGE (PANTALLA DE BIENVENIDA)
# ==============================================================================
if st.session_state.pagina_actual == 'landing':
    ui.render_landing_page()

# ==============================================================================
# 🟢 PANTALLA 1: HOME (DASHBOARD PRINCIPAL MODULARIZADO)
# ==============================================================================
if st.session_state.menu_actual in ['Home', 'Dashboard General']:
    render_interfaz_principal()

# ==============================================================================
# # ==============================================================================
# 🟢 PANTALLA 2: ENSAYOS DEMRE (SIMULADOR BIBLIOTECA OFICIAL)
# ==============================================================================
elif st.session_state.menu_actual == 'Ensayos DEMRE':
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col_back, _ = st.columns([1.5, 5])
    with col_back:
        if st.button("⬅️ VOLVER AL MENÚ", use_container_width=True):
            navegar_a('Home')
            
    # 🚀 INYECCIÓN ANTIGRAVITY: Llamamos al motor visual Premium
    ui.render_ensayos_demre()

## ==============================================================================
# 🟢 PANTALLA 3: MODO LECTURA (CENTRO DE DIAGNÓSTICO Y PRÁCTICA DIRIGIDA)
# ==============================================================================
elif st.session_state.menu_actual == 'Modo Lectura':
    
    st.markdown(ui.CSS_SPLIT_VIEW, unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # FASE 1: DASHBOARD DIAGNÓSTICO Y SELECCIÓN
    # ---------------------------------------------------------
    if st.session_state.fase_express == 'configuracion':
        st.markdown('<div style="background: rgba(245, 158, 11, 0.1); color: #F59E0B; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(245, 158, 11, 0.3);">⚡ PRÁCTICA DIRIGIDA Y EXPRESS</div>', unsafe_allow_html=True)
        
        col_izq, col_der = st.columns([1.5, 5.5])
        with col_izq:
            if st.button("⬅ Volver", use_container_width=True): 
                navegar_a('Home')
        with col_der:
            st.markdown(f"## 🎯 Diagnóstico y Entrenamiento")
            st.markdown(f"<p style='color:#64748B;'>Hola <b>{st.session_state.usuario_actual}</b>. Aquí analizamos tu historial para encontrar tus puntos débiles. Puedes generar una práctica personalizada con IA o hacer un ensayo rápido del Banco de Textos.</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 1px dashed var(--card-border); margin: 20px 0;'>", unsafe_allow_html=True)
        
        # --- CÁLCULO DE ESTADÍSTICAS Y PUNTOS DÉBILES ---
        historial_alumno = []
        if st.session_state.get('db_conectada', False):
            historial_alumno = list(st.session_state.ensayos_col.find({"usuario": st.session_state.usuario_actual}))

        stats = calcular_estadisticas_habilidades(historial_alumno)
        total_respondidas = sum(s["total"] for s in stats.values())
        
        st.markdown("### 📊 Tu Diagnóstico de Habilidades")
        
        if total_respondidas == 0:
            st.info("💡 Aún no tenemos suficientes datos para calcular tu diagnóstico. ¡Rinde un Ensayo Oficial o una Práctica Express para empezar a ver tus estadísticas!")
            punto_debil = "Interpretar" # Default para el selector
        else:
            pct_loc = int((stats["Localizar"]["acierto"] / stats["Localizar"]["total"]) * 100) if stats["Localizar"]["total"] > 0 else 0
            pct_int = int((stats["Interpretar"]["acierto"] / stats["Interpretar"]["total"]) * 100) if stats["Interpretar"]["total"] > 0 else 0
            pct_eva = int((stats["Evaluar"]["acierto"] / stats["Evaluar"]["total"]) * 100) if stats["Evaluar"]["total"] > 0 else 0
            
            c_s1, c_s2, c_s3 = st.columns(3)
            c_s1.metric("📌 Localizar", f"{pct_loc}%", f"{stats['Localizar']['acierto']}/{stats['Localizar']['total']} correctas", delta_color="off")
            c_s2.metric("🧠 Interpretar", f"{pct_int}%", f"{stats['Interpretar']['acierto']}/{stats['Interpretar']['total']} correctas", delta_color="off")
            c_s3.metric("⚖️ Evaluar", f"{pct_eva}%", f"{stats['Evaluar']['acierto']}/{stats['Evaluar']['total']} correctas", delta_color="off")
            
            pcts = {"Localizar": pct_loc if stats["Localizar"]["total"]>0 else 100, 
                    "Interpretar": pct_int if stats["Interpretar"]["total"]>0 else 100, 
                    "Evaluar": pct_eva if stats["Evaluar"]["total"]>0 else 100}
            punto_debil = min(pcts, key=pcts.get)
            
            st.warning(f"🚨 **Alerta Académica:** Tu punto más débil actual es la habilidad de **{punto_debil}**. Te sugerimos enfocar tu próxima práctica en esta área.")

        # --- SECCIÓN 1: PRÁCTICA DIRIGIDA (GENERACIÓN IA) ---
        st.markdown("<br><hr style='border-top: 1px solid var(--card-border); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Configurar Práctica Personalizada (IA)")
        
        with st.container(border=True):
            col_hab, col_tar = st.columns(2)
            with col_hab:
                habilidad_sel = st.selectbox("1. Elige la Habilidad a fortalecer:", 
                                            ["Localizar", "Interpretar (Relacionar)", "Evaluar (Reflexionar)"], 
                                            index=["Localizar", "Interpretar", "Evaluar"].index(punto_debil.split()[0]) if "Interpretar" in punto_debil else 0)
            with col_tar:
                tareas = {
                    "Localizar": [
                        "a. Extraer información explícita del texto.",
                        "b. Identificar información explícita formulada a través de sinónimos y de paráfrasis."
                    ],
                    "Interpretar (Relacionar)": [
                        "c. Establecer la relación entre distintas partes o informaciones de un texto.",
                        "d. Elaborar inferencias sobre el significado local y global del texto.",
                        "e. Determinar el significado de una parte o globalidad.",
                        "f. Sintetizar las ideas centrales de una sección o del texto.",
                        "g. Identificar la jerarquía de las ideas.",
                        "h. Reconocer la función de un elemento textual."
                    ],
                    "Evaluar (Reflexionar)": [
                        "i. Determinar la intención comunicativa del emisor(a).",
                        "j. Juzgar la información presente en el texto.",
                        "k. Juzgar la forma en relación con la información.",
                        "l. Calificar la posición o actitud del emisor(a).",
                        "m. Valorar la pertinencia de los recursos.",
                        "n. Valorar la información textual en nuevos contextos."
                    ]
                }
                tarea_sel = st.selectbox("2. Elige la Tarea Lectora específica:", tareas[habilidad_sel])
                
            col_tipo, col_cono = st.columns(2)
            with col_tipo:
                tipo_texto_sel = st.selectbox("3. Elige el Tipo de Texto:", ["Texto No Literario (Expositivo/Argumentativo)", "Texto Literario (Narración)"])
            with col_cono:
                if "No Literario" in tipo_texto_sel:
                    conocimientos = [
                        "1. La información relevante para el sentido de la lectura.",
                        "2. El o los temas e ideas principales.",
                        "3. Las ideas que se entregan para apoyar una información.",
                        "4. La tesis y la manera en que se presenta."
                    ]
                else:
                    conocimientos = [
                        "1. La información relevante para el sentido del relato.",
                        "2. La evolución y motivaciones de los personajes.",
                        "3. El conflicto o problema humano que se expresa."
                    ]
                conocimiento_sel = st.selectbox("4. Elige el Conocimiento Temático:", conocimientos)

            if st.button("🚀 GENERAR ENTRENAMIENTO ENFOCADO (IA)", type="primary", use_container_width=True):
                with st.status(f"🧠 La IA está escribiendo un texto y 3 preguntas EXCLUSIVAS para '{habilidad_sel}'... (~15 seg)", expanded=True) as status:
                    try:
                        INSTRUCCIONES_ENFOCADAS = f"""
                        Actúa como un creador de pruebas PAES DEMRE.
                        Objetivo: Generar una práctica corta enfocada 100% en la debilidad del estudiante.
                        
                        1. TIPO DE TEXTO: {tipo_texto_sel}
                        2. HABILIDAD A EVALUAR: {habilidad_sel}
                        3. TAREA LECTORA ESPECÍFICA: {tarea_sel}
                        4. CONOCIMIENTO ASOCIADO A EVALUAR: {conocimiento_sel}
                        
                        Escribe un texto original (250-350 palabras) y 3 preguntas de selección múltiple sobre esta combinación exacta.
                        
                        🛑 FORMATO JSON OBLIGATORIO:
                        El campo "correcta" debe ser un NÚMERO ENTERO (0=A, 1=B, 2=C, 3=D).
                        {{
                            "titulo": "🎯 Práctica Enfocada: {habilidad_sel}",
                            "textos": {{ "1": {{ "titulo": "Texto Personalizado", "contenido": "Contenido con <br><br>..." }} }},
                            "preguntas": [
                                {{
                                    "id": 1, "texto_id": "1", "enunciado": "¿...?", "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
                                    "correcta": 1, "explicacion": "MACRO-HABILIDAD: {habilidad_sel}..."
                                }}
                            ]
                        }}
                        """
                        response = llamar_gemini(INSTRUCCIONES_ENFOCADAS, st.session_state.api_key, status)
                        practica = parsear_json_respuesta(response.text) if response else None
                        if practica:
                            st.session_state.practica_actual = {
                                'ensayo_id': f"focused_{int(time.time())}",
                                'texto_id': "1",
                                'texto_data': practica['textos']["1"],
                                'preguntas': practica['preguntas'],
                                'titulo_override': practica['titulo']
                            }
                            st.session_state.respuestas_usuario = {}
                            st.session_state.fase_express = 'rendir'
                            st.rerun()
                        else:
                            st.error("Error en formato IA.")
                    except Exception as e:
                        st.error(f"🚨 Error de conexión con Gemini: {e}")

        # --- SECCIÓN 2: BANCO EXPRESS (PRE-GENERADO) ---
        st.markdown("<br><hr style='border-top: 1px solid var(--card-border); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📚 Banco de Textos Express (Carga Instantánea)")
        st.markdown("<p style='color:#64748B; font-size: 14px;'>Textos variados del Banco Oficial. Ideal si tienes prisa y no quieres esperar a la IA.</p>", unsafe_allow_html=True)
        
        if st.session_state.get('db_conectada', False):
            ensayos_db = list(st.session_state.ensayos_oficiales_col.find({"tipo": "banco_express"}).sort("_id", -1))
            
            historial_map = {}
            for h in historial_alumno:
                if h.get("dificultad") == "Práctica Express":
                    key = f"{h.get('ensayo_id')}_{h.get('texto_id')}"
                    historial_map[key] = h
                
            if not ensayos_db:
                st.info("📚 El Banco de Prácticas Rápidas está vacío. Pídele al administrador que genere 'Lotes de Banco Express'.")
            else:
                textos_disponibles = []
                for ens in ensayos_db:
                    e_id = str(ens['_id'])
                    textos = ens.get('textos', {})
                    preguntas = ens.get('preguntas', [])
                    for t_key, t_data in textos.items():
                        pregs_texto = [p for p in preguntas if str(p.get('texto_id')) == str(t_key)]
                        if pregs_texto:
                            textos_disponibles.append({
                                'ensayo_id': e_id,
                                'texto_id': t_key,
                                'texto_data': t_data,
                                'preguntas': pregs_texto,
                                'titulo_override': f"⚡ Micro-Práctica"
                            })
                
                st.markdown("#### 🌟 Sugeridos para ti")
                textos_sugeridos = textos_disponibles[:3] 
                
                cols = st.columns(3)
                for i, item in enumerate(textos_sugeridos):
                    e_id = item['ensayo_id']
                    t_key = item['texto_id']
                    h_key = f"{e_id}_{t_key}"
                    is_done = h_key in historial_map
                    
                    with cols[i % 3]:
                        with st.container(border=True):
                            t_titulo = item['texto_data'].get('titulo', f'Texto {t_key}')
                            st.markdown(f"<h4 style='margin-bottom: 5px; font-size: 15px; font-weight: 800; color: var(--text-color);'>{t_titulo}</h4>", unsafe_allow_html=True)
                            st.caption(f"📝 {len(item['preguntas'])} Preguntas")
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            if is_done:
                                h_data = historial_map[h_key]
                                st.success(f"✅ Realizado - Nota: {h_data.get('nota', 'N/A')}")
                                if st.button("📊 Ver Resultados", key=f"rev_exp_{e_id}_{t_key}", use_container_width=True):
                                    st.session_state.express_record = h_data
                                    st.session_state.fase_express = 'revision'
                                    st.rerun()
                            else:
                                st.info("⏳ Pendiente")
                                if st.button("⚡ Rendir Ahora", key=f"rendir_exp_{e_id}_{t_key}", use_container_width=True):
                                    st.session_state.practica_actual = item
                                    st.session_state.respuestas_usuario = {}
                                    st.session_state.fase_express = 'rendir'
                                    st.rerun()

                st.markdown("<br><hr style='border-top: 1px dashed var(--card-border); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
                st.markdown("#### 🗄️ Archivo Completo de Textos")
                
                opciones_combo = []
                mapa_opciones = {}
                
                for item in textos_disponibles:
                    e_id = item['ensayo_id']
                    t_key = item['texto_id']
                    h_key = f"{e_id}_{t_key}"
                    is_done = h_key in historial_map
                    estado = "✅ [Realizado]" if is_done else "⏳ [Pendiente]"
                    t_titulo = item['texto_data'].get('titulo', f'Texto {t_key}')
                    
                    texto_opcion = f"{estado} | {t_titulo} ({len(item['preguntas'])} pregs)"
                    opciones_combo.append(texto_opcion)
                    mapa_opciones[texto_opcion] = item

                seleccion = st.selectbox("Selecciona un texto del archivo:", ["-- Selecciona un texto --"] + opciones_combo, label_visibility="collapsed")
                
                if seleccion and seleccion != "-- Selecciona un texto --":
                    item_seleccionado = mapa_opciones[seleccion]
                    e_id_sel = item_seleccionado['ensayo_id']
                    t_key_sel = item_seleccionado['texto_id']
                    h_key_sel = f"{e_id_sel}_{t_key_sel}"
                    
                    col_info, col_btn = st.columns([3, 1])
                    with col_info:
                        st.info(f"**Selección Lista:** {item_seleccionado['texto_data'].get('titulo', 'Texto')}")
                        
                    with col_btn:
                        if h_key_sel in historial_map:
                            if st.button("📊 Ver Resultados", key="btn_combo_rev", use_container_width=True):
                                st.session_state.express_record = historial_map[h_key_sel]
                                st.session_state.fase_express = 'revision'
                                st.rerun()
                        else:
                            if st.button("⚡ Rendir Ahora", key="btn_combo_rendir", type="primary", use_container_width=True):
                                st.session_state.practica_actual = item_seleccionado
                                st.session_state.respuestas_usuario = {}
                                st.session_state.fase_express = 'rendir'
                                st.rerun()

    # ---------------------------------------------------------
    # FASE 2: RENDIR PRÁCTICA EXPRESS / ENFOCADA
    # ---------------------------------------------------------
    elif st.session_state.fase_express == 'rendir':
        practica = st.session_state.practica_actual
        texto_data = practica['texto_data']
        preguntas = practica['preguntas']
        titulo_seccion = practica.get('titulo_override', '⚡ Práctica Express')
        
        col_t, col_b = st.columns([4, 1])
        with col_t:
            st.markdown(f"## {titulo_seccion}")
        with col_b:
            if st.button("⬅️ Abandonar", use_container_width=True):
                st.session_state.fase_express = 'configuracion'
                st.rerun()
                
        c_text, c_preg = st.columns([1.2, 1], gap="large")
        
        with c_text:
            st.markdown(f"<h3 style='margin-bottom: 20px;'>{texto_data.get('titulo', 'Texto de Práctica')}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='scrollable-text-panel'>{texto_data.get('contenido', '')}</div>", unsafe_allow_html=True)
            
        with c_preg:
            st.markdown(f"#### Preguntas a resolver ({len(preguntas)})")
            st.markdown("<p style='font-size: 13px; color: #64748B;'>Desliza hacia abajo para ver todas las preguntas.</p>", unsafe_allow_html=True)
            
            st.markdown("<div style='max-height: 60vh; overflow-y: auto; padding-right: 10px;'>", unsafe_allow_html=True)
            
            for i, p in enumerate(preguntas):
                with st.container(border=True):
                    pid = p['id']
                    display_num = i + 1
                    st.markdown(f"**{display_num}. {p['enunciado']}**")
                    
                    idx_guardado = None
                    saved_val = st.session_state.respuestas_usuario.get(pid)
                    if saved_val in p['opciones']:
                        idx_guardado = p['opciones'].index(saved_val)
                        
                    respuesta = st.radio(
                        f"Opciones P{display_num}", p['opciones'], 
                        index=idx_guardado, key=f"radio_exp_{pid}", label_visibility="collapsed"
                    )
                    if respuesta:
                        st.session_state.respuestas_usuario[pid] = respuesta

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("✅ EVALUAR PRÁCTICA COMPLETA", type="primary", use_container_width=True):
                resultado = evaluar_respuestas(preguntas, st.session_state.respuestas_usuario)

                record = {
                    "usuario": st.session_state.usuario_actual,
                    "ensayo_id": practica['ensayo_id'],
                    "texto_id": practica['texto_id'],
                    "titulo_ensayo": f"{titulo_seccion}: {texto_data.get('titulo', 'Lectura')}",
                    "fecha": datetime.now(),
                    "puntaje": resultado['correctas'],
                    "total": resultado['total'],
                    "nota": resultado['nota'],
                    "dificultad": "Práctica Express",
                    "preguntas_data": preguntas,
                    "respuestas_usuario": st.session_state.respuestas_usuario
                }
                
                if st.session_state.get('db_conectada'):
                    try:
                        st.session_state.ensayos_col.insert_one(record)
                    except Exception as e:
                        print(f"Silenced DB Error: {e}")
                    
                st.session_state.express_record = record
                st.session_state.fase_express = 'revision'
                st.rerun()

    # ---------------------------------------------------------
    # FASE 3: REVISIÓN DE PRÁCTICA EXPRESS
    # ---------------------------------------------------------
    elif st.session_state.fase_express == 'revision':
        record = st.session_state.express_record
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"## 📊 Resultado de tu Práctica")
        with col2:
            if st.button("⬅️ Volver al Diagnóstico", use_container_width=True):
                st.session_state.fase_express = 'configuracion'
                st.rerun()
                
        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje Logrado", f"{record['puntaje']} / {record['total']}")
        c2.metric("Nota Final", record['nota'])
        c3.metric("Precisión Global", f"{int((record['puntaje']/record['total'])*100) if record['total'] > 0 else 0}%")
        
        if record['total'] > 0 and record['puntaje'] == record['total']:
            st.balloons()
            st.success("¡Puntaje Perfecto! Sigue con este excelente ritmo. 🌟")
        elif record['puntaje'] == 0:
            st.error("No hay aciertos. Revisa las justificaciones abajo para identificar tus fallas. 📚")
        else:
            st.info("Buen intento. Analiza tus errores para asegurar un mejor puntaje en el próximo texto. 👍")

        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("### 📝 Análisis Detallado")
        
        aciertos = []
        fallos = []
        
        preguntas = record.get('preguntas_data', [])
        respuestas_u = record.get('respuestas_usuario', {})
        
        for i, p in enumerate(preguntas):
            pid = p['id']
            display_num = i + 1
            r_user = respuestas_u.get(pid)
            r_correcta_idx = p.get('correcta', 0)
            
            if isinstance(r_correcta_idx, int) and r_correcta_idx < len(p['opciones']):
                r_correcta_str = p['opciones'][r_correcta_idx]
            else:
                r_correcta_str = "Error de formato"
                
            es_correcta = (r_user == r_correcta_str)
            
            p_data = {
                'id': pid,
                'display_num': display_num,
                'enunciado': p['enunciado'],
                'tu_respuesta': r_user or 'Sin responder (Omitida)',
                'correcta': r_correcta_str,
                'explicacion': p.get('explicacion', 'No hay explicación disponible.'),
                'es_correcta': es_correcta
            }
            
            if es_correcta: aciertos.append(p_data)
            else: fallos.append(p_data)
            
        t_aciertos, t_fallos = st.tabs([f"✅ Acertaste ({len(aciertos)})", f"❌ Fallaste ({len(fallos)})"])
        
        with t_aciertos:
            if not aciertos:
                st.info("No tuviste aciertos en esta práctica.")
            for p in aciertos:
                with st.expander(f"✅ Pregunta {p['display_num']}"):
                    st.markdown(f"**{p['enunciado']}**")
                    st.markdown(f"<span style='color:#22C55E'>**Tu respuesta:** {p['tu_respuesta']}</span>", unsafe_allow_html=True)
                    st.info(f"**💡 Explicación del DEMRE:**\n\n{p['explicacion']}")
                    
        with t_fallos:
            if not fallos:
                st.success("¡Felicidades! No tuviste fallos en este texto.")
            for p in fallos:
                with st.expander(f"❌ Pregunta {p['display_num']}"):
                    st.markdown(f"**{p['enunciado']}**")
                    st.markdown(f"<span style='color:#EF4444'>**Tu respuesta:** {p['tu_respuesta']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#22C55E'>**Respuesta correcta:** {p['correcta']}</span>", unsafe_allow_html=True)
                    st.info(f"**💡 Explicación del DEMRE:**\n\n{p['explicacion']}")

# ==============================================================================
# 🟢 PANTALLAS SECUNDARIAS
# ==============================================================================
elif st.session_state.menu_actual == 'Mi Historial':
    @st.dialog("📋 REVISIÓN DETALLADA", width="large")
    def mostrar_detalle(datos):
        st.write(f"### Resumen del {datos['fecha'].strftime('%d/%m/%Y %H:%M')}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje", f"{datos['puntaje']}/{datos['total']}")
        c2.metric("Nota", datos['nota'])
        c3.markdown(f"**Nivel:** \n{datos.get('dificultad', 'DEMRE')}")
        st.divider()
        st.subheader("📝 Revisión de Preguntas")

        preguntas = datos.get('preguntas_data', [])
        respuestas_u = datos.get('respuestas_usuario', {})

        if not preguntas:
            st.warning("Este registro no tiene el detalle de preguntas.")
        else:
            for idx, p in enumerate(preguntas):
                pid = p.get('id', idx)
                display_num = idx + 1 
                r_usuario = respuestas_u.get(pid) or respuestas_u.get(str(pid)) or respuestas_u.get(str(idx))
                
                r_correcta_idx = p.get('correcta', 0)
                if isinstance(r_correcta_idx, int) and r_correcta_idx < len(p['opciones']):
                    r_correcta = p['opciones'][r_correcta_idx]
                else: r_correcta = "N/A"
                
                es_correcta = (r_usuario == r_correcta) if r_usuario else False
                icono = "✅" if es_correcta else "❌"
                
                with st.expander(f"{icono} Pregunta {display_num}: {p.get('enunciado', '')[:60]}..."):
                    st.write(f"**Pregunta:** {p.get('enunciado', '')}")
                    st.write(f"---")
                    if es_correcta:
                        st.success(f"**Tu respuesta:** {r_usuario} (Correcta)")
                    else:
                        st.error(f"**Tu respuesta:** {r_usuario}")
                        st.info(f"**Respuesta Correcta:** {r_correcta}")
                    st.markdown(f"**💡 Explicación:** {p.get('explicacion', '')}")
        
        if st.button("CERRAR VENTANA"): st.rerun()

    st.markdown('<div style="background: rgba(138,43,226,0.1); color: #8A2BE2; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; display: inline-block; margin-bottom: 10px; border: 1px solid rgba(138,43,226,0.3);">🟣 PANEL DE RESULTADOS HISTÓRICOS</div>', unsafe_allow_html=True)
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ VOLVER"): navegar_a('Home')
    with col_title:
        st.markdown(f"## 🕒 Historial de {st.session_state.usuario_actual}")

    if st.session_state.get('db_conectada', False):
        try:
            registros = list(st.session_state.ensayos_col.find({"usuario": st.session_state.usuario_actual}).sort("fecha", -1).limit(15))
            if not registros:
                st.info(f"No hay ensayos registrados para el estudiante: {st.session_state.usuario_actual}")
            else:
                for reg in registros:
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                        with c1:
                            st.markdown(f"📅 **{reg['fecha'].strftime('%d/%m/%Y | %H:%M')}**")
                            titulo_ens = reg.get('titulo_ensayo', 'Ensayo General')
                            if "⚡ Micro-Ensayo" in titulo_ens or "🎯 Práctica" in titulo_ens:
                                st.caption(f"<span style='color:#F59E0B;'>{titulo_ens}</span>", unsafe_allow_html=True)
                            else:
                                st.caption(f"Ensayo: {titulo_ens}")
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
    
    col_back, _ = st.columns([1.5, 5])
    with col_back:
        if st.button("⬅️ VOLVER AL MENÚ", use_container_width=True): 
            navegar_a('Home')
            
    st.markdown("## ⚙️ Configuración")
    
    if st.session_state.nivel_dificultad not in ["Básico", "Intermedio", "DEMRE", "Avanzado"]:
        st.session_state.nivel_dificultad = "DEMRE"
        
    st.session_state.nivel_dificultad = st.select_slider(
        "Dificultad:", 
        options=["Básico", "Intermedio", "DEMRE", "Avanzado"], 
        value=st.session_state.nivel_dificultad
    )

    # --- PANEL DE ADMINISTRADOR OCULTO ---
    st.markdown("<hr style='margin: 40px 0; border-top: 1px dashed var(--card-border);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #64748B;'>🔐 Zona de Administración (EdTech Lead)</h3>", unsafe_allow_html=True)
    
    admin_pass = st.text_input("Ingresa la credencial maestra para gestionar la Base de Datos:", type="password")
    
    if admin_pass == os.environ.get("ADMIN_PASS", ""):
        st.success("✅ Acceso Concedido: Privilegios de Administrador Activados")
        
        # ---------------------------------------------------------
        # GENERADORES SEPARADOS: ENSAYO COMPLETO VS BANCO EXPRESS
        # ---------------------------------------------------------
        col_adm1, col_admin2 = st.columns(2)
        
        with col_adm1:
            st.markdown("""
            <div style="background: #F0FDF4; border: 1px solid #86EFAC; border-radius: 12px; padding: 20px; margin-bottom: 20px; height: 130px;">
                <h4 style="margin-top: 0; color: #166534;">🏛️ Generar Ensayo Completo</h4>
                <p style="font-size: 13px; color: #15803D; margin-bottom: 0;">Genera un simulacro oficial (65 preguntas) para la biblioteca principal.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 GENERAR ENSAYO 65 P", type="primary", use_container_width=True):
                with st.status("🧠 Procesando Matriz 2027... (Tomará bastante tiempo)", expanded=True) as status:
                    try:
                        INSTRUCCIONES_DEL_GEM = f"""
INSTRUCCIÓN DE SISTEMA: MOTOR DE GENERACIÓN PAES LENGUAJE V9.0 (MASTER)

1. CONTEXTO DE ROL Y OBJETIVO
Actúa como un Senior UI/UX & Web Developer experto en la arquitectura de la App PAES Lenguaje Chile. Tu objetivo es diseñar la lógica de generación de ensayos siguiendo la Matriz Estadística 2024-2026, el Temario Oficial 2027 y protocolos de alta precisión técnica para evitar alucinaciones.

2. MATRIZ ESTADÍSTICA DE ESTRUCTURA (BACKEND CONSTRAINTS)
Volumen Total: Exactamente 65 preguntas (60 puntuables + 5 piloto).
Conteo de Textos: 7 a 8 textos. (Si hay 2 textos >1.100 palabras, fijar el total en 7).
Carga de Lectura: El total de palabras del ensayo debe oscilar entre 5.800 y 6.600.
Regla de Oro de Extensión (Distribución):
3 Textos Cortos: <700 palabras (Infografías/Discontinuos).
3 Textos Medianos: 700 - 1.000 palabras (Ensayos/Artículos).
2 Textos Largos: >1.000 palabras (Narrativa/Reportajes).
Ratio de Preguntas por Extensión:
Textos >1.200w: 10-12 preguntas.
Textos 400-600w: 6-8 preguntas.
Infografías: 5-7 preguntas.

3. LÓGICA DE CONTENIDO Y PESOS ESTADÍSTICOS (TEMARIO 2027)
Cada ensayo debe cumplir estrictamente con la distribución de frecuencia por habilidad y tarea:

A. Cuotas de Habilidad (Fijas)
- Localizar (25%): 16-17 preguntas.
- Relacionar e Interpretar (50%): 32-33 preguntas (Incluye 15% fijo de Vocabulario Contextual).
- Evaluar y Reflexionar (25%): 16-17 preguntas.

B. Mapeo de Tareas Lectoras (Frecuencia Target %)
No Literarios:
- NL1 Localizar: Información explícita (datos, hechos) [25.0%]
- NL2 Interpretar: Tema central del texto [12.0%]
- NL3 Interpretar: Síntesis de párrafos o secciones [10.0%]
- NL5 Interpretar: Tesis explícita o implícita [10.0%]
- NL7 Interpretar: Relación texto e infografía [5.0%]
- NL11 Evaluar: Perspectiva o intención del autor [6.0%]

Literarios:
- L6 Interpretar: Conflicto o problema humano [15.0%]
- L2 Interpretar: Evolución y motivaciones personajes [12.0%]
- L11 Evaluar: Perspectiva del narrador [10.0%]
- L9 Interpretar: Símbolos y tópicos literarios [5.0%]

4. PROTOCOLOS DE PRECISIÓN Y MEMORIA (REGLAS DE ORO)
ANTI-ALUCINACIÓN: Está estrictamente prohibido inventar textos incoherentes o entregar claves erróneas. Cada pregunta debe tener una y solo una respuesta correcta indiscutible.
GARANTÍA TEXTUAL: La "Clave" de cada pregunta debe estar respaldada 100% por marcas textuales reales. Prohibido basar respuestas en conocimiento externo.
MEMORIA ACUMULATIVA: Antes de redactar preguntas de una nueva lectura, revisa el historial de la sesión. Estás obligado a priorizar la evaluación de aquellas Tareas Lectoras y Conocimientos Oficiales que aún no se hayan preguntado para asegurar cobertura total del Temario.

5. CONFIGURACIÓN TÉCNICA (OBJETO JSON)
{{
  "engine_v9": {{
    "total_q": 65,
    "word_range": [5800, 6600],
    "skills": {{"localizar": 25, "interpretar": 50, "evaluar": 25}},
    "ui_tokens": {{"font": "Sans-Serif", "line_height": 1.6}},
    "safety": "STRICT_TEXTUAL_EVIDENCE"
  }}
}}

🛑 6. MODO DE EJECUCIÓN OBLIGATORIO (MAPPING A MONGODB STREAMLIT):
DEBES generar el ensayo COMPLETO AHORA MISMO (Los 7 u 8 textos y las 65 preguntas).
El campo "correcta" debe ser exclusivamente un NÚMERO (0, 1, 2, 3).
Tu respuesta DEBE SER ÚNICAMENTE UN OBJETO JSON VÁLIDO. No agregues comillas de markdown, solo el objeto puro para no romper la interfaz:
{{
  "titulo": "PAES Oficial Regular 2027 - Generado IA V9.0",
  "tipo": "ensayo_completo",
  "tiempo_limite": "02:30:00",
  "reporte_final": "Cumplimiento: 65 preguntas generadas, X palabras en total.",
  "textos": {{
    "1": {{ "titulo": "Texto 1: [Tema] (X palabras)", "contenido": "Párrafos con <br><br>" }},
    "2": {{ "titulo": "Texto 2: [Tema] (X palabras)", "contenido": "Párrafos con <br><br>" }}
    // ... generar todos los textos necesarios
  }},
  "preguntas": [
    {{
      "id": 1,
      "texto_id": "1",
      "enunciado": "¿...?",
      "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correcta": 1,
      "explicacion": "ID_TAREA: NL1 | HABILIDAD: Localizar | CLAVE_VALIDADA: ... JUSTIFICACIÓN: ..."
    }}
  ]
}}
Asegúrate de generar hasta la pregunta con "id": 65 y asociarlas correctamente a los "texto_id".
FIN DE LA INSTRUCCIÓN
"""
                        response = llamar_gemini(INSTRUCCIONES_DEL_GEM, st.session_state.api_key, status)
                        datos_ensayo = parsear_json_respuesta(response.text) if response else None
                        if datos_ensayo:
                            datos_ensayo['tipo'] = 'ensayo_completo'
                            if st.session_state.get('db_conectada'):
                                st.session_state.ensayos_oficiales_col.insert_one(datos_ensayo)
                            status.update(label="✅ Ensayo V5.0 publicado en la Biblioteca de Ensayos", state="complete")
                            st.balloons()
                        else:
                            st.error("🚨 La IA no devolvió un JSON válido. Intenta nuevamente.")
                    except Exception as e: st.error(f"🚨 Error Gemini: {e}")

        with col_admin2:
            st.markdown("""
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 20px; margin-bottom: 20px; height: 130px;">
                <h4 style="margin-top: 0; color: #B45309;">⚡ Generar Lote Express</h4>
                <p style="font-size: 13px; color: #92400E; margin-bottom: 0;">Genera textos cortos aislados para la Biblioteca de Práctica Express.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚡ GENERAR LOTE BANCO EXPRESS", type="primary", use_container_width=True):
                with st.status("🧠 Generando 3 textos cortos y 9 preguntas... (~20 seg)", expanded=True) as status:
                    try:
                        INSTRUCCIONES_EXPRESS = f"""
INSTRUCCIÓN DE SISTEMA: MOTOR DE GENERACIÓN PAES - BANCO EXPRESS
Objetivo: Generar un lote de textos cortos independientes para micro-aprendizaje.
Estructura: 3 textos cortos (250-350 palabras cada uno), de temas completamente diferentes.
Preguntas: 3 preguntas por cada texto (9 preguntas en total).

🛑 ESPECIFICACIÓN TÉCNICA OBLIGATORIA:
El campo "correcta" debe ser exclusivamente un NÚMERO (0, 1, 2, 3).
Tu respuesta DEBE SER ÚNICAMENTE UN OBJETO JSON VÁLIDO:
{{
  "titulo": "Banco Express - Lote Generado IA",
  "tipo": "banco_express",
  "textos": {{
    "1": {{ "titulo": "Micro-Ensayo 1: [Tema]", "contenido": "Párrafos con <br><br>" }},
    "2": {{ "titulo": "Micro-Ensayo 2: [Tema]", "contenido": "Párrafos con <br><br>" }},
    "3": {{ "titulo": "Micro-Ensayo 3: [Tema]", "contenido": "Párrafos con <br><br>" }}
  }},
  "preguntas": [
    {{
      "id": 1,
      "texto_id": "1",
      "enunciado": "¿...?",
      "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correcta": 1,
      "explicacion": "MACRO-HABILIDAD: ... TAREA ESPECÍFICA: ..."
    }}
    // ... generar hasta el ID 9 (asignar 3 a cada texto_id)
  ]
}}
FIN DE LA INSTRUCCIÓN
"""
                        response = llamar_gemini(INSTRUCCIONES_EXPRESS, st.session_state.api_key, status)
                        datos_lote = parsear_json_respuesta(response.text) if response else None
                        if datos_lote:
                            datos_lote['tipo'] = 'banco_express'
                            if st.session_state.get('db_conectada'):
                                st.session_state.ensayos_oficiales_col.insert_one(datos_lote)
                            status.update(label="✅ Lote publicado en el Banco de Práctica Express", state="complete")
                            st.balloons()
                        else:
                            st.error("🚨 La IA no devolvió un JSON válido. Intenta nuevamente.")
                    except Exception as e: st.error(f"🚨 Error Gemini: {e}")

        # ---------------------------------------------------------
        # INYECCIÓN MANUAL MEDIANTE ARCHIVO
        # ---------------------------------------------------------
        st.markdown("<hr style='border-top: 1px dashed var(--card-border);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #64748B;'>📂 Cargar Archivo Manual (Backup)</h4>", unsafe_allow_html=True)
        
        destino_manual = st.selectbox("Destino del Archivo JSON:", ["Ensayo Completo", "Banco Express"])
        archivo_json = st.file_uploader("Sube el archivo .json generado externamente", type=["json"])
        
        if archivo_json is not None:
            try:
                datos_ensayo = json.load(archivo_json)
                if "titulo" in datos_ensayo and "preguntas" in datos_ensayo:
                    st.info(f"📄 Archivo detectado: **{datos_ensayo['titulo']}** ({len(datos_ensayo['preguntas'])} preguntas)")
                    
                    if st.button("⚡ INYECTAR MANUALMENTE", type="primary"):
                        # Etiquetar el archivo según la selección del administrador
                        if destino_manual == "Ensayo Completo":
                            datos_ensayo['tipo'] = 'ensayo_completo'
                        else:
                            datos_ensayo['tipo'] = 'banco_express'
                            
                        if st.session_state.get('db_conectada'):
                            st.session_state.ensayos_oficiales_col.insert_one(datos_ensayo)
                            st.balloons()
                            st.success("🚀 ¡Inyectado exitosamente en MongoDB! Ya está en vivo.")
                        else:
                            st.error("❌ No hay conexión a la Base de Datos.")
                else:
                    st.error("❌ El archivo JSON no tiene el formato estructural correcto.")
            except Exception as e:
                st.error(f"❌ Error al leer el archivo JSON: {e}")

# --- FIN DE CODIGO ---
# --- main.py ---
# --- App PAES Lenguaje Chile ---