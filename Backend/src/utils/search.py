from sqlalchemy import func



def buscar_por_nombre_uno(db, modelo, campo, texto):
    texto = texto.strip().lower()
    if texto == "":
        return None
    palabras = texto.split()

    query = db.query(modelo)
    for palabra in palabras:
        query = query.filter(func.lower(campo).ilike(f"%{palabra}%"))

    return query.first()

def buscar_por_nombre_lista(db, modelo, campo, texto, limite=10):
    texto = texto.strip().lower()
    if texto == "":
        return []
    palabras = texto.split()

    query = db.query(modelo)
    for palabra in palabras:
        query = query.filter(func.lower(campo).ilike(f"%{palabra}%"))

    return query.limit(limite).all()
