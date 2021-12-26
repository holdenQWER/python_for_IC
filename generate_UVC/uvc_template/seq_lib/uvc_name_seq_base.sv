`ifndef ${t_uvc_name_upper}_SEQ_BASE_SV
`define ${t_uvc_name_upper}_SEQ_BASE_SV
class ${t_uvc_name}_seq_base extends uvm_sequence #(${t_uvc_name}_seq_item);

   `uvm_object_utils(${t_uvc_name}_seq_base)

   function new (string name = "${t_uvc_name}_seq_base"); 
      super.new (name);
   endfunction : new

   virtual task body();
      begin
         super.body();

         `uvm_info(get_type_name(), "Starting...", UVM_DEBUG)

         start_item(req);
         assert (req.randomize()); 
         finish_item(req);
      end
   endtask : body

endclass : ${t_uvc_name}_seq_base

`endif //${t_uvc_name_upper}_SEQ_BASE_SV
