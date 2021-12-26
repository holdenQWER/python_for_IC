`ifndef ${t_uvc_name_upper}_SEQUENCER_SV
`define ${t_uvc_name_upper}_SEQUENCER_SV

class ${t_uvc_name}_sequencer extends uvm_sequencer #(${t_uvc_name}_seq_item);

   `uvm_component_utils(${t_uvc_name}_sequencer)

   function new (string name = "${t_uvc_name}_sequencer", uvm_component parent = null); 
      super.new(name, parent);
   endfunction : new

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);
   endfunction : build_phase

endclass : ${t_uvc_name}_sequencer

`endif //${t_uvc_name_upper}_SEQUENCER_SV

