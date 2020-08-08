#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to move through the database and count the numbe of unique variations


Improvements and Notes:
-------------------------
1. probably shouldn't count | and . as unique values, need to address this. 
   Need to confirm if these are counted as unique values. '.'  is likely a unique vlaue
   if it appears in a location previously filled: 
   AGA
   A.A
   A.A
   AGA
   The above is 1 unique variation due to the 'gap'. Should this gap be considered unique? 

2. This assumes that 
    ACA
    ACG
    ACA
    where G is different is one variation. 

"""

import pandas as pd
import numpy as np 
import io
import copy

'''
------------------------------------------------------------
Name: Fill in the letters
Input: data frame

------------------------------------------------------------
'''
def fill_in_the_letters(df):
    # make the values in each cell into lists ex: [A, T, G, G, C, C, G, T, C] 
    df_lists = df.applymap(lambda y: list(y))
    
    # make the df into a multiindex
    split_columns = {} # create an empty dictionary that will hold 
    
    # read throught the list df_lists and place into dict 
    for col in df_lists.columns:
        split_columns[col] = df_lists[col].apply(pd.Series) # Series is 1D pandas 'array'capable of any datatype
    
    # split into single element columns 
    multiindexed_df = pd.concat(split_columns.values(), axis = 1, keys = split_columns.keys())
    
    # rename the columns to the first row
    numbered_columns = multiindexed_df.columns
    first_row = list(multiindexed_df.iloc[0])
    columns = pd.MultiIndex.from_tuples(
        [(c[0][0],str(c[0][1]) + "-" + c[1]) for c in zip(numbered_columns, first_row)]
    )
    
    # deep copy constructs a new compound object then, 
    # recursively, inserts copies into it of the objects found in the original (multiindexed_df).
    multiindexed_df_new_col_names = copy.deepcopy(multiindexed_df) 
    
    # set columns to the mulitiindexed columns
    multiindexed_df_new_col_names.columns = columns
    
    # get the dict of how this will be replaced
    replace_with = {x: x[1].split("-")[1] for x in columns}
    
    # now run fillna on the '-'
    return multiindexed_df_new_col_names.replace("-",np.NaN).fillna(replace_with)

'''
------------------------------------------------------------
------------------------------------------------------------
Main Function 
------------------------------------------------------------
------------------------------------------------------------
'''
def main():

    #Read in the file into a list of pandas dataframes  
    with open('/Users/drjacobs/Desktop/Data/A_gen.txt') as F:
        Lines = F.readlines()[9:] # read all lines in file 
        df_lines = []
        dfs = []
        for line in Lines:
            stripped_line = line.strip()
            if len(stripped_line) > 0 and stripped_line[0] == 'A':
                df_lines.append(line.strip())
            else:
                if len(df_lines) > 0:
                    dfs.append(pd.read_csv(io.StringIO('\n'.join(df_lines)),sep='\s+',header=None).set_index(0))
                    df_lines = [] 
   
    total=0

    #inumerate through the list of dataframes and apply the function fill_in_letters
    for index, df_el in enumerate(dfs):
       # print(f"current index: {index}")
        dfs[index] = fill_in_the_letters(df_el)
    '''
    # version with unknown * values 
    # count the unique values 
    for i, element in enumerate(dfs):
        count=(element.nunique()).sum() #this was currently working
        #col_count_df = pd.DataFrame(df_el.nunique() - 1).unstack().sum(1)
        total+=count
        print(f"count for chunk {i} is {count}")
    '''
    # version withouth counting the unkown values as unique 
    # count the unique values 
    for i, element in enumerate(dfs):
        element = element.replace('*',np.NaN)
        count = (element.nunique(dropna=True)).sum() # this was currently working
        element = element.fillna('*')
       # col_count_df = pd.DataFrame(df_el.nunique() - 1).unstack().sum(1)
        total+=count
        print(f"count for number of columns with unuque values in dataframe {i} is {count}")
    
    print(f"Total variations: {total}")
    

if __name__ == "__main__":
    main()
