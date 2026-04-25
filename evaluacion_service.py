def clasificar_habilidad(explicacion: str) -> str:
    """
    Clasifica una pregunta en una de las tres habilidades DEMRE según su explicación.
    Heurística oficial: Localizar (25%) · Interpretar (50%) · Evaluar (25%).
    """
    exp = explicacion.upper()
    if "LOCALIZAR" in exp or "RASTREAR" in exp or "EXTRAER" in exp:
        return "Localizar"
    if "EVALUAR" in exp or "REFLEXIONAR" in exp or "PROPÓSITO" in exp:
        return "Evaluar"
    return "Interpretar"  # Valor por defecto — mayor peso estadístico en el DEMRE


def calcular_estadisticas_habilidades(historial_alumno: list) -> dict:
    """
    Calcula aciertos y totales por habilidad DEMRE a partir del historial del alumno.
    Devuelve un dict con claves 'Localizar', 'Interpretar', 'Evaluar'.
    """
    stats = {
        "Localizar":   {"acierto": 0, "total": 0},
        "Interpretar": {"acierto": 0, "total": 0},
        "Evaluar":     {"acierto": 0, "total": 0},
    }
    for h in historial_alumno:
        pregs = h.get('preguntas_data', [])
        resps = h.get('respuestas_usuario', {})
        for p in pregs:
            pid = str(p.get('id', ''))
            hab = clasificar_habilidad(p.get('explicacion', ''))
            stats[hab]["total"] += 1

            r_user = resps.get(pid)
            correcta_data = p.get('correcta')
            if isinstance(correcta_data, int) and correcta_data < len(p.get('opciones', [])):
                r_correcta_str = p['opciones'][correcta_data]
                if r_user == correcta_data or r_user == r_correcta_str:
                    stats[hab]["acierto"] += 1
            elif isinstance(correcta_data, str):
                if r_user and r_user.startswith(correcta_data[0]):
                    stats[hab]["acierto"] += 1
    return stats


def evaluar_respuestas(preguntas: list, respuestas_usuario: dict) -> dict:
    """
    Cuenta respuestas correctas vs total para una lista de preguntas.
    Devuelve dict con claves 'correctas', 'total' y 'nota'.
    """
    correctas = 0
    total = len(preguntas)
    for p in preguntas:
        pid = p['id']
        r_user = respuestas_usuario.get(pid)
        r_correcta_idx = p.get('correcta', 0)
        if isinstance(r_correcta_idx, int) and r_correcta_idx < len(p['opciones']):
            if r_user == p['opciones'][r_correcta_idx]:
                correctas += 1
    return {
        'correctas': correctas,
        'total': total,
        'nota': calcular_nota(correctas, total),
    }


def calcular_nota(correctas: int, total: int) -> float:
    """
    Convierte puntaje bruto a nota en escala chilena (1.0 – 7.0).
    """
    if total == 0:
        return 1.0
    return round(((correctas / total) * 6.0) + 1.0, 1)
