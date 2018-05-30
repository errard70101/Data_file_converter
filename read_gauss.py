# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:13:25 2018

@author: Shih-Yang Lin

This script convert Gauss ascii file to normal ascii file.
Since Gauss only allows 8 columns for its output data,
pandas can not correctly parse it.
"""
import numpy as np
import pandas as pd

#%%
def read_gauss_data(file_path, sep = ' '):
    '''
    Read Gauss data to a list.

    input:
        file_path: str.
        sep: str, the symbol to separate numbers.
    output:
        data: list.
    '''

    f = open(file_path)
    raw = f.read()

    data = list()
    item = ''
    for i in raw:
        if i != sep:
            item += i
        else:
            if (item != '') and (item != '\n'):
                data.append(float(item))
            item = ''

    return(data)

#%%

def build_data_matrix(file_path, n_rows, n_cols, sep = ' '):
    '''
    Build a n_rows x n_cols matrix from a list.

    input:
        file_path: str.
        sep: str, the symbol to separate numbers.
        n_rows: int.
        n_cols: int.
    output:
        mat = n_rows x n_cols numpy ndarray.
    '''
    data = read_gauss_data(file_path, sep)

    assert len(data) == n_rows * n_cols, 'The length of input data != n_rows * n_cols.'
    mat = np.array(data).reshape(n_rows, n_cols)

    return(mat)
