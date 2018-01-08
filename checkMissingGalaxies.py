import pandas as pd
import sys
import numpy

# read arguments
input_data  = pd.read_csv(sys.argv[1])
print 'len(input)  = ',len(input_data)
output_data = pd.read_csv(sys.argv[2])
print 'len(output) = ',len(output_data)
print 'numerical diff = ',int(len(input_data)-len(output_data))

# get missing galaxies data
missing = input_data[input_data['dr7objid'].isin(output_data['Id']) == False]
print 'len(missing) = ',len(missing)
# generate file with missing galaxies data
missing.to_csv(sys.argv[3], index=False)