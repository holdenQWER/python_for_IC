`ifndef ${t_uvc_name_upper}_CONFIG_SV
`define ${t_uvc_name_upper}_CONFIG_SV

class ${t_uvc_name}_config extends uvm_object;

   uvm_active_passive_enum         is_active = UVM_ACTIVE;
   bit                             has_coverage = 1;
   bit                             has_checks = 1;


   `uvm_object_utils_begin(${t_uvc_name}_config)
      `uvm_field_enum(uvm_active_passive_enum, is_active, UVM_DEFAULT)
      `uvm_field_int(has_coverage, UVM_DEFAULT)
      `uvm_field_int(has_checks, UVM_DEFAULT)
   `uvm_object_utils_end

   function new (string name = "${t_uvc_name}_config"); 
      super.new(name);
   endfunction

endclass : ${t_uvc_name}_config

`endif // ${t_uvc_name_upper}_CONFIG_SV

