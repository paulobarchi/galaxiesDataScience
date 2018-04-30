import pandas as pd
import sys

# read input
zoo = pd.read_csv(sys.argv[1])

print len(zoo)

print len(zoo[(zoo['z'] >= 0.03) & (zoo['z'] <= 0.1)])