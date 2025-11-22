"""
Script de prueba para conectar a la base de datos MySQL (Railway) y listar tablas y conteos.

Uso:
  - Establecer la variable de entorno `DATABASE_URL` con la cadena mysql://user:pass@host:port/db
  - O pasar la URL como primer argumento: `python db_test.py "mysql://..."`

El script intentará conectarse y ejecutar `SHOW TABLES` y `SELECT COUNT(*)` en cada tabla.
"""
import os
import re
import sys
import mysql.connector


def parse_mysql_url(url):
    m = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(\w+)', url)
    if not m:
        raise ValueError('DATABASE_URL no válido. Formato esperado: mysql://user:pass@host:port/db')
    return dict(user=m.group(1), password=m.group(2), host=m.group(3), port=int(m.group(4)), database=m.group(5))


def main():
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = os.environ.get('DATABASE_URL')

    if not url:
        print('Error: No se proporcionó DATABASE_URL. Pasa la URL como argumento o define la variable de entorno.')
        sys.exit(2)

    try:
        cfg = parse_mysql_url(url)
    except Exception as e:
        print('Error parseando la URL:', e)
        sys.exit(2)

    print('Conectando a', cfg['host'], 'base:', cfg['database'])
    try:
        conn = mysql.connector.connect(**cfg)
    except Exception as e:
        print('Error al conectar a la base de datos:')
        print(e)
        sys.exit(3)

    try:
        cur = conn.cursor()
        cur.execute('SHOW TABLES')
        tables = [row[0] for row in cur.fetchall()]
        if not tables:
            print('No hay tablas en la base de datos.')
        else:
            print('Tablas encontradas:', ', '.join(tables))
            for t in tables:
                try:
                    cur.execute(f'SELECT COUNT(*) FROM `{t}`')
                    cnt = cur.fetchone()[0]
                except Exception as e:
                    cnt = f'Error ({e})'
                print(f'  {t}: {cnt}')
        cur.close()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
