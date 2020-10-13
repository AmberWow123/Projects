module control(
    input [5:0] opcode,
    input [5:0] func,
    input [4:0] Rd,
    input [4:0] Rt,
    output reg RegDst,
    output reg MemToReg,
    output reg Jump,
    output reg re_in,
    output reg we_in,
    output reg [5:0] Func_in,
    output reg ALUSrc,
    output reg RegWrite,
    output reg [1:0] size_in
);

initial begin
    RegDst = 1'b0;
    MemToReg = 1'b0;
    Jump = 1'b0;
    re_in = 1'b0;
    we_in = 1'b0;
    Func_in = 6'b000000;
    ALUSrc = 1'b0;
    size_in = 2'b11;
end

always @(*) begin
    if(opcode == 6'h23) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 1;
        we_in = 0;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100000;
    end
    else if(opcode == 6'h2b) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 0;
        re_in = 0;
        we_in = 1;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100000;
    end
    else if(opcode == 6'h08) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100000;
    end
    else if(opcode == 6'h00) begin
        RegDst = 1;
        ALUSrc = 0;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        if(func == 6'h20) 
            Func_in = 6'b100000;
        else if(func == 6'h22)
            Func_in = 6'b100010;
        else if(func == 6'h24)
            Func_in = 6'b100100;
        else if(func == 6'h25)
            Func_in = 6'b100101;
        else if(func == 6'h27)
            Func_in = 6'b100111;
        else if(func == 6'h26)
            Func_in = 6'b100110;
    // addu
        else if(func == 6'b100001)
            Func_in = 6'b100001;
    // subu
        else if(func == 6'b100011)
            Func_in = 6'b100011;
    // slt
        else if(func == 6'b101010)
            Func_in = 6'b101000;
    // sltu
        else if(func == 6'b101011)
            Func_in = 6'b101001;
    // sll
        else if(func == 0) begin
            if(Rd == 6'b00000) begin
                Func_in = 6'b100000;
                RegDst = 0;
                RegWrite = 0;
            end
            else
                Func_in = 6'b000000;
        end 
        //jr 
        else if (func == 6'h08) begin
            Jump = 1;
            Func_in = 6'b100000;
            RegDst = 0;
        end 
        //jalr 
        else if (func == 06'h09) begin
            Jump = 1;
            RegDst = 1;
            Func_in = 6'b100000;
        end   
    // sra
        else 
            Func_in = 6'b000011;
        
    end
    else if(opcode == 6'h20) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 1;
        we_in = 0;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b00;
        Func_in = 6'b100000;
    end
    else if(opcode == 6'h21) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 1;
        we_in = 0;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b01;
        Func_in = 6'b100000;
    end
    else if (opcode == 6'h28) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 0;
        re_in = 0;
        we_in = 1;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b00;
        Func_in = 6'b100000;
    end
    else if (opcode == 6'h29) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 0;
        re_in = 0;
        we_in = 1;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b01;
        Func_in = 6'b100000;
    end
    else if (opcode == 6'h24) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 1;
        we_in = 0;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b00;
        Func_in = 6'b100000;
    end
    else if (opcode == 6'h25) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 1;
        we_in = 0;
        MemToReg = 1;
        Jump = 0;
        size_in = 2'b01;
        Func_in = 6'b100000;
    end
    // jal
    else if (opcode == 6'h03) begin
        RegDst = 1;
        ALUSrc = 0;
        MemToReg = 0;
        Func_in = 6'b100000;
        size_in = 2'b11;
        re_in = 0;
        we_in = 0;
        Jump = 1;
        RegWrite = 1;
    end
    else if (opcode == 6'h04) begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b111100;
    end
    else if (opcode == 6'h05) begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b111101;
    end
    else if (opcode == 6'h01) begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b111001;
        if(Rt == 6'b00001) 
            Func_in = 6'b111000;
    end
    else if (opcode == 6'h06) begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b111110;
    end
    else if (opcode == 6'h07) begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b111111;
    end
    else if (opcode == 6'h09) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100001;
    end
    else if (opcode == 6'h0c) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100100;
    end
    // ori
    else if (opcode == 6'h0d) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100101;
    end
    else if (opcode == 6'h0e) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b100110;
    end
    // lui
    else if(opcode == 6'h0f) begin
        RegDst = 0;
        ALUSrc = 1;
        RegWrite = 1;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 0;
        size_in = 2'b11;
        Func_in = 6'b000000;
    end
    else begin
        RegDst = 0;
        ALUSrc = 0;
        RegWrite = 0;
        re_in = 0;
        we_in = 0;
        MemToReg = 0;
        Jump = 1;
        size_in = 2'b11;
        Func_in = 6'b000000;
    end
end




endmodule