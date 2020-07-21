from hashlib import md5
import math
import time
import os
from pathlib import Path

import numpy as np

from saleae.range_measurements import AnalogMeasurer

class AnalogExport(AnalogMeasurer):
    supported_measurements = ["exp_hint", "exp_status"]

    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.batches = []
        self.skip = not (set(requested_measurements) & set(self.supported_measurements))

    def process_data(self, data):
        if self.skip:
            return

        self.batches.append(data.samples)

    def measure(self):
        if self.skip:
            return {
                "exp_hint": 0,
                "exp_status": -1,
            }
        try:
            total_data = np.concatenate(self.batches)
            data_hash = md5(total_data).hexdigest()
            measurement_taken = int(time.time())
            base_dir = Path.home() / "SaleaeAnalogExport"

            # Avoid re-calculating all the time. If the hash exists, return now.
            hash_dir = base_dir / "hashes"
            hash_dir.mkdir(parents=True, exist_ok=True)
            if (hash_dir / data_hash).is_file():
                return {
                    "exp_hint": measurement_taken,
                    "exp_status": -2,
                }
            else:
                with open(str(hash_dir / data_hash), "w") as hash_file:
                    pass

            # Store
            storage_dir = base_dir / "data"
            storage_dir.mkdir(parents=True, exist_ok=True)
            filename = str(storage_dir / "{}.txt.gz".format(measurement_taken))
            np.savetxt(filename, total_data)
            return {
                "exp_hint": measurement_taken,
                "exp_status": 0,
            }
        except (OSError):
            return {
                "exp_hint": 0,
                "exp_status": 1,
            }
        except (AttributeError, TypeError, IndexError, KeyError, NameError, RuntimeError, ValueError):
            return {
                "exp_hint": 0,
                "exp_status": 2,
            }
