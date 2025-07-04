import pandas as pd

# ──────────────────────── 유틸 ↓ ────────────────────────
def add_moving_average(
    df: pd.DataFrame,
    value_col: str,
    window: int,
    method: str = "sma",
    center: bool = False,
) -> pd.Series:
    if method == "sma":
        return (df[value_col]
                .rolling(window=window, min_periods=1, center=center)
                .mean())
    if method == "ema":
        alpha = 2 / (window + 1)
        return df[value_col].ewm(alpha=alpha, adjust=False).mean()
    raise ValueError("method must be 'sma' or 'ema'")