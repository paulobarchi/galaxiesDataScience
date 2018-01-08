# plotSepBC_x_k.py
# Plot different geometric histogram separations versus sExtractor detection threshold (k) values.
# input: name of file with separation values, desired metric.
# output: plots.

import sys
import pandas as pd
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib import pylab
from matplotlib.font_manager import FontProperties
matplotlib.style.use('ggplot')

inputfile = sys.argv[1]
metric = sys.argv[2]

df = pd.read_csv(inputfile)

for title, group in df.groupby(metric):
	plt.plot(group['k'], group['SepRoot'], label=title)
fontP = FontProperties()
fontP.set_size('small')
pylab.legend(prop = fontP, loc=2, bbox_to_anchor=(0.5, -0.1), ncol=2, borderaxespad=0.)

plt.gcf().subplots_adjust(bottom=0.55, left=0.55)
# plt.tight_layout()
plt.show()

# print df
# df_copy = pd.read_csv(inputfile)


# plot k x SepRoot group by metric

# for index, row in df.iterrows():
# 	title = "Config: " + str(row['s2'])
# 	for index_copy, row_copy in df_copy.iterrows():
# 	plt.clf() # clear the entire current figure
# 	plt.plot(predictions, label = 'predicted')
# 	plt.legend(loc='upper left')
# 	# plt.show()
# 	plt.savefig(output_path + replaceExtension(filename))
# 	plt.close()
