#! /usr/bin/env python
# coding = utf-8
from string import Template

#field { }
#reg { field_in_reg }
#block { reg_in_block }

field_template = Template('''\
field ${t_field} {
   bits    ${t_width}\t;
   access  ${t_type}\t;
   reset   ${t_init}\t;
}

''')

field_in_reg_template = Template('''\
   field   ${t_reg}_${t_field}(${t_reg_l}_reg_${t_field_l}[${t_width}:0]) @${t_lsb};
''')

reg_template = Template('''\
register ${t_module}_${t_reg}_REG {
   bytes 4 ;
${t_field}}

''')

reg_in_block_template = Template('''\
   register ${t_module}_${t_reg}_REG @${t_offset};
''')

block_template = Template('''\
block ${t_module} {
   bytes 4 ;
${t_reg}
}
''')

reg_struct_template = Template('''\
typedef struct __${t_regname} {
${t_field_declaration}\
} ${t_regname}\n
''')

block_struct_template = Template('''\
typedef struct __${t_regname} {
${t_reg_declaration}\
} ${t_regname}_BLOCK
''')

field_declaration_template = Template('''\
   uint32_t ${t_fieldname} : ${t_width};
''')

reg_declaration_template = Template('''\
   volatile ${t_regname} ${t_reg};/* ${t_offset} */
''')


constraint_reg_template = Template('''\
constraint ${t_module}_dut_cfg::${t_reg}_reg_typical {
${t_field}}
''')

constraint_field_template = Template(''' // m_${t_reg}_${t_field}
''')

cfg_template = Template('''\
class ${t_module}_dut_cfg extends uvm_object;

   `uvm_object_utils_begin(${t_module}_dut_cfg)
${t_part1}
   `uvm_object_utils_end

   ral_block_${t_module_u} m_reg_model_h; //m_reg_model_h
   uvm_path_e m_path;	// operation path for backdoor or frontdoor. default path: frontdoor
${t_part2}

${t_part3}
   extern function new(string name = "${t_module}_dut_cfg");
endclass

function ${t_module}_dut_cfg::new(string name = "${t_module}_dut_cfg");
   super.new(name);

   // set default value for register write enable
${t_part4}

   // set default value for field in each register
${t_part5}
endfunction : new
''')

part1_field_template = Template('''\
   `uvm_field_int(m_${t_reg}_${t_field}, UVM_DEFAULT)\n''')

part2_reg_template = Template('''\
//--------------------------------------------------------------------------------------------------------
// ${t_reg}_reg
// Description : N A
//--------------------------------------------------------------------------------------------------------
//    m_${t_reg}_reg_en
//    Description : m_${t_reg}_reg_en can be used to control wheather corresponding register can be written.
//	                 value 1 : can be written value 0 : not be written value default : 1
   bit m_${t_reg}_reg_en; // m_${t_reg}_reg_en
${t_field}
''')

part2_field_template = Template('''\
   //	   m_${t_reg}_${t_field}
   //	   Description : N A
   rand bit ${t_bits} m_${t_reg}_${t_field}; // m_${t_reg}_${t_field}\n''')

part3_reg_template = Template('''\
   constraint ${t_reg}_reg_typical;\n''')

part4_reg_template = Template('''\
   m_${t_reg}_reg_en = 1;\n''')

part5_field_template = Template('''\
   m_${t_reg}_${t_field} = ${t_values};\n''')

