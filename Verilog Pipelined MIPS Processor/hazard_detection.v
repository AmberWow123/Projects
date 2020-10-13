module hazard_detection (
    input reset,
    input [4:0] id_reg1,
    input [4:0] id_reg2,
    input [5:0] id_opcode,
    input [5:0] id_func,
    input [4:0] dest,
    output reg control_hazard,
    output reg data_hazard
);

initial begin
    control_hazard = 1'b0;
    data_hazard = 1'b0;
end


wire isbeq;
wire isbne;
wire bltz_or_bgez;
wire isblez;
wire isbgtz;
//wire isj;
//wire isjr;
//wire isjal;
//wire isjalr;
wire br;
wire d_h;

assign d_h = ((dest == id_reg1 || dest == id_reg2) && dest != 0 && reset != 1) ? 1 : 0; 
assign isbeq = (id_opcode == 6'h04) ? 1: 0;
assign isbne = (id_opcode == 6'h05) ? 1: 0;
assign bltz_or_bgez = (id_opcode == 6'h01) ? 1: 0;
assign isblez = (id_opcode == 6'h06) ? 1: 0;
assign isbgtz = (id_opcode == 6'h07) ? 1: 0;
//assign isj = (id_opcode == 6'h02) ? 1: 0;
//assign isjr = (id_opcode == 6'h00 && id_func == 6'h08) ? 1: 0;
//assign isjal = (id_opcode == 6'h03) ? 1: 0;
//assign isjalr = (id_opcode == 6'h00 && id_func == 6'h09) ? 1: 0;
assign br = (isbeq || isbne || bltz_or_bgez || isblez || isbgtz) ? 1 : 0;


always@(*) begin
    if (br) begin
        control_hazard = 1;
        if(d_h)
            data_hazard = 1;
        else
            data_hazard = 0;
    end
    else if (d_h) begin
        data_hazard = 1;
        control_hazard = 0;
    end
    else begin
        data_hazard = 0;
        control_hazard = 0;
    end
end


endmodule