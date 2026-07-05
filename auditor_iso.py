import sqlite3
from datetime import datetime

# 1. Creamos la base de datos para las auditorías de cumplimiento
def preparar_bd_auditoria():
    conexion = sqlite3.connect('ciberdefensa.db') # Usamos la misma BD para centralizar todo
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
    conexion.commit()
    conexion.close()

# 2. Función para guardar el resultado del reporte legal-técnico
def guardar_auditoria(empresa, aprobados, fallidos, porcentaje, estado):
    conexion = sqlite3.connect('ciberdefensa.db')
    cursor = conexion.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO auditorias_iso (fecha, empresa, controles_aprobados, controles_fallidos, porcentaje_cumplimiento, estado_legal)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (fecha_actual, empresa, aprobados, fallidos, porcentaje, estado))
    conexion.commit()
    conexion.close()

# 3. El motor del cuestionario de cumplimiento (ISO 27001)
def ejecutar_auditoria():
    preparar_bd_auditoria()
    
    print("\n" + "="*60)
    print("   SISTEMA AUTOMATIZADO DE AUDITORÍA DE COMPLIANCE - ISO 27001")
    print("="*60)
    
    empresa = input("Nombre de la organización a evaluar: ")
    
    # Lista de controles clave de la norma ISO 27001
    controles = [
        "¿La empresa cuenta con una Política de Seguridad de la Información documentada y firmada? (A.5.1.1)",
        "¿Se realizan análisis de vulnerabilidades y pruebas de penetración periódicas? (A.12.6.1)",
        "¿Existe un registro formal y actualizado de incidentes de seguridad? (A.16.1.4)",
        "¿El acceso a las bases de datos de producción está restringido y cifrado? (A.9.4.1)",
        "¿Se cumple estrictamente con la Ley de Protección de Datos Personales en el almacenamiento? (A.18.1.1)"
    ]
    
    aprobados = 0
    fallidos = 0
    
    print("\nResponda con 'S' para SÍ o 'N' para NO a los siguientes controles regulatorios:\n")
    
    for i, control in enumerate(controles, 1):
        respuesta = input(f"Control {i}: {control} [S/N]: ").strip().upper()
        if respuesta == 'S':
            aprobados += 1
        else:
            fallidos += 1
            
    # Cálculos estadísticos básicos de riesgo
    total_controles = len(controles)
    porcentaje_cumplimiento = (aprobados / total_controles) * 100
    
    # Criterio legal/tecnológico para el dictamen
    if porcentaje_cumplimiento == 100:
        estado_legal = "Cumplimiento Total - Riesgo Bajo"
    elif porcentaje_cumplimiento >= 60:
        estado_legal = "Cumplimiento Parcial - Riesgo Moderado (Requiere plan de acción)"
    else:
        estado_legal = "No Compliant - Riesgo Crítico (Pasible de sanciones legales)"
        
    # Guardamos en SQL
    guardar_auditoria(empresa, aprobados, fallidos, porcentaje_cumplimiento, estado_legal)
    
    # Mostrar dictamen en pantalla
    print("\n" + "-"*60)
    print(f" RESULTADO DICTAMEN LEGAL-TÉCNICO PARA: {empresa.upper()}")
    print("-"*60)
    print(f"Controles Acreditados: {aprobados}/{total_controles}")
    print(f"Controles No Acreditados: {fallidos}/{total_controles}")
    print(f"Porcentaje de Cumplimiento Normativo: {porcentaje_cumplimiento}%")
    print(f"Dictamen del Auditor: {estado_legal}")
    print("="*60)
    print("[+] Evaluación registrada con éxito en la base de datos central.\n")

if __name__ == "__main__":
    ejecutar_auditoria()