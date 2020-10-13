module reg_file(
    input clock,
    input reset,
    input [4:0] reg1,
    input [4:0] reg2,
    input [4:0] write_reg,
    input write_enable,
    input [31:0] wr_data,
    output [31:0] read_data1,
    output [31:0] read_data2
);
    reg [31:0] reg_mem [0:31];
 
    assign read_data1 = reg_mem[reg1];
    assign read_data2 = reg_mem[reg2];
    integer i,j;
    initial begin
        
        for(i = 0; i < 32; i = i + 1)
            reg_mem[i] = 32'b0;
    end 

    always @(posedge clock) begin
        if(write_enable == 1 && write_reg != 0)
            reg_mem[write_reg] <= wr_data;
        if(reset == 1) begin
            for(j = 0; j < 32; j = j + 1)
                reg_mem[j] = 32'b0;
        end

    end

endmodule