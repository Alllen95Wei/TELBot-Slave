__all__ = ["clamp"]


def clamp(val: float, min_val: float = -1.0, max_val: float = 1.0) -> float:
    """
    Clamps a numeric value between min_val and max_val.
    Defaults to [-1.0, 1.0] for standard normalized motor speeds.
    """
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    return val

