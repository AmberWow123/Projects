module adder#(parameter dw = 32)
(
    input   [dw-1:0] data,
    output  [dw-1:0] result
);

    assign result = data + 4;

endmodule