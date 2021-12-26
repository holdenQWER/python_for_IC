`ifndef ${t_uvc_name_upper}_SEQ_ITEM_SV
`define ${t_uvc_name_upper}_SEQ_ITEM_SV
class ${t_uvc_name}_seq_item extends uvm_sequence_item;

// add field
   rand bit [ `${t_uvc_name_upper}_ADDR_WIDTH-1:0]        addr;
   rand bit [ `${t_uvc_name_upper}_DATA_WIDTH-1:0][31:0]  data;
   rand access_type_e                            access;


   `uvm_object_utils_begin(${t_uvc_name}_seq_item)
      `uvm_field_int(addr, UVM_DEFAULT)
      `uvm_field_int(data, UVM_DEFAULT)
      `uvm_field_enum(access_type_e, access, UVM_DEFAULT) 
   `uvm_object_utils_end

// add constraint


   function new (string name = "${t_uvc_name}_seq_item");
      super.new(name);
   endfunction : new

endclass : ${t_uvc_name}_seq_item

`endif // ${t_uvc_name_upper}_SEQ_ITEM_SV
