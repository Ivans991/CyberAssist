import sqlite3

con = sqlite3.connect("cyberassist.db")
resultado = con.execute(
    "SELECT DISTINCT criticidad FROM activos"
).fetchall()
print(resultado)
con.close()