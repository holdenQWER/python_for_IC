`ifndef ${t_uvc_name_upper}_PKG_SV
`define ${t_uvc_name_upper}_PKG_SV

package ${t_uvc_name}_pkg;
   import uvm_pkg::* ;
   `include "uvm_macros.svh"

   `include "${t_uvc_name}_common.sv"
   `include "${t_uvc_name}_config.sv"
   `include "${t_uvc_name}_seq_item.sv"
   `include "${t_uvc_name}_sequencer.sv"
   `include "../seq_lib/${t_uvc_name}_seq_list.sv"
   `include "${t_uvc_name}_coverage.sv"
   `include "${t_uvc_name}_monitor.sv"
   `include "${t_uvc_name}_driver.sv"
   `include "${t_uvc_name}_agent.sv"

endpackage : ${t_uvc_name}_pkg

   `include "${t_uvc_name}_if.sv"

`endif // ${t_uvc_name_upper}_PKG_SV

