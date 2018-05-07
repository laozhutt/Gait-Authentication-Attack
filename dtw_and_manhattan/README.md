# cycle generation

## usage
+ update `ROOT` at top of `generations.py`
+ in `__main__`, set up your result dir to save pics and splitted data
+ prepare your data like `cycle_detection/test_data`
+ prepare your dataset as below
```
dataset_name
©À©¤©¤ user_name1
    ©À©¤©¤ file_name1
    ©À©¤©¤ file_name2
    ...
©À©¤©¤ user_name2
...
``` 
+ override `get_data(self, file_path)` to get timestamps and data
+ update `sample_rate` and `subset_size` at the bottom, `subset_size` is approx 80% of sample_rate
+ not change the `smoothing factor`
+ write your own `show_xxx(...)` in `tools.py` to show or save the pics as you want, we've already provide you some
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



