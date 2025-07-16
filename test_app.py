# test_app.py
import numpy as np
from server import get_data

def test_get_data():
    ts = np.float64(1720828800)  # 2025-07-13
    result = get_data("AAPL", ts)
    assert isinstance(result, np.float32)
    print("✅ test_get_data passed")

if __name__ == "__main__":
    test_get_data()
