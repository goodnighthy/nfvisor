#!/usr/bin/python
#

from __future__ import print_function
from bcc import BPF, USDT
from time import sleep
import sys

if len(sys.argv) < 2:
    print("USAGE: hellow_world_usdt PID")
    exit()
pid = sys.argv[1]
debug = 0

# load BPF program
bpf_text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(trace, int);

int do_trace(struct pt_regs *ctx) {

    return 0;
};
"""
u = USDT(pid=int(pid))
u.enable_probe(probe="hello_probe", fn_name="do_trace")
if debug:
    print(u.get_text())
    print(bpf_text)

# initialize BPF
b = BPF(text=bpf_text, usdt_contexts=[u])
# header
print("Tracing hello_world_uprobe()... Hit Ctrl-C to end.")

# sleep until Ctrl-C
try:
    sleep(99999999)
except KeyboardInterrupt:
    pass
