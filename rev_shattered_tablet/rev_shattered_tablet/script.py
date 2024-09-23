import angr
import claripy
from pwn import *

proj = angr.Project(
    'tablet',
    main_opts = {'base_addr': 0x0},
    load_options = {'auto_load_libs': False}
)

len_flag = 64

flag = claripy.BVS("flag", 8 * len_flag)

state = proj.factory.entry_state(stdin = flag)

state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)

for i in range(10):
    state.solver.add(flag.get_byte(i) >= 0x20)
    state.solver.add(flag.get_byte(i) <= 0x7f)

sm = proj.factory.simulation_manager(state)

FIND_ADDR = 0x1371

AVOID_ADDR = 0x137f

sm.explore(find=FIND_ADDR, avoid=AVOID_ADDR)

print("[*] Flag found: " + sm.found[0].posix.dumps(0).decode("utf-8"))