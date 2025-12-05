import mysql.connector


def conectar():
    """Establece la conexión a la base de datos."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",  # MODIFICAR si tu root tiene contraseña
            database="greenup_db"
        )
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

# --- Funciones CRUD Corregidas ---
# ---------------------------------

## 📝 Registrar Usuario
def registrar_usuario():
    print("\n--- REGISTRAR USUARIO ---")
    
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    # Usamos 'usuario' (que actúa como email/username) y 'password_hash'
    usuario = input("Email/Usuario: ")
    password_hash = input("Contraseña (se guardará sin hash): ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Se corrige la consulta y se usan los nombres de columna correctos (usuario, password_hash)
    query = """
        INSERT INTO usuarios (nombre, apellido, usuario, password_hash)
        VALUES (%s, %s, %s, %s)
    """
    datos = (nombre, apellido, usuario, password_hash)

    try:
        cursor.execute(query, datos)
        conexion.commit() # ¡COMMIT es esencial para guardar los cambios!
        print("\nUsuario registrado con éxito.\n")
    except mysql.connector.Error as err:
        print(f"\nError al registrar el usuario: {err}")
        conexion.rollback() # Revierte los cambios si hay error
    finally:
        # Se cierran la conexión y el cursor dentro del bloque de manejo de errores.
        cursor.close()
        conexion.close()


## 🔑 Iniciar Sesión
def iniciar_sesion():
    print("\n--- INICIO DE SESIÓN ---")
    # Se usa 'usuario' para el login
    usuario = input("Email/Usuario: ")
    # Se usa 'password_hash' para la contraseña
    password_input = input("Contraseña: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Consulta ajustada a 'usuario' y 'password_hash'
    query = "SELECT id, nombre, apellido FROM usuarios WHERE usuario = %s AND password_hash = %s"
    cursor.execute(query, (usuario, password_input))
    resultado = cursor.fetchone()

    if resultado:
        print(f"\nBienvenido {resultado[1]} {resultado[2]} (ID: {resultado[0]})\n")
    else:
        print("\nCredenciales incorrectas.\n")

    cursor.close()
    conexion.close()


## 🔎 Consultar Usuario por ID
def consultar_usuario():
    print("\n--- CONSULTAR USUARIO ---")
    user_id = input("ID del usuario: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    cursor.execute("SELECT id, usuario, nombre, apellido, fecha_registro FROM usuarios WHERE id = %s", (user_id,))
    resultado = cursor.fetchone()

    if resultado:
        print("\nDatos del usuario:")
        print(f"ID: {resultado[0]}, Email/Usuario: {resultado[1]}, Nombre: {resultado[2]}, Apellido: {resultado[3]}, Registro: {resultado[4]}")
    else:
        print("\nNo existe un usuario con ese ID.")

    cursor.close()
    conexion.close()


## ✏️ Modificar Datos del Usuario (Nombre y Apellido)
def modificar_usuario():
    print("\n--- MODIFICAR DATOS (Nombre y Apellido) ---")
    user_id = input("ID del usuario: ")
    
    # Se solicitan los campos que están en la tabla greenup_db
    nuevo_nombre = input("Nuevo nombre: ")
    nuevo_apellido = input("Nuevo apellido: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # La consulta se ajusta para modificar nombre y apellido
    query = """
        UPDATE usuarios
        SET nombre = %s, apellido = %s
        WHERE id = %s
    """
    
    try:
        cursor.execute(query, (nuevo_nombre, nuevo_apellido, user_id))
        conexion.commit()
        print("\nDatos modificados correctamente.\n")
    except mysql.connector.Error as err:
        print(f"\nError al modificar datos: {err}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()


## 🔒 Modificar Contraseña
def modificar_password():
    print("\n--- CAMBIAR CONTRASEÑA ---")
    user_id = input("ID del usuario: ")
    nueva_pass = input("Nueva contraseña: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Columna cambiada a 'password_hash'
    query = "UPDATE usuarios SET password_hash = %s WHERE id = %s"
    
    try:
        cursor.execute(query, (nueva_pass, user_id))
        conexion.commit()
        print("\nContraseña actualizada.\n")
    except mysql.connector.Error as err:
        print(f"\nError al actualizar contraseña: {err}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()


## ❌ Eliminar Usuario
def eliminar_usuario():
    print("\n--- ELIMINAR USUARIO ---")
    user_id = input("ID del usuario: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        conexion.commit()
        print("\nUsuario eliminado correctamente.\n")
    except mysql.connector.Error as err:
        print(f"\nError al eliminar usuario: {err}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()

# --- Menú principal ---
def menu():
    while True:
        print("\n========= MENÚ PRINCIPAL (greenup_db) =========")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Consultar usuario (por ID)")
        print("4. Modificar datos (Nombre y Apellido)")
        print("5. Cambiar contraseña")
        print("6. Eliminar usuario")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            consultar_usuario()
        elif opcion == "4":
            modificar_usuario()
        elif opcion == "5":
            modificar_password()
        elif opcion == "6":
            eliminar_usuario()
        elif opcion == "7":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

# -------------------------------------
# EJECUCIÓN
# -------------------------------------
if __name__ == "__main__":
    menu()