#! /usr/bin/env python
# coding = utf-8
import os
import re
import sys
import argparse
import xlrd3 as xlrd
from string import Template
from filetemplate import *

Regs = {}

## reg  0	    1	      2	    3	     4
##	     RegName Offset  field1 field2 field3...

## field  FieldName(0) AccessType(1) | Msb(2) | Lsb(3) | Width(4) | InitVal(5)

RegName = 0
Offset  = 1
FieldName = 0
AccessType = 1
Msb = 2
Lsb = 3
Width = 4
InitVal = 5


def GetArg():
   parser = argparse.ArgumentParser(usage = '''\n\t$ python %(prog)s -i register_{module_name}.xls -o {directory_name}\n
        #########################################################################################\n
        ##create ral_{module_name}.sv ral_{module_name}.ral in {directory_name}\n
        ##create {module_name}_dut_cfg.sv {module_name}.h in {directory_name}\n
        ##{module_name} should the first sheet in Excel
        #########################################################################################\n'''
        ,
                          description = '')
   parser.add_argument("-i", required=True, help = "Input the spreadsheet file path.")
   parser.add_argument("-o", required=True, help = "Input the output file directory name.")
   args = parser.parse_args()
   return args


def GetExcell(xlsx):
   global Regs
   key = ''
   workbook = xlrd.open_workbook(xlsx)
   sheet = workbook.sheet_by_index(0)
   for rownum in range(sheet.nrows):
      row_val = sheet.row_values(rowx=rownum)
      if re.match(r'Name',row_val[0]):
         counter = 0
         key = row_val[1].strip().upper()
         Regs[key] = [key]
         continue
      elif re.match(r'Offset',row_val[0]):
         offset = row_val[1].split('x')[1]
         Regs[key].append("'h" + offset)
         continue
      elif re.match(r'\[.+\]',row_val[0]):
         Msb = ''
         Lsb = ''
         Width = ''
         result = re.match(r'\[(.+)\]',row_val[0]).group(1)
         if re.search(r':',result):
            Msb = int(result.split(':')[0])
            Lsb = int(result.split(':')[1])
            Width = Msb - Lsb + 1
         else:
            Msb = int(result)
            Lsb = Msb
            Width = 1
         if re.match('reserve',row_val[1],re.I):
            FieldName = row_val[1].strip().upper() + str(counter)
            counter += 1
         else:
            FieldName = row_val[1].strip().upper()
         AccessType = row_val[3].strip().lower()
         InitVal = re.search(r"('h.+)",row_val[4].strip()).group(1)
          #   field name(0) access_type(1) | Msb(2) | Lsb(3) | width(4) | initial value(5)
         field = [FieldName,AccessType,Msb,Lsb,Width,InitVal]
         Regs[key].append(field)


def CheckReg():
   for key in Regs.keys():
      count = 0
      if (int(Regs[key][Offset].split('h')[1],16)%4 != 0):
         sys.exit("Error: the reg:%s address is not 32bit aligned!"%(key))
      for i in range(2,len(Regs[key])):
         field = Regs[key][i]
         count += field[Width]
      if(count != 32):
         sys.exit("Error: the reg:%s width is not 32!"%(key))


def GenRal(modulename):
   s_field_code = ''
   s_reg_code = ''
   s_block_code = ''
   s_reg_in_block_code = ''

   for key in Regs.keys():
      s_field_in_reg_code = ''
      for i in range(2,len(Regs[key])):
         field = Regs[key][i]
         if re.match('reserve',field[FieldName],re.I):
            continue
         tmp_code1 = field_template.substitute(
                        t_field = key+'_'+field[FieldName],
                        t_width = field[Width],
                        t_type = field[AccessType],
                        t_init = field[InitVal],)
         s_field_code += tmp_code1
         tmp_code2 = field_in_reg_template.substitute(
                             t_reg = key,
                             t_reg_l = key.lower(),
                             t_field = field[FieldName],
                             t_field_l = field[FieldName].lower(),
                             t_width = field[Width]-1,
                             t_lsb = hex(field[Lsb]).replace("0x","'h"),)
         s_field_in_reg_code += tmp_code2
      tmp_code3 = reg_template.substitute(t_module = modulename,t_reg=key,t_field= s_field_in_reg_code,)
      s_reg_code += tmp_code3
      tmp_code4 = reg_in_block_template.substitute(t_module = modulename,t_reg=key,t_offset=(Regs[key][Offset]))
      s_reg_in_block_code += tmp_code4
   s_block_code = block_template.substitute(t_module = modulename,t_reg=s_reg_in_block_code,)

   return s_field_code + s_reg_code +s_block_code


