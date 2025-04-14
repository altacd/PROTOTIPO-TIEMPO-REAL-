
import sqlite3
import threading
import time
import random

# Configuración inicial de la base de datos (solo para prototipo local)
def init_db(nombre_db):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            estado TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transacciones (
            id_transaccion INTEGER PRIMARY KEY,
            id_usuario INTEGER,
            monto REAL,
            tipo TEXT,
            fecha_hora TEXT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
        );
    """)
    conn.commit()
    conn.close()

# Inserta datos en tiempo real
def insertar_transaccion(db_path, id_usuario, monto, tipo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transacciones (id_usuario, monto, tipo, fecha_hora) VALUES (?, ?, ?, datetime('now'))",
                   (id_usuario, monto, tipo))
    conn.commit()
    conn.close()

# Hebra simulando eventos en tiempo real
def simulador_eventos(db_path):
    while True:
        id_usuario = random.randint(1, 3)
        monto = random.uniform(10.0, 500.0)
        tipo = random.choice(["deposito", "retiro"])
        insertar_transaccion(db_path, id_usuario, monto, tipo)
        print(f"Evento procesado: Usuario {id_usuario}, Monto {monto:.2f}, Tipo {tipo}")
        time.sleep(random.uniform(0.5, 2.0))

# Inicializar y poblar datos de ejemplo
def poblar_usuarios(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO Usuarios (nombre, email, estado) VALUES (?, ?, ?)", [
        ("Joel Gómez", "joel@example.com", "activo"),
        ("Laura Pérez", "laura@example.com", "activo"),
        ("Carlos Núñez", "carlos@example.com", "inactivo"),
    ])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db = "tiempo_real.db"
    init_db(db)
    poblar_usuarios(db)

    # Iniciar hebra
    hilo = threading.Thread(target=simulador_eventos, args=(db,), daemon=True)
    hilo.start()

    # Esperar para simular sistema corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Sistema detenido.")
