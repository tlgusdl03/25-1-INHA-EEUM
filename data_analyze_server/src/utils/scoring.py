from typing import Dict

# ────────────────────── CAI (통합대기환경지수) ──────────────────────
_CA_BREAKPOINTS: Dict[str, list[tuple[int, int]]] = {
    # (농도_LO, 농도_HI)  →  (지수_LO, 지수_HI)   # 환경부 고시(µg/m³)
    "pm10": [
        (0, 30,   0,  50),
        (31, 80, 51, 100),
        (81, 150,101, 250),
        (151, 600,251, 500),
    ],
    "pm2_5": [
        (0, 15,   0,  50),
        (16, 35, 51, 100),
        (36, 75,101, 250),
        (76, 500,251, 500),
    ],
    "tvoc": [
        (0, 200,   0,  50),
        (201, 500, 51, 100),
        (501, 1000,101, 250),
        (1001, 3000,251, 500),
    ],
}

# 농도를 통합대기지수(0‒500)로 변환
def _sub_index(pollutant: str, conc: float) -> int:
    conc = round(conc)
    for bp_lo, bp_hi, i_lo, i_hi in _CA_BREAKPOINTS[pollutant]:
        if bp_lo <= conc <= bp_hi:
            return round((i_hi - i_lo) / (bp_hi - bp_lo) * (conc - bp_lo) + i_lo)
    return 500  # 범위를 초과하면 최악으로

# PM10 통합 대기 지수 계산
def cai_score_pm10(pm10: float) -> float:
    score = _sub_index("pm10", pm10)
    score = 100 - 100 * (score / 500)
    return score

# PM2_5 통합 대기 지수 계산
def cai_score_pm2_5(pm2_5: float) -> float:
    score = _sub_index("pm2_5", pm2_5)
    score = 100 - 100 * (score / 500)
  
    return score

# TVOC 통합 대기 지수 계산
def cai_score_tvoc(tvoc: float) -> float:
    score = _sub_index("tvoc", tvoc)
    score = 100 - 100 * (score / 500)
    
    return score

# ────────────────────── 불쾌지수 (Discomfort Index) ──────────────────────
def discomfort_index(t:float, rh: float) -> float:
    # DI = 1.8*T - 0.55*(1-RH)*(1.8*T-26)+32   (°C, RH 0‒1)
    di = 1.8 * t - 0.55 * (1 - rh / 100) * (1.8 * t - 26) + 32
    score = 100 - 100 * ((di-68) / 18)
    if(score > 100):
        return 100
    if(score < 0):
        return 0
    return score