def GenDutConstraint(modulename):
   s_reg_code = ''
   for key in Regs.keys():
      s_field_code = ''
      tmp_reg_code = ''
      for i in range(2,len(Regs[key])):
         field = Regs[key][i]
         if re.match('reserve',field[FieldName], re.I):
            continue
         tmp_field_code = constraint_field_template.substitute(
                              t_reg = key.lower(),
                              t_field = field[FieldName].lower(),)
         s_field_code += tmp_field_code
      tmp_reg_code = constraint_reg_template.substitute(
                              t_module = modulename,
                              t_reg = key.lower(),
                              t_field = s_field_code,)
      s_reg_code += tmp_reg_code
   return s_reg_code


def GenDutCfg(modulename):
   s_cfg_code = ''
   s_part1_code = ''
   s_part2_code = ''
   s_part3_code = ''
   s_part4_code = ''
   s_part5_code = ''
   for key in Regs.keys():
      part1_field_code = ''
      part2_field_code = ''
      part5_field_code = ''
      s_regname = key.lower()
      s_part1_code += '	// %s_reg\n'%s_regname
      s_part5_code += '	// %s_reg\n'%s_regname
      tmp3 = part3_reg_template.substitute(t_reg = s_regname)
      tmp4 = part4_reg_template.substitute(t_reg = s_regname)
      for i in range(2,len(Regs[key])):
         field = Regs[key][i]
         s_fieldname = field[FieldName].lower()
         if re.match('reserve',field[FieldName],re.I):
            continue
         if field[Width] == 1:
            bits = '       '
         else:
            bits = r'[%d : 0]'%(field[Width]-1)
         values = str(field[Width])+field[InitVal]
         #values = str(field[Width])+field[InitVal].replace(r"0x",r"'h")
         tmp1 = part1_field_template.substitute(t_reg = s_regname, t_field = s_fieldname)
         part1_field_code += tmp1
         tmp2 = part2_field_template.substitute(t_reg = s_regname, t_field = s_fieldname, t_bits = bits)
         part2_field_code += tmp2
         tmp5 = part5_field_template.substitute(t_reg = s_regname, t_field = s_fieldname, t_values = values)
         part5_field_code += tmp5
      s_part1_code += part1_field_code
      s_part2_code += part2_reg_template.substitute(t_reg = s_regname, t_field = part2_field_code)
      s_part3_code += tmp3
      s_part4_code += tmp4
      s_part5_code += part5_field_code
   s_cfg_code = cfg_template.substitute(t_module = modulename,
                                        t_module_u = modulename.upper(),
                                        t_part1 = s_part1_code,
                                        t_part2 = s_part2_code,
                                        t_part3 = s_part3_code,
                                        t_part4 = s_part4_code,
                                        t_part5 = s_part5_code)
   return s_cfg_code


def GenHeadFile(modulename):
   s_reg_struct = ''
   s_reg_declar = ''
   for key in Regs.keys():
      s_field_code = ''
      tmp_reg_code = ''
      tmp_reg_declar = ''
      for i in range(2,len(Regs[key])):
         field = Regs[key][i]
         tmp_field_code = field_declaration_template.substitute(
                              t_fieldname = "{:<20}".format(field[FieldName].lower()),
                              t_width = "{:<3}".format(field[Width]),)
         s_field_code += tmp_field_code
      tmp_reg_code = reg_struct_template.substitute(
                         t_regname = key,
                         t_field_declaration = s_field_code,)
      s_reg_struct += tmp_reg_code
      tmp_reg_declar = reg_declaration_template.substitute(
                         t_regname = "{:<20}".format(key),
                         t_reg = "{:<20}".format(key.lower()),
                         t_offset = "{:<5}".format(Regs[key][Offset]),)
      s_reg_declar += tmp_reg_declar
   s_block_struct = block_struct_template.substitute(
                         t_regname = modulename.upper(),
                         t_reg_declaration = s_reg_declar,)
   return s_reg_struct + s_block_struct


if __name__ == "__main__":
   cmdline = GetArg()
   result = re.search(r'_(\w+).',cmdline.i)
   modulename = result.group(1)
   GetExcell (cmdline.i)

   CheckReg()

   if os.path.exists(cmdline.o):
      sys.exit("\n\tThe directory already exist! ")
   os.mkdir(cmdline.o)
   os.chdir(cmdline.o)

   #	ral file
   ralfile = 'ral_%s.ralf'%modulename.upper()
   with open (ralfile,'w') as fh:
      fh.write(GenRal(modulename.upper()))
   os.popen('ralgen -uvm -t %s %s -c abf'%(modulename.upper(),ralfile)).read()

   #	constraint file
   constraintfile = '%s_dut_cfg_constraint.sv'%modulename

   with open (constraintfile,'w') as fh:
      fh.write(GenDutConstraint(modulename))

   #	dut cfg file
   dutcfgfile = '%s_dut_cfg.sv'%modulename
   with open (dutcfgfile,'w') as fh:
      fh.write(GenDutCfg(modulename))

   #	c head file
   cheadfile = '%s.h'%modulename
   with open (cheadfile,'w') as fh:
      fh.write(GenHeadFile(modulename))

   print("\n\t Gen reg model done in path %s !"%cmdline.o)
