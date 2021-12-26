`ifndef ${t_uvc_name_upper}_DRIVER_SV
`define ${t_uvc_name_upper}_DRIVER_SV
class ${t_uvc_name}_driver extends uvm_driver #(${t_uvc_name}_seq_item);

   `uvm_component_utils(${t_uvc_name}_driver)

   virtual ${t_uvc_name}_if    vif;
   ${t_uvc_name}_config        cfg;

   function new (string name = "${t_uvc_name}_driver", uvm_component parent = null); 
      super.new(name, parent);
   endfunction : new

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase);

      if(!uvm_config_db#(virtual ${t_uvc_name}_if)::get(this, "", "vif", vif)) 
         `uvm_fatal(get_type_name(),"virtual if not configured");

   endfunction : build_phase

   virtual function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
   endfunction : connect_phase

   task run_phase(uvm_phase phase);
      super.run_phase(phase);

      fork
         /* add other tasks here */
         get_and_drive();
         observe_reset();
      join_none;
   endtask : run_phase

   task initialize();
   /* add interface initialize */
   endtask : initialize

   task observe_reset();
      forever begin
         @(negedge vif.resetn);
         `uvm_info(get_type_name(), "Reset observed on HRESETn.", UVM_DEBUG); 
         initialize();
      end
   endtask : observe_reset

   task get_and_drive() ;
      initialize() ;

      forever begin
         seq_item_port.get_next_item(req);
         /* add interface driver */ 
         seq_item_port.item_done();
      end // forever
   endtask : get_and_drive

   function void report_phase(uvm_phase phase);
      super.report_phase(phase);
   endfunction : report_phase

endclass : ${t_uvc_name}_driver

`endif // ${t_uvc_name_upper}_DRIVER_SV

