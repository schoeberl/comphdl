// File: m_vending.v
// Generated by MyHDL 0.9dev
// Date: Fri Feb  7 10:28:49 2014


`timescale 1ns/10ps

module m_vending (
    clock,
    reset,
    button,
    led
);
// 

input clock;
input reset;
input [3:0] button;
output [7:0] led;
reg [7:0] led;

reg [3:0] bitem;
reg [4:0] ccoin;
reg [28:0] ticks;
reg [6:0] ccost;
reg [2:0] state;
reg [2:0] itemi;
reg [3:0] _button;
reg user_reset;
reg [3:0] bbounce;





always @(bbounce) begin: M_VENDING_RTL_BITS2INT
    if (((bbounce > 0) && (bbounce < 9))) begin
        case (bbounce)
            0: bitem = (-1);
            1: bitem = 1;
            2: bitem = 2;
            3: bitem = (-1);
            4: bitem = 3;
            5: bitem = (-1);
            6: bitem = (-1);
            7: bitem = (-1);
            8: bitem = 4;
            9: bitem = (-1);
            10: bitem = (-1);
            11: bitem = (-1);
            12: bitem = (-1);
            13: bitem = (-1);
            14: bitem = (-1);
            default: bitem = (-1);
        endcase
    end
    else begin
        bitem = 0;
    end
end


always @(bitem, itemi, state) begin: M_VENDING_RTL_COIN
    case (bitem)
        0: ccoin = 0;
        1: ccoin = 1;
        2: ccoin = 5;
        3: ccoin = 10;
        default: ccoin = 25;
    endcase
    if ((state == 3'b010)) begin
        case (itemi)
            0: ccost = 0;
            1: ccost = 20;
            2: ccost = 100;
            3: ccost = 40;
            default: ccost = 55;
        endcase
    end
end


always @(posedge clock) begin: M_VENDING_RTL_SM
    reg [4-1:0] itemb;
    reg [7-1:0] total;
    if (reset == 1) begin
        state <= 3'b000;
        ticks <= 0;
        led <= 0;
        itemi <= 0;
        itemb = 0;
        total = 0;
    end
    else begin
        ticks <= (ticks + 1);
        if (user_reset) begin
            state <= 3'b101;
        end
        else if ((state == 3'b000)) begin
            total = 0;
            if (((bbounce > 0) && (bbounce < 9))) begin
                itemb = button;
                itemi <= bitem;
                ticks <= 0;
                state <= 3'b001;
                led <= (itemb << 2);
            end
        end
        else if ((state == 3'b001)) begin
            if ((bbounce == 0)) begin
                state <= 3'b010;
            end
        end
        else if ((state == 3'b010)) begin
            if (((ticks >= 200000000) || (total > ccost))) begin
                state <= 3'b100;
                led <= 255;
            end
            else if (((bbounce > 0) && (bbounce < 9))) begin
                total = (total + ccoin);
                if ((total == ccost)) begin
                    state <= 3'b011;
                    ticks <= 0;
                    itemi <= 1;
                    led <= 195;
                end
                else begin
                    state <= 3'b001;
                    ticks <= 0;
                end
            end
        end
        else if ((state == 3'b011)) begin
            if ((ticks > (500 * 50000))) begin
                ticks <= 0;
                itemi <= (itemi + 1);
                if (((itemi % 2) == 1)) begin
                    led <= (itemb << 2);
                end
                else begin
                    led <= 195;
                end
                if ((itemi == 6)) begin
                    state <= 3'b101;
                end
            end
        end
        else if ((state == 3'b101)) begin
            state <= 3'b000;
            led <= 0;
        end
        else if ((state == 3'b100)) begin
            led <= 255;
        end
        else begin
            if (1'b0 !== 1) begin
                $display("*** AssertionError ***");
            end
        end
    end
end


always @(posedge clock) begin: M_VENDING_RTL_DEBOUNCE
    if (reset == 1) begin
        _button <= 0;
        bbounce <= 0;
    end
    else begin
        if (((ticks % (50000 * 4)) == 0)) begin
            _button <= button;
            if ((button == _button)) begin
                bbounce <= button;
            end
        end
    end
end


always @(bbounce) begin: M_VENDING_RTL_USER_RESET
    integer ii;
    integer bcnt;
    bcnt = 0;
    for (ii=0; ii<4; ii=ii+1) begin
        if (bbounce[ii]) begin
            bcnt = bcnt + 1;
        end
    end
    if ((bcnt > 1)) begin
        user_reset = 1'b1;
    end
    else begin
        user_reset = 1'b0;
    end
end

endmodule