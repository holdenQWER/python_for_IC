`ifndef ${t_uvc_name_upper}_COMMON_SV
`define ${t_uvc_name_upper}_COMMON_SV

// add defines, parameters, typedefs, enums...


// defines signal widths
`define ${t_uvc_name_upper}_ADDR_WIDTH    32 
`define ${t_uvc_name_upper}_DATA_WIDTH    32 

// define enums 
typedef enum {READ=0, WRITE} access_type_e;

// define struct
typedef struct packed{
   byte val1_f;
   byte val2_f;
   byte val3_f;
   byte val4_f;
} val_t;

// define common method
function int calculate_size ();
   return 100;
endfunction: calculate_size


`endif// ${t_uvc_name_upper}_COMMON_SV

