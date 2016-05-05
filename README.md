# plot2Dcluster

**plot2Dcluster.py** is a Python module that visualizes community detection results with the 
interaction between 2 nominal node attributes. 

In the raw data, the 2 attributes are arranged by rows and columns and the 
communities are denoted by non-negative integers. 

Every community will be assigned with a "distinct" enough color (using the 
HLS-to-RGB conversion). 

The rows and columns can be kept as original or rearranged by a majority
rule, which includes the following steps:

1. A ranking list of the frequencies of all the communities in the raw 
data is generated. 
2. The majority (most frequent) communities for each row (or column) are 
recorded.
3. The rows (or columns) with their majority community ranking highest 
in the list of step 1 will be rearranged first from the top (or from the 
left for columns). 
4. When there are multiple rows (or columns) with their majority
    community ranking the same in the list of step 1, the one will the 
	highest
    frequency will be rearranged first. 

This project is hosted at: [https://github.com/zhenzhu/plot2Dcluster](https://github.com/zhenzhu/plot2Dcluster).

MIT License

Copyright (c) 2016 Zhen Zhu

<hr>

**Table of Contents**
- [Usage](#usage)
	- [Context](#context)
	- [Download](#download)
	- [Input](#input)
	- [Functions](#functions)
- [Testing](#testing)
- [Reference](#reference)
- [Acknowledgements](#acknowledgements)

<hr>
**Packages Required:**
- [matplotlib](http://matplotlib.org/)
- [numpy](http://www.numpy.org/)

<br>

# Usage
[[back to top](#plot2dcluster)]

## Context
Sometimes it is useful to visualize the community detection result with 
the interaction between 2 nominal node attributes. 
For example, in our [paper](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0134025), each node of the network has 2 nominal
attributes, country and industry. 

A typical visualization is based on a community array with the 2 attributes
arranged as rows and columns. And each element of the array represents a
node in the network and contains a
non-negative integer indicating the community which the node
belongs to. 

You may want to visualize the result using a pre-defined arrangement of
rows and columns (e.g. arranging countries by alphabetical order and 
industry codes by numerical order). But more likely, you want to highlight
the largest communities detected (e.g. clustering the rows involving the
largest communities on the top). 

**plot2Dcluster** provides such a functionality to visualize the community
array either using a pre-defined arrangement or using a majority rule to
highlight the most significant communities. 

## Download
The easiest way is to download the script **plot2Dcluster.py** directly:

1. Go to the raw version of [plot2Dcluster.py](https://raw.githubusercontent.com/zhenzhu/plot2Dcluster/master/plot2Dcluster.py).
2. Right click and save it. 

## Input

**plot2Dcluster.py** only works with 2-dimension arrays.

The user-supplied lists of row names and column names of the community
array (i.e. the 2 nominal node attributes) are also needed.

Finally, the communities (i.e. the elements of the array) need to be
denoted as non-negative integers. 


## Functions

3 functions are available:

1. `plot_com_original` returns a plot of the community array as it is. The parameters
    include:
    * `com_data`: A 2-dimension community array. 
    * `rownames`: A list of strings corresponding to the row names of `com_data`.
    * `colnames`: A list of strings corresponding to the column names of `com_data`.

2. `plot_com_order1` returns a plot of the community array and applies the majority
    rule to rearrange **either** rows **or** columns. The parameters include:
    * `com_data`: A 2-dimension community array.
    * `rownames`: A list of strings corresponding to the row names of `com_data`.
    * `colnames`: A list of strings corresponding to the column names of `com_data`.
    * `row`: A logical value. If true, rows will be rearranged according to
    the majority rule and columns will be fixed. Otherwise, columns will
    be rearranged and rows will be fixed. 

3. `plot_com_order2` returns a plot of the community array and applies the majority
    rule to rearrange **both** rows **and** columns. The parameters include:
    * `com_data`: A 2-dimension community array.
    * `rownames`: A list of strings corresponding to the row names of `com_data`.
    * `colnames`: A list of strings corresponding to the column names of `com_data`.


<br>

# Testing
[[back to top](#plot2dcluster)]


```python
import random as rd
import numpy as np
import plot2Dcluster as p2c

# Define a function to generate an example community array.
def example_com(n_row,n_col,n_com):
    """
    This function returns a 2-dimension array as an example of community detection
    result. The parameters include:
    n_row: The number of instances of the first node attribute.
    n_col: The number of instances of the second node attribute.
    n_com: The number of communities detected.
    """
    top2 = rd.sample(range(n_com),2) # There will be 2 dominating communities detected.
    
    # The first half of the data.
    prob1 = [(1-0.6)/(n_com-2)]*n_com # All the other communities are assigned with the same probability.
    prob1[top2[0]] = 0.45
    prob1[top2[1]] = 0.15
    data1 = np.random.choice(n_com,(n_row*n_col)/2,p=prob1)
    
    # The second half of the data.
    prob2 = [(1-0.9)/(n_com-2)]*n_com # All the other communities are assigned with the same probability.
    prob2[top2[0]] = 0.7
    prob2[top2[1]] = 0.2
    data2 = np.random.choice(n_com,(n_row*n_col)/2,p=prob2)
    
    # Combine the two halves.
    data = np.concatenate((data1,data2))
    
    # The example will look more "diverse" on the top and more "uniform" on the bottom.
    com_data = data.reshape(n_row,n_col)
    return com_data

# Generate an example community array with 40 rows, 26 columns, and 30 communities.
rd.seed(3)
np.random.seed(3)
example = example_com(40,26,30)

# Generate an example list of column names A-Z.
colnames = []
for i in range(ord('A'),ord('Z')+1):
    colnames.append(chr(i))

# Generate an example list of row names 1-40.
rownames = [str(i) for i in range(1,41)]

# Test 1
rd.seed(3)
p2c.plot_com_original(example,rownames,colnames)

# Test 2
rd.seed(3)
p2c.plot_com_order1(example,rownames,colnames,row=True)

# Test 3
rd.seed(3)
p2c.plot_com_order1(example,rownames,colnames,row=False)

# Test 4
rd.seed(3)
p2c.plot_com_order2(example,rownames,colnames)
```

The code is working properly if the figures [original](https://github.com/zhenzhu/plot2Dcluster/blob/master/examples/original.png), 
[order1_row](https://github.com/zhenzhu/plot2Dcluster/blob/master/examples/order1_row.png), 
[order1_col](https://github.com/zhenzhu/plot2Dcluster/blob/master/examples/order1_col.png), 
and [order2](https://github.com/zhenzhu/plot2Dcluster/blob/master/examples/order2.png) are generated by Tests 1-4 respectively.


<br>

# Reference
[[back to top](#plot2dcluster)]

If using the code, please cite the publication below:

Cerina F, Zhu Z, Chessa A, Riccaboni M (2015)
[World Input-Output Network](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0134025). 
PLoS ONE 10(7): e0134025. doi:10.1371/journal.pone.0134025

# Acknowledgements
[[back to top](#plot2dcluster)]

The code is inspired by the figures produced by Federica Cerina in [World Input-Output Network](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0134025).
