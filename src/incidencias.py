from __future__ import annotations
from mysql.connector.connection import MySQLConnection
from src.db import execute, fetch_all

def listar_incidencias_activas(conn: MySQLConnection) -> list[dict]:
    sql = """SELECT * FROM incidencias WHERE estado <> 'cerrada' 
             ORDER BY CASE prioridad WHEN 'alta' THEN 1 WHEN 'media' THEN 2 WHEN 'baja' THEN 3 END ASC, fecha_apertura ASC"""
    return fetch_all(conn, sql)

def listar_incidencias_sin_tecnico(conn: MySQLConnection) -> list[dict]:
    sql = "SELECT * FROM incidencias WHERE tecnico_id IS NULL AND estado <> 'cerrada' ORDER BY fecha_apertura ASC"
    return fetch_all(conn, sql)

def crear_incidencia(conn: MySQLConnection, equipo_id: int, descripcion: str, prioridad: str = "media") -> int:
    if not descripcion.strip() or prioridad not in ('baja', 'media', 'alta') or equipo_id <= 0:
        raise ValueError("Datos de incidencia inválidos.")
    sql = "INSERT INTO incidencias (equipo_id, descripcion, prioridad, estado, fecha_apertura) VALUES (%s, %s, %s, 'abierta', NOW())"
    return execute(conn, sql, (equipo_id, descripcion.strip(), prioridad))

def asignar_tecnico(conn: MySQLConnection, incidencia_id: int, tecnico_id: int) -> int:
    if incidencia_id <= 0 or tecnico_id <= 0: raise ValueError("IDs inválidos.")
    sql = "UPDATE incidencias SET tecnico_id = %s, estado = 'en_proceso' WHERE id = %s AND estado <> 'cerrada'"
    return execute(conn, sql, (tecnico_id, incidencia_id))

def cerrar_incidencia(conn: MySQLConnection, incidencia_id: int) -> int:
    if incidencia_id <= 0: raise ValueError("ID inválido.")
    sql = "UPDATE incidencias SET estado = 'cerrada', fecha_cierre = NOW() WHERE id = %s AND estado <> 'cerrada'"
    return execute(conn, sql, (incidencia_id,))

def detalle_incidencias_join(conn: MySQLConnection) -> list[dict]:
    sql = """SELECT i.id, i.descripcion, i.prioridad, i.estado, i.fecha_apertura, i.fecha_cierre,
             e.tipo, e.modelo, e.ubicacion, e.estado AS estado_equipo, t.nombre AS tecnico
             FROM incidencias i JOIN equipos e ON i.equipo_id = e.id LEFT JOIN tecnicos t ON i.tecnico_id = t.id
             ORDER BY i.estado ASC, CASE i.prioridad WHEN 'alta' THEN 1 WHEN 'media' THEN 2 WHEN 'baja' THEN 3 END ASC, i.fecha_apertura ASC"""
    return fetch_all(conn, sql)


