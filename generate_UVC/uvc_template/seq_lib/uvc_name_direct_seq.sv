`ifndef ${t_uvc_name_upper}_DIRECT_SEQ_SV
`define ${t_uvc_name_upper}_DIRECT_SEQ_SV
class ${t_uvc_name}_direct_seq extends ${t_uvc_name}_seq_base;

   `uvm_object_utils(${t_uvc_name}_direct_seq)

   rand bit [ `${t_uvc_name_upper}_ADDR_WIDTH-1:0]       addr;
   rand bit [ `${t_uvc_name_upper}_DATA_WIDTH-1:0][31:0] data; 
   rand access_type_e                           access;


   function new(string name = "${t_uvc_name}_direct_seq");
      super.new(name);
   endfunction : new


   virtual task body();
      begin
         `uvm_info(get_type_name(), "Starting...", UVM_DEBUG) 
         req = ${t_uvc_name}_seq_item::type_id::create("req");
         start_item(req);
         assert(req.randomize() with { 
            req.addr       ==  local::addr;
            req.data       ==  local::data;
            req.access     ==  local::access;
         });
         finish_item(req);
      end
   endtask : body

endclass : ${t_uvc_name}_direct_seq

`endif //${t_uvc_name_upper}_DIRECT_SEQ_SV
