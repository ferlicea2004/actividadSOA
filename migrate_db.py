"""
Script simple para ejecutar el archivo `db_schema.sql` contra la base de datos MySQL.

Uso:
  - Asegúrate de que `db_schema.sql` esté en el mismo directorio (`c:\Users\filib\Documents\Actividad\db_schema.sql`).
  - Establece `DATABASE_URL` o pásala como primer argumento.
  - Ejecuta: `python migrate_db.py` (esto aplicará las sentencias SQL en el archivo).

Precaución: Este script ejecuta SQL directamente; revisa `db_schema.sql` antes de correr.
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

    schema_file = os.path.join(os.path.dirname(__file__), 'db_schema.sql')
    if not os.path.exists(schema_file):
        print('Error: no se encontró', schema_file)
        sys.exit(2)

    with open(schema_file, 'r', encoding='utf-8') as f:
        sql = f.read()

    # dividir por ';' básico (asume que el archivo está en formato simple)
    statements = [s.strip() for s in sql.split(';') if s.strip()]

    print('Conectando a', cfg['host'], 'base:', cfg['database'])
    try:
        conn = mysql.connector.connect(**cfg)
        cur = conn.cursor()
        for stmt in statements:
            print('Ejecutando sentencia...')
            cur.execute(stmt)
        conn.commit()
        cur.close()
        print('Migración completada.')
    except Exception as e:
        print('Error ejecutando migración:', e)
        sys.exit(3)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    main()
