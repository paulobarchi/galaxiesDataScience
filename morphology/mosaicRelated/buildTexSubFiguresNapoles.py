# buildTexSubFiguresNapoles.py
# Build Tex document with subfigures.
# input: path to stamps (fit), path to figures, tex file name, texwidth percentage for each subfigure.
# output: tex file for generating pdf with subfigures.

import sys
import os

def removeExtension(filename):
	return filename.split(".")[0]

E_path = sys.argv[1] # must end with "/"
S_path = sys.argv[2] # must end with "/"
texFile = sys.argv[3]
percent = sys.argv[4]

extension = 'png'

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
			+"\\usepackage{subcaption} \n\n"\
			+"\\begin{document}\n\n"\
			+"\t\\section{Classified as Elliptical Galaxies}\n\n"


with open (texFile, 'wb') as out:
	out.write(texHeader)

i = 0

## build tex subfigures code
# for each png file in directory
for file in os.listdir(E_path):
	if (not os.path.isdir(file) and file.endswith(extension) ):

		objId = removeExtension(file)

		# first of the row
		if (i % 3 == 0):	
			subFigures = "\t\\begin{figure}[!ht]\n\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
	   	# last of the row
	   	elif (i % 3 == 2):
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	   				+"\t\end{figure}\n"
	   	# middle of the row
	   	else:
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
		    				 		
		with open (texFile, 'ab') as out:
			out.write(subFigures)

		i += 1

if (i % 3 == 2):
	with open (texFile, 'ab') as out:
		out.write("\t\end{figure}\n")

i = 0

with open (texFile, 'ab') as out:
	out.write("\n\t\\clearpage\n\t\\section{Classified as Spiral Galaxies}\n\n")

# for each png file in directory
for file in os.listdir(S_path):
	if (not os.path.isdir(file) and file.endswith(extension) ):

		objId = removeExtension(file)

		# first of the row
		if (i % 3 == 0):	
			subFigures = "\t\\begin{figure}[!ht]\n\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
	   	# last of the row
	   	elif (i % 3 == 2):
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	   				+"\t\end{figure}\n"
	   	# middle of the row
	   	else:
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+file+"}\n"\
	    			+"\t\t\t\caption*{"+objId+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
		    				 		
		with open (texFile, 'ab') as out:
			out.write(subFigures)

		i += 1

if (i % 3 == 2):
	with open (texFile, 'ab') as out:
		out.write("\t\end{figure}\n")

texFooter = "\\end{document}"

with open (texFile, 'ab') as out:
	out.write(texFooter)
