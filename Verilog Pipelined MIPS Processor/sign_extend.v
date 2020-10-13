module sign_extend#(parameter WIDTH = 16)
(
    input [WIDTH-1:0] in,
    input s,
    output [2*WIDTH-1:0] out
);

     /*always_comb begin
         if(in[WIDTH-1] == 1)
            out = {16'hffff,in};
         else
            out = {16'h0000,in};
        
    end*/
    assign out = (s == 1) ? { {WIDTH{in[WIDTH-1]}}, in[WIDTH-1:0] } : {16'h0000, in[WIDTH-1:0]};
endmodule