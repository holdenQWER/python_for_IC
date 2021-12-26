`ifndef ${t_uvc_name_upper}_COVERAGE_SV
`define ${t_uvc_name_upper}_COVERAGE_SV
class ${t_uvc_name}_coverage extends uvm_subscriber #(${t_uvc_name}_seq_item);

   `uvm_component_utils(${t_uvc_name}_coverage)

   ${t_uvc_name}_seq_item item;


   //---------------------------------------------------
   // Cover groups
   //---------------------------------------------------

   covergroup ${t_uvc_name}_active_cg (string name) ; 
      ACCESS_TYPE: coverpoint item.access {
         bins READ  = {READ};
         bins WRITE = {WRITE};
      }
      ADDRESS: coverpoint item.addr {
         //auto bins for now
         option.auto_bin_max = 20;
      }
      DATA: coverpoint item.data {
         //auto bins for now
         option.auto_bin_max = 20;
      }

      ADDR_ACCES: cross ACCESS_TYPE, ADDRESS;
      ADDR_DATA:  cross ADDRESS,DATA;

   endgroup : ${t_uvc_name}_active_cg

   function new(string name = "${t_uvc_name}_coverage", uvm_component parent = null); 
      super.new(name, parent);
      ${t_uvc_name}_active_cg = new(name);
   endfunction : new

   function void write(${t_uvc_name}_seq_item t);
      item = t;
      ${t_uvc_name}_active_cg.sample();
   endfunction : write

endclass : ${t_uvc_name}_coverage

`endif // ${t_uvc_name_upper}_COVERAGE_SV
