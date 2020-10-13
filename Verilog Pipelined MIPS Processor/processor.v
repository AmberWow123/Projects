`timescale 1ns / 1ps

// How to connect the processor to data_memory ?
module processor(
    input clock,
    input reset,
    input [7:0] serial_in,
    input serial_valid_in,
    input serial_ready_in,
    output [7:0] serial_out,
    output serial_rden_out,
    output serial_wren_out
);
    // connect program counter
    wire [31:0] pc_in, pc_out;
    wire [31:0] t_out, pc_ex;
    wire c_h, d_h;
    wire [31:0] br_out_ex;
    wire [31:0] new_pc;
    program_counter pc(.clock(clock), .d_h(d_h), .c_h(c_h), .reset(reset), .in(t_out), .out(pc_out));
    //assign pc_in = (pc_out == 0) ? (pc_ex + 4) : pc_in;
    // connect adder    
    adder pc_add(.data(pc_out), .result(pc_in));

   

    // mux for branch target
    wire [31:0] br_target;
    wire [31:0] extend_output, sign_extend_out;
    wire [4:0] write_reg_out;
    wire RegDst, MemToReg, Jump, re_in, we_in, ALUSrc, RegWrite,
         RegDst_out, MemToReg_out, Jump_o, re_in_out, we_in_out, ALUSrc_out, RegWrite_out;
    wire [31:0] br_out;
    wire Branch_out;
    wire Jump_out;
    wire [31:0] inst, inst_out;
    wire [31:0] read_data1, read_data2, readdata1_out, readdata2_out;
    wire [31:0] addr_in;
    assign br_target = (Branch_out) ? br_out_ex : (extend_output << 2) + pc_in;

    mux #(.WIDTH(32)) mux_br (
        .d0(br_target), .d1({pc_in[31:28],inst[25:0],2'b00}), .s(Jump), .y(br_out)
        );


    // connect instrction memory
    ///fib/fib.inst_rom.memh
    //hello_world/hello_world.inst_rom.memh
    inst_rom#(.INIT_PROGRAM("C:/Users/Richard/Downloads/lab4-files-2/memh/fib/fib.inst_rom.memh"),
              .ADDR_WIDTH(10)) 
    inst_mem(.clock(clock), .reset(reset), .addr_in(addr_in), .data_out(inst)); 
    assign addr_in = (d_h) ? pc_out : t_out;


    // connect control unit
    wire [5:0] Func_in, Func_in_out;
    wire [1:0] size_in, size_in_out;
    control control_unit(.opcode(inst[31:26]), .func(inst[5:0]), .Rd(inst[15:11]), .Rt(inst[20:16]), .RegDst(RegDst), .MemToReg(MemToReg), .Jump(Jump),
                         .re_in(re_in),  .we_in(we_in), .Func_in(Func_in), .ALUSrc(ALUSrc), .RegWrite(RegWrite), .size_in(size_in));

    // connect mux 1
    wire [4:0] data4;
    wire [4:0] mux_res1;
    assign data4 = (inst[31:26] == 6'h03) ? 5'h1f : inst[15:11];
    mux #(.WIDTH(5)) mux_5bit (
        .d0(inst[20:16]), .d1(data4), .s(RegDst), .y(mux_res1)
        );

    // connect reg file
    wire [31:0] mux_res3;
    reg_file reg_f(.clock(clock), .reset(reset), .reg1(inst[25:21]), .reg2(inst[20:16]), .write_reg(write_reg_out), 
                   .write_enable(RegWrite_out), .wr_data(mux_res3), .read_data1(read_data1), .read_data2(read_data2));


     //mux for taken or not    
    wire [31:0] d1;
    wire s;
    wire isjal, isjal_out;
    wire isjr;
    wire isj;
    wire isjalr, isjalr_out;
    assign isjal = (inst[31:26] == 6'h03) ? 1 : 0;
    assign isjr = (inst[31:26] == 6'h00 && inst[5:0] == 6'h08) ? 1 : 0;
    assign isjalr = (inst[31:26] == 6'h00 && inst[5:0] == 6'h09) ? 1 : 0;
    assign isj = (inst[31:26] == 6'h02) ? 1: 0;
    assign s = (isjal || isjr || isjalr || isj) ? Jump : (Branch_out | Jump_out);
    assign d1 =(isjr || isjalr) ? read_data1 : (isjal) ? {pc_in[31:28],inst[25:0],2'b00} : br_out;

    mux #(.WIDTH(32)) mux_t (
        .d0(new_pc), .d1(d1), .s(s), .y(t_out)
    );
    assign new_pc = (pc_out == 0) ? (pc_ex + 4) : pc_in;
    //connect sign extend
    wire extend_or_not;
    assign extend_or_not = (inst[31:26] == 6'h0c || inst[31:26] == 6'h0d || inst[31:26] == 6'h0e ) ? 0 : 1;
    sign_extend s_e(.in(inst[15:0]), .s(extend_or_not), .out(extend_output));



    hazard_detection h_d_u(.id_reg1(inst[25:21]), .reset(reset), .id_reg2(inst[20:16]), .id_opcode(inst[31:26]), .id_func(inst[5:0]), .dest(write_reg_out), .control_hazard(c_h), .data_hazard(d_h));

    if_id_reg if_id_stage(.clock(clock), .br_out(br_out), .MemToReg(MemToReg), .size_in(size_in), .d_h(d_h), .Jump(Jump), .re_in(re_in), .we_in(we_in), .Func_in(Func_in), .ALUSrc(ALUSrc), .RegWrite(RegWrite),
                          .pc_in(pc_out), .inst(inst), .readdata1(read_data1), .readdata2(read_data2), .sign_extend(extend_output), .write_reg(mux_res1), .MemToReg_out(MemToReg_out), .br_out_o(br_out_ex),
                          .Jump_out(Jump_o), .re_in_out(re_in_out), .we_in_out(we_in_out), .Func_in_out(Func_in_out), .ALUSrc_out(ALUSrc_out), .RegWrite_out(RegWrite_out), .pc_in_out(pc_ex),
                          .inst_out(inst_out), .readdata1_out(readdata1_out), .readdata2_out(readdata2_out), .sign_extend_out(sign_extend_out), .write_reg_out(write_reg_out), .size_in_out(size_in_out));

    //connect mux 2
    wire [31:0] mux_res2;

    mux #(.WIDTH(32)) mux_32bit (
        .d0(readdata2_out), .d1(sign_extend_out), .s(ALUSrc_out), .y(mux_res2)
    );
    wire [31:0] data1;
    wire [31:0] data2;
    wire islui;
    wire issll;
    wire issra;
    assign islui = (inst_out[31:26] == 6'h0f) ? 1 : 0;
    assign issll = (inst_out[31:26] == 6'h00 && inst_out[5:0] == 6'h00 && Func_in_out == 6'h00) ? 1 : 0;
    assign issra = (inst_out[31:26] == 6'h00 && inst_out[5:0] == 6'h03 ) ? 1 : 0;
    assign data1 = (islui) ? sign_extend_out : (issra || issll) ? readdata2_out : readdata1_out;
    assign data2 = (islui) ? 32'h0010 : (issra || issll) ? {27'h0000000,inst_out[10:6]} : mux_res2;
    //connect ALU
    wire [31:0] alu_out;
    alu ALU(.Func_in(Func_in_out), .A_in(data1), .B_in(data2), .O_out(alu_out), .Branch_out(Branch_out), .Jump_out(Jump_out));

    //connect data memory
    wire [31:0] readdata_out;
    wire [31:0] writedata_in;
    assign writedata_in = (inst_out[31:26] == 6'h29 ) ? {{16{readdata2_out[15]}},readdata2_out[15:0]} : (inst_out[31:26] == 6'h28) ? {{24{readdata2_out[15]}},readdata2_out[7:0]} : readdata2_out;

    data_memory data_rom(.clock(clock), .reset(reset), .addr_in(alu_out), .writedata_in(writedata_in), .re_in(re_in_out), .we_in(we_in_out), 
                         .size_in(size_in_out), .readdata_out(readdata_out), .serial_in(serial_in), .serial_ready_in(serial_ready_in), .serial_valid_in(serial_valid_in),
                         .serial_out(serial_out), .serial_rden_out(serial_rden_out), .serial_wren_out(serial_wren_out));

    //connect mux 3 
    wire [31:0] data0;
    wire [31:0] loaddata;
    wire [31:0] loaddataunsign;
    wire [31:0] loaddatasigned;
    wire [31:0] loadb;
    wire [31:0] loadh;
    wire [31:0] loadbu;
    wire [31:0] loadhu;
    assign loaddata = (inst_out[31:26] == 6'h20 || inst_out[31:26] == 6'h21) ? loaddatasigned : (inst_out[31:26] == 6'h24 || inst_out[31:26] == 6'h25) ? loaddataunsign : readdata_out;
    assign loaddataunsign = (inst_out[31:26] == 6'h25) ? loadhu : loadbu;
    assign loaddatasigned = (inst_out[31:26] == 6'h21) ? loadh  : loadb;
    assign loadh = (alu_out[1:0] == 2'b10 || alu_out[1:0] == 2'b11) ? {{16{readdata_out[31]}},readdata_out[31:16]} : {{16{readdata_out[15]}},readdata_out[15:0]};
    assign loadhu = (alu_out[1:0] == 2'b10 || alu_out[1:0] == 2'b11) ? {16'h0000, readdata_out[31:16]} : {16'h0000, readdata_out[15:0]};
    assign loadb = (alu_out[1:0] == 2'b00) ? {{24{readdata_out[7]}}, readdata_out[7:0]} : (alu_out[1:0] == 2'b01) ? {{24{readdata_out[15]}}, readdata_out[15:8]} : (alu_out[1:0] == 2'b10) ? {{24{readdata_out[23]}}, readdata_out[23:16]} : {{24{readdata_out[31]}}, readdata_out[31:24]};
    assign loadbu = (alu_out[1:0] == 2'b00) ? {24'h000000,readdata_out[7:0]} : (alu_out[1:0] == 2'b01) ? {24'h000000, readdata_out[15:8]} : (alu_out[1:0] == 2'b10) ? {24'h000000, readdata_out[23:16]} : {24'h000000, readdata_out[31:24]};
    assign isjal_out = (inst_out[31:26] == 6'h03) ? 1 : 0;
    assign isjalr_out = (inst_out[31:26] == 6'h00 && inst_out[5:0] == 6'h09) ? 1 : 0;

    assign data0 = (isjalr_out|| isjal_out) ? (pc_ex + 4) : alu_out;  

    mux #(.WIDTH(32)) mux_data32bit (
        .d0(data0), .d1(loaddata), .s(MemToReg_out), .y(mux_res3)
    );

    
endmodule