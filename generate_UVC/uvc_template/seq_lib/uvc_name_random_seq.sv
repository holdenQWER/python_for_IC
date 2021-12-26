`ifndef ${t_uvc_name_upper}_RANDOM_SEQ_SV
`define ${t_uvc_name_upper}_RANDOM_SEQ_SV
class ${t_uvc_name}_random_seq extends ${t_uvc_name}_seq_base;

   `uvm_object_utils(${t_uvc_name}_random_seq)

   function new(string name = "${t_uvc_name}_random_seq"); 
      super.new(name);
      req = ${t_uvc_name}_seq_item::type_id::create("req"); 
   endfunction : new

   virtual task body();
      begin
         `uvm_info(get_type_name(), "Starting...", UVM_DEBUG)
         start_item(req);
         assert(req.randomize()); 
         finish_item(req);
      end
   endtask : body

endclass : ${t_uvc_name}_random_seq

`endif //${t_uvc_name_upper}_RANDOM_SEQ_SV
