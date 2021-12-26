`ifndef ${t_uvc_name_upper}_IF_SV
`define ${t_uvc_name_upper}_IF_SV

interface ${t_uvc_name}_if;

   // Check flags
   bit   has_checks = 1;
   bit   has_coverage = 1;

   // signal declaration
   logic                                 clk;    
   logic                                 resetn; 
   logic [ `${t_uvc_name_upper}_ADDR_WIDTH-1:0  ] addr;
   logic [ `${t_uvc_name_upper}_DATA_WIDTH-1:0  ] wdata;
   logic [ `${t_uvc_name_upper}_DATA_WIDTH-1:0  ] rdata;


   /***************************/
   /* ASSERTIONS               */
   /***************************/

   /***************************/
   /* COVERAGE                 */
   /***************************/




endinterface : ${t_uvc_name}_if

`endif // ${t_uvc_name_upper}_IF_SV


