from __future__ import annotations
import sys
import os

# Añadimos la raíz al path para evitar líos de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db import get_connection
from src.incidencias import (
    asignar_tecnico, cerrar_incidencia, crear_incidencia,
    detalle_incidencias_join, listar_incidencias_activas, listar_incidencias_sin_tecnico
)

def main() -> None:
    try:
        conn = get_connection()
        while True:
            print("\n=== STI Incidencias ===")
            print("1) Listar activas | 2) Sin técnico | 3) Crear | 4) Asignar | 5) Cerrar | 6) Detalle | 0) Salir")
            op = input("Opción: ").strip()
            if op == "0": break
            
            if op == "1":
                for r in listar_incidencias_activas(conn): print(r)
            elif op == "2":
                for r in listar_incidencias_sin_tecnico(conn): print(r)
            elif op == "3":
                eid = int(input("equipo_id: "))
                desc = input("descripcion: ")
                prio = input("prioridad (baja/media/alta): ") or "media"
                print(f"Filas: {crear_incidencia(conn, eid, desc, prio)}")
            elif op == "4":
                iid = int(input("incidencia_id: "))
                tid = int(input("tecnico_id: "))
                print(f"Filas: {asignar_tecnico(conn, iid, tid)}")
            elif op == "5":
                iid = int(input("incidencia_id: "))
                print(f"Filas: {cerrar_incidencia(conn, iid)}")
            elif op == "6":
                for r in detalle_incidencias_join(conn): print(r)
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


