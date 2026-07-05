"""
Limpieza de datos de pedidos - Bluerdress
------------------------------------------
Este script toma el registro "crudo" de pedidos de mi marca (Bluerdress)
y lo deja listo para análisis: sin duplicados, con formatos consistentes
y sin valores faltantes sin resolver.

Autora: Hitomi Carrasco
"""

import pandas as pd

# 1. Cargar los datos originales
df = pd.read_csv("bluerdress_orders_raw.csv")

print("--- ANTES DE LIMPIAR ---")
print(f"Filas totales: {len(df)}")
print(f"Valores nulos por columna:\n{df.isnull().sum()}\n")

# 2. Quitar espacios en blanco de texto (ej. " Ana Torres " -> "Ana Torres")
text_cols = ["customer_name", "city", "product", "status"]
for col in text_cols:
    df[col] = df[col].str.strip()

# 3. Estandarizar mayúsculas/minúsculas
# Nombres y ciudades en formato "Título", el estado en minúsculas
df["customer_name"] = df["customer_name"].str.title()
df["city"] = df["city"].str.title()
df["status"] = df["status"].str.lower()

# 4. Unificar la columna de estado (traducir "delivered" -> "entregado" si apareciera,
# y asegurar que valores como "entregado"/"ENTREGADO"/"Entregado" queden iguales)
df["status"] = df["status"].replace({"delivered": "entregado"})

# 5. Limpiar la columna de precio: quitar "S/" y comas, convertir a número
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("S/", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 6. Convertir fechas con formatos mixtos (YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY) a un solo formato
# Probamos cada formato conocido de forma explícita, en vez de dejar que pandas
# adivine (adivinar puede confundir día/mes y dañar los datos silenciosamente).
def parse_mixed_date(value):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return pd.to_datetime(value, format=fmt)
        except ValueError:
            continue
    return pd.NaT


df["order_date"] = df["order_date"].apply(parse_mixed_date)

# 7. Rellenar cantidades faltantes con 1 (asumiendo pedido mínimo de 1 unidad)
df["quantity"] = df["quantity"].fillna(1).astype(int)

# 8. Rellenar precio faltante usando el precio promedio de ese mismo producto
df["price"] = df.groupby("product")["price"].transform(lambda x: x.fillna(x.mean()))

# 9. Rellenar ciudad faltante como "No especificado" (no hay forma de adivinarla)
df["city"] = df["city"].fillna("No especificado")

# 10. Eliminar pedidos duplicados
# a) Mismo order_id no debería repetirse nunca
df = df.drop_duplicates(subset="order_id", keep="first")
# b) A veces el mismo pedido se registra dos veces con un order_id distinto
#    (error humano al tipear). Lo detectamos por cliente+fecha+producto+cantidad.
df = df.drop_duplicates(
    subset=["customer_name", "order_date", "product", "quantity"], keep="first"
)

# 11. Calcular el total del pedido (nueva columna útil para análisis)
df["total"] = df["quantity"] * df["price"]

print("--- DESPUÉS DE LIMPIAR ---")
print(f"Filas totales: {len(df)}")
print(f"Valores nulos por columna:\n{df.isnull().sum()}\n")

# 12. Guardar el archivo limpio
df.to_csv("bluerdress_orders_clean.csv", index=False)
print("Archivo limpio guardado como bluerdress_orders_clean.csv")
