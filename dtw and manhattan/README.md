# cycle generation

## usage
+ make sure you have a dir for `results`
+ prepare you data like `cycle_detection/test_data.csv`
+ update `ROOT`, `RESULTS_DIR`, `DATA_SET_DIR`, the last two are relative paths
+ override `get_data(self, file_path)` to get timestamps and data
+ override `show(...)` to show or save the pics as you want
+ update `sample_rate` and `subset_size` at the bottom
+ run

