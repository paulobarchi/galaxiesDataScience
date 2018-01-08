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
# fig, ax = plt.subplots(figsize=(8,6))

# bp = df.groupby(metric).plot(kind='kde', ax=ax)

# df.set_index(metric, append=True).unstack().interpolate().plot(subplots=True)

# fig = plt.figure(1)
# ax = fig.add_subplot(111)

for title, group in df.groupby(metric):
	plt.plot(group['k'], group['SepRoot'], label=title)
# 	group.plot(x='k', y='SepRoot', title=title)
fontP = FontProperties()
fontP.set_size('small')
pylab.legend(prop = fontP, loc=2, bbox_to_anchor=(0.5, -0.1), ncol=2, borderaxespad=0.)


# handles, labels = ax.get_legend_handles_labels()
# lgd = ax.legend(handles, labels, loc='upper right', bbox_to_anchor=(0,0))
# ax.grid('on')
# plt.legend(bbox_to_anchor=(1.2, 1.2), loc=10, ncol=1)

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