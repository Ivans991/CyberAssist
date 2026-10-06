import sqlite3

con = sqlite3.connect("cyberassist.db")
cursor = con.cursor()

activos = cursor.execute("SELECT id, codigo FROM activos").fetchall()

for activo_id, codigo in activos:
    codigo_normalizado = codigo.strip().upper()

    if codigo_normalizado == codigo:
        continue

    ya_existe = cursor.execute(
        "SELECT id FROM activos WHERE codigo = ? AND id != ?",
        (codigo_normalizado, activo_id)
    ).fetchone()

    if ya_existe:
        print(f"CONFLICTO: id={activo_id} código '{codigo}' -> '{codigo_normalizado}' "
              f"ya está en uso por id={ya_existe[0]}. NO se modificó, requiere renombrar manualmente.")
        continue

    cursor.execute(
        "UPDATE activos SET codigo = ? WHERE id = ?",
        (codigo_normalizado, activo_id)
    )
    print(f"Normalizado: id={activo_id} '{codigo}' -> '{codigo_normalizado}'")

con.commit()
con.close()