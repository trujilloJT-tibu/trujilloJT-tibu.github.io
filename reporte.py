import sqlite3

def generar_reporte_incidentes():
    print("\n" + "="*70)
    print("      REPORTE DE INCIDENTES DE SEGURIDAD - AUDITORÍA ISO 27001")
    print("="*70)
    
    try:
        with sqlite3.connect('ciberdefensa.db') as conexion:
            cursor = conexion.cursor()
            
            # Consulta Avanzada 1: Consolidado de Ataques Web (SIEM)
            consulta_siem = "SELECT ip, fecha, tipo_ataque, severidad FROM incidentes ORDER BY severidad DESC, fecha DESC"
            cursor.execute(consulta_siem)
            incidentes = cursor.fetchall()
            
            print(f"{'DIRECCIÓN IP':<15} | {'FECHA / HORA':<20} | {'TIPO AMENAZA':<15} | {'SEVERIDAD'}")
            print("-" * 70)
            for reg in incidentes:
                print(f"{reg[0]:<15} | {reg[1]:<20} | {reg[2]:<15} | {reg[3]}")
                
            print(f"\n[i] Total de anomalías web en base de datos: {len(incidentes)}")
            print("="*70)
            
            # Consulta Avanzada 2 (Mapeo de Red IoT): Métricas agregadas de atacantes recurrentes
            print("\n      TOP IPS CON ALERTAS DE ANOMALÍAS DE RED (MONITOREO IoT)")
            print("-" * 70)
            consulta_iot = """
                SELECT ip, dispositivo, COUNT(*) as cantidad, tipo_alerta 
                FROM alertas_red 
                GROUP BY ip 
                ORDER BY cantidad DESC
            """
            cursor.execute(consulta_iot)
            alertas = cursor.fetchall()
            
            print(f"{'DIRECCIÓN IP':<15} | {'DISPOSITIVO OBJETIVO':<30} | {'ALERTAS':<8} | {'VECTOR'}")
            print("-" * 70)
            for alerta in alertas:
                print(f"{alerta[0]:<15} | {alerta[1]:<30} | {alerta[2]:<8} | {alerta[3]}")
                
    except sqlite3.Error as e:
        print(f"[-] Error al generar reportes de auditoría forense: {e}")

if __name__ == "__main__":
    generar_reporte_incidentes()