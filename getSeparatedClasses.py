import pandas as pd
import sys

result = pd.read_csv(sys.argv[1])
classCol = sys.argv[2]
print 'len(result) = ',len(result)

resultE = result[(result[classCol] == 'E')]
print 'len(resultE) = ',len(resultE)
# resultE = resultE.head(n=1000)
resultE.to_csv(sys.argv[3], index=False)

resultS = result[(result[classCol] == 'S')]
print 'len(resultS) = ',len(resultS)
# resultS = resultS.head(n=1000)
resultS.to_csv(sys.argv[4], index=False)
