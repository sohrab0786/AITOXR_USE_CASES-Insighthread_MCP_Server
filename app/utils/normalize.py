from typing import Optional, Union, List

def normalize_metrics(metrics: Optional[Union[str, List[str]]]) -> List[str]:
    if not metrics:
        return []
    if isinstance(metrics, str):
        return [m.strip() for m in metrics.split(",")]
    if isinstance(metrics, list):
        if len(metrics) == 1 and isinstance(metrics[0], str) and "," in metrics[0]:
            return [m.strip() for m in metrics[0].split(",")]
        return [m.strip() for m in metrics if isinstance(m, str)]
    return []
