# data/

The dataset is NOT stored in this zip (CSV 6.9 GB, binary 378 MB).

Source files (NYC Yellow Taxi trip records), placed in `data/archive/`:

| File | Rows kept |
| --- | --- |
| yellow_tripdata_2015-01.csv | 12,748,927 |
| yellow_tripdata_2016-01.csv | 10,906,847 |
| yellow_tripdata_2016-02.csv | 11,382,020 |
| yellow_tripdata_2016-03.csv | 12,210,929 |
| **Total** | **47,248,723** (122 invalid rows removed from 47,248,845) |

`python3 scripts/prepare_data.py` extracts the `trip_distance` column into
`data/trip_distance_all.bin`: 47,248,723 little-endian 8-byte doubles (377,989,784 bytes = 378.0 MB).
Full cleaning log: `results/prepare_data_output.txt`.
