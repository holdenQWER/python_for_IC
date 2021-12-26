`ifndef ${t_uvc_name_upper}_AGENT_SV
`define ${t_uvc_name_upper}_AGENT_SV
class ${t_uvc_name}_agent extends uvm_agent;

   ${t_uvc_name}_config    cfg;
   ${t_uvc_name}_driver    driver;
   ${t_uvc_name}_monitor   monitor;
   ${t_uvc_name}_coverage  coverage; 
   ${t_uvc_name}_sequencer sequencer;

   `uvm_component_utils_begin(${t_uvc_name}_agent)
      `uvm_field_object(cfg, UVM_DEFAULT)
   `uvm_component_utils_end

   function new (string name = "${t_uvc_name}_agent", uvm_component parent = null); 
      super.new(name, parent);
   endfunction : new

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);

      // Get Configuration
      if (!uvm_config_db#(${t_uvc_name}_config)::get(this, "", "cfg", cfg)) begin 
         `uvm_fatal(get_type_name(), "Config not set for slave agent using default is_active") 
      end

      // Create components
      monitor = ${t_uvc_name}_monitor::type_id::create("monitor",this);
      monitor.cfg = cfg;
      if (cfg.has_coverage) begin
         coverage = ${t_uvc_name}_coverage::type_id::create("coverage", this);
      end

      if (cfg.is_active == UVM_ACTIVE) begin
         sequencer = ${t_uvc_name}_sequencer::type_id::create("sequencer",this); 
         driver = ${t_uvc_name}_driver::type_id::create("driver",this);
      end

   endfunction : build_phase

   function void connect_phase(uvm_phase phase); 
      if (cfg.has_coverage) begin
         monitor.ap.connect(coverage.analysis_export);
      end

      if (cfg.is_active == UVM_ACTIVE) begin
         driver.cfg = cfg;
         // Connect the driver to the sequencer using TLM interface 
         driver.seq_item_port.connect(sequencer.seq_item_export); 
      end
   endfunction : connect_phase

endclass : ${t_uvc_name}_agent


`endif // ${t_uvc_name_upper}_AGENT_SV
