def normalize(data, min_val=0, max_val=1):

    # step 1: normalize between 0 and 1
    data_nomred = data - data.min()
    data_normed = data_nomred / data_nomred.max()

    data_normed = data_normed * (max_val - min_val) + min_val
    return data_normed