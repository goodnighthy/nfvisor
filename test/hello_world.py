#!/usr/bin/python
#
# USAGE: hellow_world PID

from __future__ import print_function
from bcc import BPF, USDT
import sys

if len(sys.argv) < 2:
    print("USAGE: hellow_world PID")
    exit()
pid = sys.argv[1]
debug = 0

# load BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
int do_trace(struct pt_regs *ctx) {
    int i;
    bpf_usdt_readarg(1, ctx, &i);
    bpf_trace_printk("BPF %d: Hello World!\\n", i);
    return 0;
};
"""

# enable USDT probe from given PID
u = USDT(pid=int(pid))
u.enable_probe(probe="hello_probe", fn_name="do_trace")
if debug:
    print(u.get_text())
    print(bpf_text)

# initialize BPF
b = BPF(text=bpf_text, usdt_contexts=[u])

# header
print("BPF terminal")

# format output
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    except ValueError:
        print("value error")
        continue
    print("%s" % msg)
