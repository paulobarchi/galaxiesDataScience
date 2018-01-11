# buildTexSubFigures.py
# Build Tex document with subfigures.
# input: path to stamps (fit), path to figures, tex file name, texwidth percentage for each subfigure.
# output: tex file for generating pdf with subfigures.

import sys
import os

def removeExtension(filename):
	return filename.split(".")[0]

stamps_path = sys.argv[1] # must end with "/"
figs_path = sys.argv[2] # must end with "/"
texFile = sys.argv[3]
percent = sys.argv[4]

extension = ".fit"

texHeader = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"\
			+"% \n"\
			+"% Automatically generated tex file by buildTexSubFigures.py\n"\
			+"% see https://github.com/paulobarchi/galaxiesDataScience \n"\
			+"% \n"\
			+"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"\
			+"\n"\
			+"\\documentclass[12pt]{article} \n"\
			+"\\usepackage[margin=0.7in]{geometry} \n"\
			+"\\usepackage{graphicx} \n"\
			+"\\usepackage{caption} \n"\
			+"\\usepackage{subcaption} \n"\
			+"% \\usepackage{multicol}  \n\n"\
			+"\\begin{document} \n\n"

with open (texFile, 'wb') as out:
	out.write(texHeader)

## for each row, print to file tex subfigures code
# for each fit file in directory
for file in os.listdir(stamps_path):
	if (not os.path.isdir(file) and file.endswith(extension) ):

		objId = removeExtension(file)
		filename = figs_path+objId
		fit = filename+"_fit.png"
		oldMask = filename+"_oldMask.png"
		newMask = filename+"_newMask.png"

		subFigures = "\t\\begin{figure}\n\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					 +"\t\t\t\\includegraphics[width=\\linewidth]{"+fit+"}\n"\
	    			 +"\t\t\end{subfigure}%%\n"\
	    			 +"\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
	            	 +"\t\t\t\\includegraphics[width=\\linewidth]{"+oldMask+"}\n"\
	    			 +"\t\t\end{subfigure}%%\n"\
	    			 +"\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
	    			 +"\t\t\t\\includegraphics[width=\\linewidth]{"+newMask+"}\n"\
	    			 +"\t\t\end{subfigure}%%\n"\
	    			 +"\t\t\caption*{ObjId: "+ objId +"}\n"\
	    			 +"\t\end{figure}\n"
	    				 		
		with open (texFile, 'ab') as out:
			out.write(subFigures)

texFooter = "\\end{document}"

with open (texFile, 'ab') as out:
	out.write(texFooter)
