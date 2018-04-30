# buildTexSubFiguresNapoles.py
# Build Tex document with subfigures.
# input: path to stamps (fit), path to figures, tex file name, texwidth percentage for each subfigure.
# output: tex file for generating pdf with subfigures.

import sys
import os

def getRaDec(filename):
	filename = ".".join(filename.split(".")[:-1])

	string2return = "(" + filename.split("_")[-2] + "," + filename.split("_")[-1] + ")"
	
	return string2return

E_path = sys.argv[1] # must end with "/"
S_path = sys.argv[2] # must end with "/"
texFile = sys.argv[3]
percent = sys.argv[4]

extension = '.png'

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
			+"\\usepackage[table]{xcolor} \n\n"\
			+"\\begin{document}\n\n"\
			+"\t\\section{Classified as Elliptical Galaxies}\n\n"


with open (texFile, 'wb') as out:
	out.write(texHeader)

# build table mapping numbers to files
# table = "\n\t\\begin{longtable}[!ht]\n\t\\centering\n\t\\rowcolors{2}{gray!25}{white}\n" \
# 		+ "\t\\begin{tabular}{c|c}\n\t\t\\hline\n\t\t\\rowcolor{gray!50}\n" \
# 		+ "\t\t\\textbf{Num} & \\textbf{File} \\ \hline\n"

# table = "\n\t\\begin{longtable}{c|c}\n\t\t\\hline\n" \
# 		+ "\t\t\\textbf{Num} & \\textbf{File} \\ \hline\n"

i = 0

## build tex subfigures code
# for each png file in directory
for file in os.listdir(E_path):
	if (not os.path.isdir(file) and file.endswith(extension) ):

		filename = "{" + ".".join(file.split(".")[:-1]) + "}." + file.split(".")[-1]

		# first of the row
		if (i % 3 == 0):	
			subFigures = "\t\\begin{figure}[!ht]\n\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
	   	# last of the row
	   	elif (i % 3 == 2):
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	   				+"\t\end{figure}\n"
	   	# middle of the row
	   	else:
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+E_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
		    				 		
		with open (texFile, 'ab') as out:
			out.write(subFigures)

		i += 1
		# table = table + "\t\t" + str(i) + " & " + objId + "\\\\ \\hline\n"

if (i % 3 == 2):
	with open (texFile, 'ab') as out:
		out.write("\t\end{figure}\n")

temp = i
i = 0

with open (texFile, 'ab') as out:
	out.write("\n\t\\clearpage\n\t\\section{Classified as Spiral Galaxies}\n\n")

# for each png file in directory
for file in os.listdir(S_path):
	if (not os.path.isdir(file) and file.endswith(extension) ):

		filename = "{" + ".".join(file.split(".")[:-1]) + "}." + file.split(".")[-1]

		# first of the row
		if (i % 3 == 0):	
			subFigures = "\t\\begin{figure}[!ht]\n\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
	   	# last of the row
	   	elif (i % 3 == 2):
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	   				+"\t\end{figure}\n"
	   	# middle of the row
	   	else:
	   		subFigures = "\t\t\\begin{subfigure}[b]{"+percent+"\\textwidth} \n"\
					+"\t\t\t\\includegraphics[width=\\linewidth]{"+S_path+filename+"}\n"\
	    			+"\t\t\t\caption*{"+getRaDec(file)+"}\n"\
	    			+"\t\t\end{subfigure}%%\n"\
	    			+"\t\t\hspace{0.03\\textwidth}\n"
		    				 		
		with open (texFile, 'ab') as out:
			out.write(subFigures)

		i += 1		
		temp += 1
		# table = table + "\t\t" + str(temp) + " & " + objId + "\\\\ \\hline\n"

if (i % 3 == 2):
	with open (texFile, 'ab') as out:
		out.write("\t\end{figure}\n")

# table = table + "\t\\end{tabular}\n\t\\caption{Map of figures and files}\n\\end{longtable}\n\n"

texFooter = "\\end{document}"

with open (texFile, 'ab') as out:
	# out.write(table)
	out.write(texFooter)
