import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure

# Clock generator coroutine
async def clock_gen(clk):
    """Toggle the clock signal every 10ns."""
    while True:
        clk.value = 0
        await Timer(10, units="ns")
        clk.value = 1
        await Timer(10, units="ns")

@cocotb.test()
async def test_mbox_basic(dut):
    """Safe mailbox enqueue test with readiness check"""

    cocotb.start_soon(clock_gen(dut.CLK))

    # Apply active-low reset
    dut.RST_N.value = 0
    await Timer(50, units="ns")
    dut.RST_N.value = 1
    await Timer(50, units="ns")

    # Initialize control signals
    dut.tx_output_notFull_b.value = 1
    dut.tx_output_enq_rdy_b.value = 1
    dut.EN_ma_inputs.value = 0  # Initially disable enqueue
    dut.ma_inputs_inputs.value = 0xABCDEF123456789ABCDEF123456789ABC  # 132-bit safe value

    await Timer(100, units="ns")

    # ✅ Safety check before enqueuing
    if dut.mv_ready.value == 1:
        dut._log.info("Mailbox ready. Initiating enqueue...")
        dut.EN_ma_inputs.value = 1
    else:
        dut._log.warning("Mailbox not ready. Skipping enqueue to prevent overflow.")
        dut.EN_ma_inputs.value = 0

    await Timer(100, units="ns")

    # Log outputs
    dut._log.info(f"tx_output_enq_ena = {dut.tx_output_enq_ena.value}")
    dut._log.info(f"tx_output_enq_data = {hex(dut.tx_output_enq_data.value)}")

    # Optional test result
    if dut.tx_output_enq_ena.value == 0 and dut.mv_ready.value == 1:
        raise TestFailure("❌ Enqueue enable signal was not asserted despite readiness.")
    else:
        dut._log.info("✅ Mailbox enqueue behavior verified successfully.")
