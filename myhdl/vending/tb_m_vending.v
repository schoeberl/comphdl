module tb_m_vending;

reg clock;
reg reset;
reg [3:0] button;
wire [7:0] led;

initial begin
    $from_myhdl(
        clock,
        reset,
        button
    );
    $to_myhdl(
        led
    );
end

m_vending dut(
    clock,
    reset,
    button,
    led
);

endmodule
