import sqlite3
import re

# 1. Configuración de la Base de Datos SQL
def inicializar_bd():
    conexion = sqlite3.connect('ciberdefensa.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            fecha TEXT,
            tipo_ataque TEXT,
            payload TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# 2. Función para registrar los incidentes en la BD
def registrar_incidente(ip, fecha, tipo_ataque, payload):
    conexion = sqlite3.connect('ciberdefensa.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO incidentes (ip, fecha, tipo_ataque, payload)
        VALUES (?, ?, ?, ?)
    ''', (ip, fecha, tipo_ataque, payload))
    conexion.commit()
    conexion.close()

# 3. Procesador de Logs (El motor de detección)
def analizar_logs(archivo_ruta):
    inicializar_bd()
    print("[*] Iniciando analisis de logs...")
    
    with open(archivo_ruta, 'r') as archivo:
        for linea in archivo:
            patron = r'^([\d\.]+) - \[(.*?)\] "(.*?)" (\d+)'
            match = re.match(patron, linea)
            
            if match:
                ip = match.group(1)
                fecha = match.group(2)
                peticion = match.group(3)
                estado = match.group(4)
                
                # Regla 1: Intentos de SQL Injection
                if "OR" in peticion or "'" in peticion or "--" in peticion:
                    print(f"[ALERTA] SQLi detectado desde la IP {ip}")
                    registrar_incidente(ip, fecha, "SQL Injection", peticion)
                
                # Regla 2: Fuerza Bruta
                if "/login" in peticion and estado == "401":
                    print(f"[ALERTA] Intento de login fallido desde la IP {ip}")
                    registrar_incidente(ip, fecha, "Fuerza Bruta (Intento)", peticion)

    print("[+] Analisis finalizado. Resultados guardados en ciberdefensa.db")

if __name__ == "__main__":
    analizar_logs('access.log')