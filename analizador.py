import sqlite3
import re
import os
from datetime import datetime

# 1. Configuración de la Base de Datos SQL Centralizada
def inicializar_bd():
    try:
        conexion = sqlite3.connect('ciberdefensa.db')
        cursor = conexion.cursor()
        # Tabla de incidentes web (SIEM)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidentes (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                ip TEXT NOT EXISTS,\
                fecha TEXT NOT EXISTS,\
                tipo_ataque TEXT NOT EXISTS,\
                payload TEXT,\
                severidad TEXT\
            )
        ''')
        # Nueva Tabla: Alertas de Red Perimetral (IoT) para correlación de datos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertas_red (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                fecha TEXT NOT EXISTS,\
                dispositivo TEXT NOT EXISTS,\
                ip TEXT NOT EXISTS,\
                metricas TEXT NOT EXISTS,\
                tipo_alerta TEXT\
            )
        ''')
        conexion.commit()
    except sqlite3.Error as e:
        print(f"[-] Error crítico al inicializar la base de datos: {e}")
    finally:
        conexion.close()

# 2. Función para registrar los incidentes con cálculo de severidad
def registrar_incidente(ip, fecha, tipo_ataque, payload):
    # Lógica de negocio/ciberdefensa: clasificar la severidad según el vector
    severidad = "ALTA" if tipo_ataque == "SQL Injection" else "MEDIA"
    
    try:
        with sqlite3.connect('ciberdefensa.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO incidentes (ip, fecha, tipo_ataque, payload, severidad)
                VALUES (?, ?, ?, ?, ?)
            ''', (ip, fecha, tipo_ataque, payload, severidad))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"[-] Error al guardar evidencia digital en SQL: {e}")

# 3. Procesador de Logs Profesional
def analizar_logs(archivo_ruta):
    inicializar_bd()
    print(f"[*] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando motor SIEM Log Parser...")
    
    if not os.path.exists(archivo_ruta):
        print(f"[-] Error: El archivo de logs '{archivo_ruta}' no existe. Creando uno de prueba...")
        with open(archivo_ruta, 'w') as f:
            f.write('192.168.1.100 - [05/Jul/2026:14:32:10] "GET /index.php?id=1\' OR \'1\'=\'1" 200\n')
            f.write('10.0.0.45 - [05/Jul/2026:14:35:15] "POST /login HTTP/1.1" 401\n')
    
    contador = 0
    with open(archivo_ruta, 'r') as archivo:
        for linea in archivo:
            patron = r'^([\d\.]+) - \[(.*?)\] "(.*?)" (\d+)'
            match = re.match(patron, linea)
            
            if match:
                ip = match.group(1)
                fecha = match.group(2)
                peticion = match.group(3)
                estado = match.group(4)
                
                # Regla 1: Detección de SQL Injection (OWASP Top 10)
                if any(indicador in peticion.upper() for indicador in ["OR", "'", "--", "UNION", "SELECT"]):
                    print(f"[ALERTA CRÍTICA] SQLi detectado desde la IP {ip}")
                    registrar_incidente(ip, fecha, "SQL Injection", peticion)
                    contador += 1
                
                # Regla 2: Intentos de Fuerza Bruta (Detección por código de estado HTTP)
                elif "/login" in peticion.lower() and estado == "401":
                    print(f"[ALERTA MEDIA] Intento de autenticación fallido desde la IP {ip}")
                    registrar_incidente(ip, fecha, "Fuerza Bruta", peticion)
                    contador += 1
                    
    print(f"[+] Análisis finalizado. Se han integrado {contador} eventos a la base de datos relacional.")

if __name__ == "__main__":
    analizar_logs("access.log")