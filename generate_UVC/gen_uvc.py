#! /usr/bin/env python
# coding = utf-8
import os,sys,shlex,re
from string import Template

uvc_name = ''
if len(sys.argv) == 2:
   uvc_name = sys.argv[1]
else:
   sys.exit('''
            usage:\tpython gen_uvc.py {uvc_name}\n
            example:\tpython gen_uvc.py uart\n
            result:\tgenerate direcotry [uart_uvc]
   ''')

template_path = os.getcwd() + os.sep + 'uvc_template'
uvc_path = os.getcwd() + os.sep + uvc_name + '_uvc'
print (template_path)
print (uvc_path)
os.system('cp %s %s -r'%(template_path,uvc_path))

cmd = ('find %s -name "*sv"'%uvc_path)
print(os.getcwd())
filelist = os.popen(cmd).read().split()

for file in filelist:
   with open (file,'r+') as fh:
      text = Template(fh.read()).safe_substitute(t_uvc_name = uvc_name, t_uvc_name_upper = uvc_name.upper(),)
      file_new = re.sub('uvc_name',uvc_name,file)
      print(file_new)
      os.system('touch %s'%file_new)
      with open (file_new,'r+') as fh_new:
         fh_new.write(text)
      os.system('rm -f %s'%file)
