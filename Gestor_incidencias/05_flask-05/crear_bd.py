import sqlite3

def inicializar_bd():
    """Crea el esquema de la base de datos y carga los datos maestros iniciales."""
    with sqlite3.connect("incidencias.db") as con:
        cursor = con.cursor()
        
        # ACTIVAR RESTRICCIONES DE CLAVE FORÁNEA
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        #  TABLAS MAESTRAS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY, 
                nombre TEXT NOT NULL, 
                turno TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salas (
                id INTEGER PRIMARY KEY, 
                nombre TEXT NOT NULL, 
                ubicacion TEXT
            )
        """)
        
        #  TABLA PRINCIPAL 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidencias (
                id INTEGER PRIMARY KEY,
                tecnico_id INTEGER NOT NULL,
                sala_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT NOT NULL,
                resolucion TEXT,
                fecha_apertura TEXT NOT NULL,
                fecha_cierre TEXT,
                FOREIGN KEY(tecnico_id) REFERENCES tecnicos(id),
                FOREIGN KEY(sala_id) REFERENCES salas(id)
            )
        """)
        
        # CARGA DE DATOS INICIALES SEMILLA
        # Técnicos iniciales (Evita duplicados)
        cursor.executemany("INSERT OR IGNORE INTO tecnicos (id, nombre, turno) VALUES (?, ?, ?)", 
                           [(1, 'Juan', 'Mañana'), 
                            (2, 'Ana', 'Tarde'), 
                            (3, 'Pedro', 'Noche')])
        
        # Salas iniciales con ID fijo para mantener consistencia en las pruebas
        cursor.executemany("INSERT OR IGNORE INTO salas (id, nombre, ubicacion) VALUES (?, ?, ?)",
                           [(1, 'Sala de Emergencias', 'Planta 1'), 
                            (2, 'Sala de Comunicaciones', 'Planta 0'),
                            (3, 'Sala de Control', 'Planta baja')])
        
        con.commit()
    print("✔ Base de datos 'incidencias.db' inicializada y protegida con éxito.")

if __name__ == "__main__":
    inicializar_bd()