import os
from dotenv import load_dotenv
import certifi
import dns.resolver  # INYECCIÓN: Librería para controlar redes
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st

# 🔒 Cargar las variables de entorno desde el archivo .env Oculto
load_dotenv()

# 🛡️ BYPASS DE DNS (HACK): Forzamos el uso de Google DNS (8.8.8.8) 
# Esto evita que los proveedores de internet chilenos bloqueen la conexión SRV.
try:
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    dns.resolver.default_resolver = resolver
    print("[OK] Bypass de DNS de Google activado con exito.")
except Exception as e:
    print(f"[WARN] No se pudo aplicar el Bypass DNS: {e}")

# ⚠️ URL EXTRAÍDA DE FORMA SEGURA DESDE EL ENTORNO
MONGO_URI = os.getenv("MONGO_URI")

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
        print(f"[ERROR] Error de conexion de seguridad: {error_msg}")
        return None, error_msg