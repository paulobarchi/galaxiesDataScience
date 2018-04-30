import pandas as pd
import sys
import numpy

result_60k = pd.read_csv(sys.argv[1])

# remove duplicatas
result_60k = result_60k.drop_duplicates(subset=['Id'], keep='first')
print('total = '+str(len(result_60k)))

# remove registros indesejados
# result_wout_errors = result_60k[(result_60k['Error'] == 0)]
result_wout_errors = result_60k[(result_60k['sS3'] != 1)]
print('total w/ sS3 != 1 = '+str(len(result_wout_errors)))

result_wout_errors = result_60k[numpy.isfinite(result_60k['CN'])]
print('total w/ CN != nan = '+str(len(result_wout_errors)))

result_wout_errors.to_csv(sys.argv[2],index=False)