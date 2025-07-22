import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

coverage_points = {
    "Enqueue Basic": False,
    "Dequeue Basic": False
}

@cocotb.test()
async def test_mailbox_basic(dut):
    """Mailbox test: enqueue and dequeue a value"""

    # Clock generator
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)

    # Enqueue data
    dut.enq.value = 1
    dut.data_in.value = 0xABCD1234
    await RisingEdge(dut.clk)
    dut.enq.value = 0
    coverage_points["Enqueue Basic"] = True

    # Small delay
    await Timer(20, units="ns")

    # Dequeue data
    dut.deq.value = 1
    await RisingEdge(dut.clk)
    dut.deq.value = 0
    await RisingEdge(dut.clk)  # Give DUT time to update data_out
    coverage_points["Dequeue Basic"] = True

    # Log output
    actual = dut.data_out.value.integer
    expected = 0xABCD1234
    dut._log.info(f"🧪 DUT data_out = {hex(actual)}")

    # Assertion
    assert actual == expected, f"❌ Output mismatch: Expected {hex(expected)}, got {hex(actual)}"
    dut._log.info("✅ Output matched expected value")

    # Coverage report
    covered = sum(hit for hit in coverage_points.values())
    total = len(coverage_points)
    percent = (covered / total) * 100
    for feature, hit in coverage_points.items():
        status = "✅ Covered" if hit else "❌ Not Covered"
        dut._log.info(f"{feature}: {status}")
    dut._log.info(f"📈 Overall Coverage: {covered}/{total} = {percent:.2f}%")

    # Save coverage report
    with open("coverage_log.txt", "w") as f:
        f.write(f"Coverage: {covered}/{total} = {percent:.2f}%\n")
        for feature, hit in coverage_points.items():
            mark = "✔️" if hit else "❌"
            f.write(f"{feature}: {mark}\n")
