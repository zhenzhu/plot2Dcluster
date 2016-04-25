"""
Please cite our publication below if using the code:
    Cerina F, Zhu Z, Chessa A, Riccaboni M (2015) 
    World Input-Output Network. PLoS ONE 10(7): e0134025. 
    doi:10.1371/journal.pone.0134025

This Python module visualizes community detection results with the 
interaction between 2 nominal node attributes. 

In the raw data, the 2 attributes are arranged by rows and columns and the 
communities are denoted by positive integers. 

Every community will be assigned with a "distinct" enough color (using the 
HLS-to-RGB conversion). 

The rows and columns can be kept as original or rearranged by a majority
rule, which includes the following steps:
    1) A ranking list of the frequencies of all the communities in the raw
    data is generated. 
    2) The majority (most frequent) communities for each row (or column) 
    are recorded.
    3) The rows (or columns) with their majority community ranking highest
    in the list of 1) will be rearranged first from the top (or from the
    left for columns). 
    4) When there are multiple rows (or columns) with their majority
    community ranking the same in the list of 1), the one will the highest
    frequency will be rearranged first. 

MIT License
Copyright (c) 2016 Zhen Zhu 
"""

import matplotlib.pyplot as plt
from matplotlib import colors
import random as rd
import numpy as np
import colorsys as cs
import operator


def plot_com_original(com_data,rownames,colnames):
    """
    This function returns a plot of the community array as it is. The parameters
    include:
    com_data: A 2-dimension community array. 
    rownames: A list of strings corresponding to the row names of com_data.
    colnames: A list of strings corresponding to the column names of com_data.
    """
    # Get the basic info of the community array.
    com_data = com_data.astype(int) # Make sure that the communities are denoted as integers.
    n_row = np.shape(com_data)[0] # Number of rows.
    n_col = np.shape(com_data)[1] # Number of columns.
    data = com_data.reshape(com_data.size) # Convert to 1-dimension array.
    all_count = np.bincount(data) # Count frequency of each community.
    all_order = np.argsort(all_count)[::-1] # Generate the ranking list of communities by frequency.
    n_com = len(all_order) # n_com is equal to the largest integer in com_data plus 1.
    
    # Generate n_com "distinct" enough colors.
    HLS_color = []
    i = 0
    step = 0.9/n_com
    init = step
    while i < n_com:
        temp_hue = init
        temp_lig = rd.random()
        temp_sat = rd.random()
        HLS_color.append((temp_hue,temp_lig,temp_sat))
        i += 1
        init += step
    RGB_color = [cs.hls_to_rgb(a,b,c) for (a,b,c) in HLS_color]
    
    # Prepare the discrete colormap for each integer/community.
    cmap = colors.ListedColormap(RGB_color)
    bounds = [i-0.5 for i in range(n_com+1)]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    # Prepare the plot.
    fig, ax = plt.subplots(figsize=(16,16))
    xticks = np.arange(0,n_col,1)
    yticks = np.arange(0,n_row,1)
    ax.imshow(com_data, cmap=cmap, norm=norm, interpolation='nearest')
    ax.xaxis.tick_top() # This will make x labels on top.
    plt.xticks(xticks)
    plt.yticks(yticks)
    ax.set_xticklabels(colnames)
    ax.set_yticklabels(rownames)
    
    plt.savefig('original.png')


def plot_com_order1(com_data,rownames,colnames,row=True):
    """
    This function returns a plot of the community array and applies the majority
    rule to rearrange either rows or columns. The parameters include:
    com_data: A 2-dimension community array.
    rownames: A list of strings corresponding to the row names of com_data.
    colnames: A list of strings corresponding to the column names of com_data.
    row: A logical value. If true, rows will be rearranged according to
    the majority rule and columns will be fixed. Otherwise, columns will
    be rearranged and rows will be fixed.
    """
    # Get the basic info of the community array.
    com_data = com_data.astype(int) # Make sure that the communities are denoted as integers.
    n_row = np.shape(com_data)[0] # Number of rows.
    n_col = np.shape(com_data)[1] # Number of columns.
    data = com_data.reshape(com_data.size) # Convert to 1-dimension array.
    all_count = np.bincount(data) # Count frequency of each community.
    all_order = np.argsort(all_count)[::-1] # Generate the ranking list of communities by frequency.
    n_com = len(all_order) # n_com is equal to the largest integer in com_data plus 1.
    
    # Apply the majority rule depending on the logical value of row.
    majority = {}
    for i in range(n_com):
        majority[i] = {}
    
    if (row==True): # When rows are to be rearranged.
        # For each row, the most frequent communities are stored.
        for i in range(n_row):
            myrow = com_data[i,:]
            rowcount = np.bincount(myrow)
            rowmax = max(rowcount)
            for (j,k) in enumerate(rowcount):
                if k==rowmax:
                    majority[j][i] = k
        
        unreach = set(range(n_row))
        row_order = [] # The list of new order of the rows.
        
        for i in range(len(all_order)):
            if len(majority[i])>0:
                temp1 = majority[i]
                temp2 = sorted(temp1.items(), key=operator.itemgetter(1), reverse=True)
                for (m,n) in temp2:
                    if (m in unreach):
                        row_order.append(m)
                        unreach.remove(m)
                
        new_data = com_data[row_order,:] # The rearranged data.    
    
    else: # When columns are to be rearranged.
        # For each column, the most frequent communities are stored.
        for i in range(n_col):
            mycol = com_data[:,i]
            colcount = np.bincount(mycol)
            colmax = max(colcount)
            for (j,k) in enumerate(colcount):
                if k==colmax:
                    majority[j][i] = k
        
        unreach = set(range(n_col))
        col_order = [] # The list of new order of the columns.
        
        for i in range(len(all_order)):
            if len(majority[i])>0:
                temp1 = majority[i]
                temp2 = sorted(temp1.items(), key=operator.itemgetter(1), reverse=True)
                for (m,n) in temp2:
                    if (m in unreach):
                        col_order.append(m)
                        unreach.remove(m)
                
        new_data = com_data[:,col_order] # The rearranged data.  
    
    # Generate n_com "distinct" enough colors.
    HLS_color = []
    i = 0
    step = 0.9/n_com
    init = step
    while i < n_com:
        temp_hue = init
        temp_lig = rd.random()
        temp_sat = rd.random()
        HLS_color.append((temp_hue,temp_lig,temp_sat))
        i += 1
        init += step
    RGB_color = [cs.hls_to_rgb(a,b,c) for (a,b,c) in HLS_color]
    
    # Prepare the discrete colormap for each integer/community.
    cmap = colors.ListedColormap(RGB_color)
    bounds = [i-0.5 for i in range(n_com+1)]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    # Reorder the row names or the column names depending on the logical value of row.
    if (row==True):
        rownames = [rownames[i] for i in row_order]
    else:
        colnames = [colnames[i] for i in col_order]
    
    # Prepare the plot.
    fig, ax = plt.subplots(figsize=(16,16))
    xticks = np.arange(0,n_col,1)
    yticks = np.arange(0,n_row,1)
    ax.imshow(new_data, cmap=cmap, norm=norm, interpolation='nearest')
    ax.xaxis.tick_top() # This will make x labels on top.
    plt.xticks(xticks)
    plt.yticks(yticks)
    ax.set_xticklabels(colnames)
    ax.set_yticklabels(rownames)
    
    plt.savefig('order1.png')


