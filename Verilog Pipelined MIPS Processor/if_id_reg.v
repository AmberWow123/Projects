module if_id_reg  (
    input clock,
    input d_h,
    input MemToReg,
    input Jump,
    input [31:0] br_out,
    input re_in,
    input we_in,
    input [5:0] Func_in,
    input ALUSrc,
    input RegWrite,
    input [31:0] pc_in,
    input [1:0] size_in,
    input [31:0] inst,
    input [31:0] readdata1,
    input [31:0] readdata2,
    input [31:0] sign_extend,
    input [4:0] write_reg,
    output reg MemToReg_out,
    output reg Jump_out,
    output reg re_in_out,
    output reg we_in_out,
    output reg [5:0] Func_in_out,
    output reg ALUSrc_out,
    output reg RegWrite_out,
    output reg [31:0] pc_in_out,
    output reg [31:0] inst_out,
    output reg [31:0] readdata1_out,
    output reg [31:0] readdata2_out,
    output reg [31:0] sign_extend_out,
    output reg [1:0] size_in_out,
    output reg [31:0] br_out_o,
    output reg [4:0] write_reg_out
);

always @(posedge clock) begin
    if(d_h) begin
        MemToReg_out <= 0; 
        Jump_out <= 0;
        re_in_out <= 0;
        we_in_out <= 0;
        Func_in_out <= 0;
        ALUSrc_out <= 0;
        RegWrite_out <= 0;
        pc_in_out <= 0;
        inst_out <= 0;
        readdata1_out <= 0;
        readdata2_out <= 0;
        sign_extend_out <= 0;
        write_reg_out <= 0;
        size_in_out <= 0;
    end else begin
        MemToReg_out <= MemToReg; 
        Jump_out <= Jump;
        re_in_out <= re_in;
        we_in_out <= we_in;
        Func_in_out <= Func_in;
        ALUSrc_out <= ALUSrc;
        RegWrite_out <= RegWrite;
        pc_in_out <= pc_in;
        inst_out <= inst;
        readdata1_out <= readdata1;
        readdata2_out <= readdata2;
        sign_extend_out <= sign_extend;
        write_reg_out <= write_reg;
        size_in_out <= size_in; 
        br_out_o <= br_out;
    end
    
end

endmodule