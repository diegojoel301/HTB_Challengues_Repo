import angr
from pwn import ELF
import claripy
import sys

e = ELF("./spookylicence")

BASE = 0x400000
ADDR_START = BASE
ADDR_GOOD = BASE + 0x00187d
# At this point, the checker function has decided to return 0
ADDR_BAD  = BASE + 0x001890

proj = angr.Project(
    e.path, main_opts={"base_addr": BASE}, 
    load_options={
        "auto_load_libs": False, 
        "use_system_libs": False,
    }
)

argv = [proj.filename]

flag_size = 32
sym_arg = claripy.BVS("sym_arg", 8*flag_size)

state = proj.factory.call_state(
    ADDR_START,
    sym_arg)

argv.append(sym_arg)
state = proj.factory.entry_state(args=argv)
sm = proj.factory.simulation_manager(state)

sm.explore(find=ADDR_GOOD, avoid=[ADDR_BAD, BASE + 0x11b8])

if sm.found:
    for i in sm.found:
        print(i.solver.eval(sym_arg,cast_to=bytes).decode('utf-8','ignore'))