def plot_com_order2(com_data,rownames,colnames):
    """
    This function returns a plot of the community array and applies the majority
    rule to rearrange both rows and columns. The parameters include:
    com_data: A 2-dimension community array.
    rownames: A list of strings corresponding to the row names of com_data.
    colnames: A list of strings corresponding to the column names of com_data.
    """
    # Get the basic info of the community array.
    com_data = com_data.astype(int) # Make sure that the communities are denoted as integers.
    n_row = np.shape(com_data)[0] # Number of rows.
    n_col = np.shape(com_data)[1] # Number of columns.
    data = com_data.reshape(com_data.size) # Convert to 1-dimension array.
    all_count = np.bincount(data) # Count frequency of each community.
    all_order = np.argsort(all_count)[::-1] # Generate the ranking list of communities by frequency.
    n_com = len(all_order) # n_com is equal to the largest integer in com_data plus 1.
    
    # First apply the majority rule to the rows.
    majority_row = {}
    for i in range(n_com):
        majority_row[i] = {}
    
    # For each row, the most frequent communities are stored.
    for i in range(n_row):
        myrow = com_data[i,:]
        rowcount = np.bincount(myrow)
        rowmax = max(rowcount)
        for (j,k) in enumerate(rowcount):
            if k==rowmax:
                majority_row[j][i] = k
        
    unreach = set(range(n_row))
    row_order = [] # The list of new order of the rows.
        
    for i in range(len(all_order)):
        if len(majority_row[i])>0:
            temp1 = majority_row[i]
            temp2 = sorted(temp1.items(), key=operator.itemgetter(1), reverse=True)
            for (m,n) in temp2:
                if (m in unreach):
                    row_order.append(m)
                    unreach.remove(m)
                
    new_data = com_data[row_order,:] # The row-rearranged data.    
    
    # Then apply the majority rule to the columns.
    majority_col = {}
    for i in range(n_com):
        majority_col[i] = {}

    # For each column, the most frequent communities are stored.
    for i in range(n_col):
        mycol = com_data[:,i]
        colcount = np.bincount(mycol)
        colmax = max(colcount)
        for (j,k) in enumerate(colcount):
            if k==colmax:
                majority_col[j][i] = k
        
    unreach = set(range(n_col))
    col_order = [] # The list of new order of the columns.
        
    for i in range(len(all_order)):
        if len(majority_col[i])>0:
            temp1 = majority_col[i]
            temp2 = sorted(temp1.items(), key=operator.itemgetter(1), reverse=True)
            for (m,n) in temp2:
                if (m in unreach):
                    col_order.append(m)
                    unreach.remove(m)
                
    new_data2 = new_data[:,col_order] # The row-and-column-rearranged data.  
    
    # Generate n_com "distinct" enough colors.
    HLS_color = []
    i = 0
    step = 0.9/n_com
    init = step
    while i < n_com:
        temp_hue = init
        temp_lig = rd.random()
        temp_sat = rd.random()
        HLS_color.append((temp_hue,temp_lig,temp_sat))
        i += 1
        init += step
    RGB_color = [cs.hls_to_rgb(a,b,c) for (a,b,c) in HLS_color]
    
    # Prepare the discrete colormap for each integer/community.
    cmap = colors.ListedColormap(RGB_color)
    bounds = [i-0.5 for i in range(n_com+1)]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    # Reorder the row names and the column names.
    rownames = [rownames[i] for i in row_order]
    colnames = [colnames[i] for i in col_order]
    
    # Prepare the plot.
    fig, ax = plt.subplots(figsize=(16,16))
    xticks = np.arange(0,n_col,1)
    yticks = np.arange(0,n_row,1)
    ax.imshow(new_data2, cmap=cmap, norm=norm, interpolation='nearest')
    ax.xaxis.tick_top() # This will make x labels on top.
    plt.xticks(xticks)
    plt.yticks(yticks)
    ax.set_xticklabels(colnames)
    ax.set_yticklabels(rownames)
    
    plt.savefig('order2.png')

