import pandas as pd
from pandas.core.frame import DataFrame

def initial_set(datafram: DataFrame, coloumn_name):
    info = [str(datafram[coloumn_name][i]) for i in range(len(datafram[coloumn_name]))]
    return info

def initial_parameter_1(dataframe:DataFrame, index, coloumn1):
    return {str(dataframe[index][i]):dataframe[coloumn1][i] for i in range(len(dataframe[index]))}

def initial_parameter_2(dataframe:DataFrame, index1, index2):
    return {(str(dataframe[index1][i]), str(dataframe[index2][i])):1 for i in range(len(dataframe[index1]))}
