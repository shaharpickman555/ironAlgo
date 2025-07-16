# test_app.py
import numpy as np
from server import get_data
import time
from datetime import datetime

def test_get_data():
    date = datetime(2025, 7, 15)
    ts = np.float64(time.mktime(date.timetuple()))
    result = get_data("AAPL", ts)
    assert isinstance(result, np.float32)
    print("✅ test_get_data passed")

if __name__ == "__main__":
    test_get_data()
