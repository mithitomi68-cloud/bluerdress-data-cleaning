[README.md](https://github.com/user-attachments/files/29681378/README.md)
# Limpieza de datos de pedidos — Bluerdress

Proyecto de limpieza de datos usando **Python y Pandas**, aplicado a un registro real de pedidos de mi marca de ropa, [Bluerdress](.).

## El problema

El registro de pedidos (`bluerdress_orders_raw.csv`) tenía varios errores típicos de captura manual:

- Duplicados: el mismo pedido cargado dos veces con distinto ID.
- Textos inconsistentes: `"Lima"`, `"LIMA"`, `"lima "` referían a la misma ciudad.
- Fechas en tres formatos distintos (`2025-03-01`, `01/03/2025`, `05-03-2025`).
- Precios guardados como texto, algunos con el símbolo `S/` o comas.
- Valores faltantes en cantidad, precio y ciudad.
- Estados de pedido escritos de formas distintas (`Entregado`, `ENTREGADO`, `entregado`).

## Qué hice

El script `clean_data.py` recorre el dataset y:

1. Elimina espacios en blanco sobrantes en texto.
2. Estandariza mayúsculas/minúsculas en nombres, ciudades y estados.
3. Convierte precios de texto a números, quitando símbolos y comas.
4. Normaliza las fechas a un único formato, probando cada formato conocido explícitamente (en vez de dejar que la librería "adivine", que puede confundir día y mes).
5. Rellena cantidades faltantes y precios faltantes (usando el precio promedio de ese mismo producto).
6. Elimina duplicados, incluyendo pedidos repetidos con un ID distinto por error de tipeo.
7. Calcula el total de cada pedido.

## Resultado

| | Antes | Después |
|---|---|---|
| Filas | 20 | 18 |
| Valores nulos | 7 | 0 |
| Duplicados | 2 | 0 |

## Tecnologías

- Python 3
- Pandas

## Cómo correrlo

```bash
pip install pandas
python clean_data.py
```

Esto genera `bluerdress_orders_clean.csv`, listo para análisis o para cargar en Excel/Power BI.

---
*Proyecto hecho por Hitomi Carrasco como parte de mi aprendizaje autodidacta en análisis de datos.*
