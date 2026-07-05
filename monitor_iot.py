import random
import time
import sqlite3
from datetime import datetime

def registrar_alerta_red(dispositivo, ip, metricas, tipo_alerta):
    try:
        with sqlite3.connect('ciberdefensa.db') as conexion:
            cursor = conexion.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO alertas_red (fecha, dispositivo, ip, metricas, tipo_alerta)
                VALUES (?, ?, ?, ?, ?)
            ''', (fecha_actual, dispositivo, ip, metricas, tipo_alerta))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"[-] Error de persistencia en red IoT: {e}")

def simular_trafico_iot():
    print("\n" + "="*60)
    print("   SISTEMA DE MONITOREO DE TRÁFICO IoT & ANOMALÍAS DE RED")
    print("="*60)
    print("[+] Inicializando sensores y captura perimetral en tiempo real...\n")
    
    dispositivos = {
        "192.168.1.50": "Cámara de Seguridad Principal",
        "192.168.1.55": "Sensor de Acceso Biométrico",
        "192.168.1.60": "Servidor de Archivos Legales"
    }
    
    UMBRAL_DOS = 150 
    
    try:
        for i in range(3): # Reducimos ciclos para pruebas rápidas
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Analizando ráfaga de tráfico N° {i+1}...")
            time.sleep(1)
            
            for ip, nombre in dispositivos.items():
                paquetes = random.randint(10, 220)
                print(f" -> {nombre} ({ip}): {paquetes} req/seg", end="")
                
                if paquetes > UMBRAL_DOS:
                    print(" | ⚠️ [ALERTA] Anomalía detectada: Posible Ataque DoS.")
                    registrar_alerta_red(
                        dispositivo=nombre, 
                        ip=ip, 
                        metricas=f"{paquetes} req/seg (Umbral max: {UMBRAL_DOS})", 
                        tipo_alerta="Denegación de Servicio (DoS)"
                    )
                else:
                    print(" | [OK] Tráfico Normal.")
            print("-" * 50)
    except KeyboardInterrupt:
        print("\n[-] Monitoreo detenido por el operador de Ciberdefensa.")

if __name__ == "__main__":
    simular_trafico_iot()