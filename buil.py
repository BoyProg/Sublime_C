import os,sys,re
import subprocess as sub

Xpath = sys.argv[1]
path = re.search(".*(?=/+[A-Za-z0-9_]+\.c)",Xpath)
Out_name = path.group()+"/"+Xpath.split("/")[-1].split(".")[0]
co =  sub.Popen(['g++','-o','%s'%Out_name,"%s"%Xpath],stdout=sub.PIPE)
co.wait()

co =  os.system('%s.exe'%Out_name)
print()
print()
input("Press any key . . . . ")
