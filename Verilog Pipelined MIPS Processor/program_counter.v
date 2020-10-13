module program_counter#(parameter N = 32)
    (input              clock,
    input               reset,
    input               d_h,
    input               c_h,
    input   [N-1:0]     in,
    output  reg [N-1:0] out
    );

    always@(posedge clock) begin
        if(reset == 1) 
            out <= 32'h003FFFFC; // not sure
        else begin
            if(d_h == 1)
                out <= in - 4;
            else if(c_h == 1) 
                out <= 32'h00000000;
            else
                out <= in;
        end 
    end

endmodule