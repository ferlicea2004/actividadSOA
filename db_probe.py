"""
Script de diagnóstico para intentar una conexión más robusta a MySQL
Muestra traceback completo y prueba con distintos parámetros.
"""
import os
import re
import sys
import traceback
import mysql.connector


def parse_mysql_url(url):
    m = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', url)
    if not m:
        raise ValueError('DATABASE_URL no válido. Formato esperado: mysql://user:pass@host:port/db')
    return dict(user=m.group(1), password=m.group(2), host=m.group(3), port=int(m.group(4)), database=m.group(5))


def try_connect(cfg, **kwargs):
    print('\nIntentando conectar con opciones:', kwargs)
    try:
        conn = mysql.connector.connect(**cfg, **kwargs)
        cur = conn.cursor()
        cur.execute('SELECT VERSION()')
        print('Versión MySQL:', cur.fetchone())
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print('Error al conectar:')
        traceback.print_exc()
        return False


def main():
    url = os.environ.get('DATABASE_URL') or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not url:
        print('Pasa la DATABASE_URL como variable de entorno o argumento')
        sys.exit(2)
    cfg = parse_mysql_url(url)
    # Intento simple
    ok = try_connect(cfg)
    if ok:
        return

    # Intentar con tiempo de espera mayor
    try_connect(cfg, connection_timeout=30)

    # Intentar con use_pure True
    try_connect(cfg, connection_timeout=30, use_pure=True)

    # Intentar deshabilitar SSL (si la librería lo soporta)
    try:
        try_connect(cfg, connection_timeout=30, ssl_disabled=True)
    except TypeError:
        print('ssl_disabled no soportado por esta versión del conector.')


if __name__ == '__main__':
    main()
