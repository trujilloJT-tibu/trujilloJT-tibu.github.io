import sqlite3

def generar_reporte_incidentes():
    # Nos conectamos a la base de datos que creó el script anterior
    conexion = sqlite3.connect('ciberdefensa.db')
    cursor = conexion.cursor()
    
    # Consulta SQL pura para traer los datos ordenados por tipo de ataque
    consulta_sql = "SELECT ip, fecha, tipo_ataque FROM incidentes ORDER BY tipo_ataque ASC"
    cursor.execute(consulta_sql)
    
    # Recuperamos todas las filas que devolvió la consulta
    incidentes = cursor.fetchall()
    
    # Cerramos la conexión por seguridad y buenas prácticas
    conexion.close()
    
    # Mostramos los resultados de forma prolija en la pantalla
    print("\n" + "="*60)
    print("      REPORTE DE INCIDENTES DE SEGURIDAD - AUDITORÍA ISO 27001")
    print("="*60)
    print(f"{'DIRECCIÓN IP':<18} | {'FECHA / HORA':<22} | {'TIPO DE AMENAZA'}")
    print("-"*60)
    
    for registro in incidentes:
        ip, fecha, tipo_ataque = registro
        print(f"{ip:<18} | {fecha:<22} | {tipo_ataque}")
        
    print("="*60)
    print(f"Total de anomalías registradas en la base de datos: {len(incidentes)}\n")

if __name__ == "__main__":
    generar_reporte_incidentes()