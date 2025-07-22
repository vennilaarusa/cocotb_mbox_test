SIM ?= icarus

TOPLEVEL_LANG = verilog
TOPLEVEL = mkmbox
MODULE = test_mbox

PWD := $(shell pwd)

VERILOG_SOURCES = $(PWD)/verilog_core/*.v*

COMPILE_ARGS += -I $(PWD)/verilog_core

VVP_EXEC = vvp -M $(shell /mnt/c/Users/latha/Downloads/ceg/venv/bin/cocotb-config --lib-dir) -m libcocotbvpi_icarus sim_build/sim.vvp

# Export virtual environment path to ensure correct Python
export PYTHONPATH := $(PWD):$(PYTHONPATH)


WAVES ?= 1

include /mnt/c/Users/latha/Downloads/ceg/venv/lib/python3.10/site-packages/cocotb/share/makefiles/Makefile.inc
