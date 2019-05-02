import re
import sys

output_writer=open('output.txt','a')
input_txt=open('input.txt','r').read()
for i in range(1,100000):
	strTxt=re.findall(r'\*\s*(str'+str(i)+r'[^*]*)\*',input_txt)
	if not strTxt:
		output_writer.flush()
		output_writer.close()
		sys.exit()
	for line in strTxt:
		output_writer.write(line+'\n')
	comments=raw_input("str"+str(i)+" inserted. Enter your Txt\n")
	output_writer.write(comments+'\n')
	output_writer.flush()