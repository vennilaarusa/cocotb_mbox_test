module mkmbox (
    input clk,
    input reset,
    input enq,
    input deq,
    input [31:0] data_in,
    output reg [31:0] data_out,
    output reg full,
    output reg empty
);

reg [31:0] fifo [0:3];
integer wr_ptr = 0;
integer rd_ptr = 0;

always @(posedge clk) begin
    if (reset) begin
        wr_ptr <= 0;
        rd_ptr <= 0;
        data_out <= 0;
        full <= 0;
        empty <= 1;
    end else begin
        if (enq && !full) begin
            fifo[wr_ptr % 4] <= data_in;
            wr_ptr <= wr_ptr + 1;
        end
        if (deq && !empty) begin
            data_out <= fifo[rd_ptr % 4];
            rd_ptr <= rd_ptr + 1;
        end
        full <= ((wr_ptr - rd_ptr) == 4);
        empty <= (wr_ptr == rd_ptr);
    end
end

endmodule
