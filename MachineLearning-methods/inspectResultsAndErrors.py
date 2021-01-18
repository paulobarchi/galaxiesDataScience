import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])
print 'Total = ' + str(len(df))

und = df[(df['class'] == 'U')]
print 'und = '+ str(len(und))

errors = [1, 2, 3, 4, 5, 6, 7]

for error in errors:
	temp = df[(df['Error'] == error)]
	print 'Error' + str(error) + ' = ' + str(len(temp))

metrics = ['G2', 'H', 'C', 'A', 'S']

for metric in metrics:
	temp = df[(df[metric] == 9999.99)]
	print 'problem with ' + metric + ' = ' + str(len(temp))

newM = df[(df['C'] == 9999.99)]
newM = newM[(newM['G2'] != 9999.99)]
newM = newM[(newM['H'] != 9999.99)]
newM = newM[(newM['A'] != 9999.99)]
newM = newM[(newM['S'] != 9999.99)]
print 'problem exclusively with C = ' + str(len(newM))