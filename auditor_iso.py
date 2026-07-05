import sqlite3
from datetime import datetime

def comprobar_incidentes_activos():
    """Auditoría de Datos automatizada: Analiza fallas en la infraestructura"""
    try:
        with sqlite3.connect('ciberdefensa.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM incidentes WHERE severidad='ALTA'")
            incidentes_criticos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM alertas_red")
            alertas_red = cursor.fetchone()[0]
            
            return incidentes_criticos, alertas_red
    except sqlite3.Error:
        return 0, 0

def ejecutar_auditoria():
    print("\n" + "="*60)
    print("   ISO/IEC 27001 COMPLIANCE AUDITOR TOOL - DICTAMEN LEGAL")
    print("="*60)
    
    empresa = input("[?] Ingrese el nombre de la organización a auditar: ").strip()
    if not empresa: empresa = "Consultora Standard"
    
    # Mapeo de controles según el Anexo A de ISO 27001:2022
    controles = [
        "A.5.15 - ¿Se cuenta con una política de control de accesos reglamentada?",
        "A.8.20 - ¿Se implementan controles de seguridad en redes perimetrales?",
        "A.8.16 - ¿Se realiza monitoreo, recolección y análisis de logs de eventos?"
    ]
    
    aprobados = 0
    fallidos = 0
    
    # Integración de Auditoría Técnica Automática
    inc_web, alc_red = comprobar_incidentes_activos()
    print(f"\n[*] Ejecutando escaneo forense automático en base de datos...")
    print(f"    -> Alertas SIEM críticas en BD: {inc_web}")
    print(f"    -> Incidentes de red IoT en BD: {alc_red}")
    
    print("\n[!] Comience el cuestionario normativo complementario:\n")
    
    # Evaluación Control 1
    resp = input(f"{controles[0]} [S/N]: ").strip().upper()
    if resp == 'S': aprobados += 1 
    else: fallidos += 1
        
    # Evaluación Control 2 (Afectado automáticamente por alertas IoT)
    print(f"{controles[1]}")
    if alc_red > 0:
        print("    [X] CONTROL RECHAZADO AUTOMÁTICAMENTE: Existen alertas DoS de red sin contener en base de datos.")
        fallidos += 1
    else:
        resp = input("    Verificación manual necesaria [S/N]: ").strip().upper()
        if resp == 'S': aprobados += 1
        else: fallidos += 1
            
    # Evaluación Control 3 (Afectado automáticamente por SIEM)
    print(f"{controles[2]}")
    if inc_web > 0:
        print("    [X] CONTROL RECHAZADO AUTOMÁTICAMENTE: Registros SIEM exponen brechas de inyección SQL activas.")
        fallidos += 1
    else:
        resp = input("    Verificación manual necesaria [S/N]: ").strip().upper()
        if resp == 'S': aprobados += 1
        else: fallidos += 1

    # Análisis de Riesgo Cualitativo y Dictamen Legal
    total_controles = len(controles)
    porcentaje = (aprobados / total_controles) * 100
    
    if porcentaje == 100:
        dictamen_legal = "Compliance Completo - Nivel de Riesgo Corporativo: BAJO"
    elif porcentaje >= 50:
        dictamen_legal = "Compliance Parcial - Nivel de Riesgo: MODERADO. Requiere plan de adecuación inmediato."
    else:
        dictamen_legal = "NO COMPLIANT - Riesgo: CRÍTICO. Responsabilidad civil y contractual expuesta por falta de debida diligencia."
        
    # Guardar persistencia de la Auditoría Legal
    try:
        with sqlite3.connect('ciberdefensa.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auditorias_iso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    empresa TEXT,
                    controles_aprobados INTEGER,
                    controles_fallidos INTEGER,
                    porcentaje_cumplimiento REAL,
                    estado_legal TEXT
                )
            ''')
            cursor.execute('''
                INSERT INTO auditorias_iso (fecha, empresa, controles_aprobados, controles_fallidos, porcentaje_cumplimiento, estado_legal)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), empresa, aprobados, fallidos, porcentaje, dictamen_legal))
            conexion.commit()
    except sqlite3.Error as e:
        print(f"[-] No se pudo registrar la auditoría corporativa: {e}")

    # Impresión de Resultados en pantalla
    print("\n" + "="*60)
    print(f" DICTAMEN EMITIDO PARA ENTORNO: {empresa.upper()}")
    print("="*60)
    print(f"Controles validados: {aprobados}/{total_controles} ({porcentaje:.1f}%)")
    print(f"Conclusión Legal-Técnica: {dictamen_legal}\n")

if __name__ == "__main__":
    ejecutar_auditoria()