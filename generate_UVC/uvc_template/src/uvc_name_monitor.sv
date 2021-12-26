`ifndef ${t_uvc_name_upper}_MONITOR_SV
`define ${t_uvc_name_upper}_MONITOR_SV
class ${t_uvc_name}_monitor extends uvm_monitor;

   virtual ${t_uvc_name}_if vif;
   ${t_uvc_name}_config     cfg;
   uvm_analysis_port #(${t_uvc_name}_seq_item) ap;

   `uvm_component_utils(${t_uvc_name}_monitor)

   function new(string name = "${t_uvc_name}_monitor", uvm_component parent = null); 
      super.new(name, parent);
   endfunction : new

   virtual function void build_phase(uvm_phase phase);
      super.build_phase(phase) ;

      if(!uvm_config_db#(virtual ${t_uvc_name}_if)::get(this, "", "vif", vif)) 
         `uvm_fatal(get_type_name(),"virtual if not configured");

      ap = new("ap", this);
   endfunction : build_phase

   virtual function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
   endfunction : connect_phase

   task run_phase(uvm_phase phase);
      super.run_phase(phase) ;

      fork
         /* add some task calls here */
         collect_transaction() ;
         observe_reset() ;
      join_none;

   endtask : run_phase

   task observe_reset();
      wait (vif.resetn == 'b0);
      `uvm_info(get_type_name(), "Transaction recording interrupted by reset assertion.", UVM_DEBUG); 
   endtask : observe_reset

   task collect_transaction();

      forever begin

      ${t_uvc_name}_seq_item item = ${t_uvc_name}_seq_item::type_id::create("item");

      if (cfg.has_checks)
         perform_checks();

      ap.write(item);
      end// forever
   endtask : collect_transaction

   function void perform_checks();
   endfunction : perform_checks

   function void report_phase(uvm_phase phase); 
      super.report_phase(phase);
   endfunction : report_phase

endclass : ${t_uvc_name}_monitor

`endif //${t_uvc_name_upper}_MONITOR_SV

