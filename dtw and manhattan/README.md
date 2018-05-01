# cycle generation

## usage
+ make sure you have a dir for `results`
+ prepare you data like `cycle_detection/test_data.csv`
+ update `ROOT`, `RESULTS_DIR`, `DATA_SET_DIR`, the last two are relative paths
+ override `get_data(self, file_path)` to get timestamps and data
+ override `show(...)` to show or save the pics as you want
+ update `sample_rate` and `subset_size` at the bottom
+ run


# similarity score

## usage

+ make seq0 as train set and seq1 as test set
+ calculate the similarity score and record
+ run python score.py filename e.g. python score.py T0_ID130007_Center_seq1


# plot the ROC curve

## usage

+ make Sure you have run the code above and similarity score must stored in the target file
+ run python accuracy.py



