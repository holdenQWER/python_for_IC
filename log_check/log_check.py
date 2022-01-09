#!/usr/bin/env python
import os
import sys
import re
import enum
import datetime
import argparse
from string import Template

def GetArg():
   parser = argparse.ArgumentParser(usage = '''\n\t$ python %(prog)s -l {log_file_path} -r {regex_ignored_file_path}\n
        #########################################################################################\n
        ##after run, the end of log file will append the check result and error line info\n
        #########################################################################################\n'''
        ,
                          description = '')
   parser.add_argument("-l", required=True, help = "The log file path.")
   parser.add_argument("-r", required=True, help = "The regex of ignore_keywords.")
   args = parser.parse_args()
   return args

def CheckPath(log_file,regex_file):
   if not os.path.exists(r'%s'%log_file):
      sys.exit('ERROR: %s is not exist!'%(log_file))
   if not os.path.exists(r'%s'%regex_file):
      sys.exit('ERROR: %s is not exist!'%(regex_file))

def ExtractIgnoreKeywords(regex_file):
   keyword_list = []
   with open (regex_file,'r+') as fh:
      lines = fh.readlines()
   for line in lines:
      if re.match('##NOTE|^\s+$',line):
         continue
      else:
         keyword_list.append(line.strip())
   return keyword_list

def GetTime():
   nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   return nowtime


class Status(enum.Enum):
   RUNNING = 1
   PASS = 2
   FAILED = 3


PASS_PATTERN = '''
\t\t\t \033[0;32;32mPPPP     A     SSSSS  SSSSS
\t\t\t P   P   A A    S      S
\t\t\t PPPP   AAAAA   SSSSS  SSSSS
\t\t\t P     A     A      S      S
\t\t\t P     A     A  SSSSS  SSSSS\033[0m

'''

FAIL_PATTERN = '''
\t\t\t \033[0;32;31mFFFFF    A     IIIII  L
\t\t\t F       A A      I    L
\t\t\t FFFF   AAAAA     I    L
\t\t\t F     A     A    I    L
\t\t\t F     A     A  IIIII  LLLLL\033[0m

'''

SIM_RESULT = Template('''
 ****************************************
 **      Simulaiton Report    
 ** Time : ${t_time}
 ** TestName : ${t_testname}  
 ** Seed : ${t_seed}
 ** Status : ${t_result}
 ****************************************
''')

def GetTestInfo(log_file):
   with open (log_file,'r+') as fh:
      str = fh.read()
   re1 = re.search('\+ntb_random_seed=(\d+)',str,re.M)
   re2 = re.search('automatic random seed used: (\d+)',str,re.M)
   re3 = re.search('\+UVM_TESTNAME=(\w+)',str,re.M)
   re4 = re.search('|'.join(pass_keywords),str,re.M)

   if re1 is not None:
      seed = re1.group(1)
   elif re2 is not None:
      seed = re2.group(1)
   else:
      seed = 'Not find in log'

   if re3 is not None:
      testname = re3.group(1)

   if re4 is not None:
      status = Status.PASS

   return testname,seed,status


def main_code(log_file):
   print ("Parse simulation log ...")
   
   fail_syndrome = ''
   fail_status = ''
   pass_status = ''
   
   testname,seed,pass_status = GetTestInfo(log_file)
   testtime      = GetTime()


   log_fh = open(log_file, "r+")
   log_fh.flush()
   os.fsync(log_fh.fileno())

   for index, line in enumerate(log_fh):
      if fail_pattern.search(line):
         if (ignore_pattern.search(line)):
            continue
         else:
            fail_syndrome += ('Line:%d %s'%(index+1,line))
            fail_status = Status.FAILED
               #break
   
   log_fh.seek(0, 2) # move file pointer to the end of file
   if fail_status == Status.FAILED:
      sim_result = SIM_RESULT.substitute(t_time=testtime,t_testname=testname,t_seed=seed,t_result='FAIL')
      print (FAIL_PATTERN)
      print (sim_result)
      log_fh.write(sim_result)
   elif pass_status == Status.PASS:
      sim_result = SIM_RESULT.substitute(t_time=testtime,t_testname=testname,t_seed=seed,t_result='PASS')
      print (PASS_PATTERN)
      print (sim_result)
      log_fh.write(sim_result)
   else:
      str = "Can't find the test case PASS keywords, please check!!!"
      sim_result = SIM_RESULT.substitute(t_time=testtime,t_testname=testname,t_seed=seed,t_result='NULL')
      print(sim_result)
      print(str)
      log_fh.write(sim_result)
      log_fh.write(str)
      

   # make sure file contents in internal buffer have been writtern to disk
   log_fh.flush()
   os.fsync(log_fh.fileno())
   # run_plan assumes fail syndrome is put in the last line
   log_fh.write(fail_syndrome)
   log_fh.close()

if __name__ == "__main__":
   cmdline = GetArg()
   CheckPath(cmdline.l,cmdline.r)
   pass_keywords = ['TEST PASS', 'SIMULATION PASS', 'Simulation PASSED', 'SvtTestEpilog: Passed']
   fail_keywords = ['error', 'fail', 'fatal', 'violat']
   ignore_keywords = ExtractIgnoreKeywords(cmdline.r)
   pass_pattern   = re.compile('|'.join(pass_keywords),re.IGNORECASE)
   fail_pattern   = re.compile('|'.join(fail_keywords),re.IGNORECASE)
   ignore_pattern = re.compile('|'.join(ignore_keywords),re.IGNORECASE)
   main_code(cmdline.l)



