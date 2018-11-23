#!/usr/bin/python
#

from __future__ import print_function
from bcc import BPF
from time import sleep

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(times, int);

int time(struct pt_regs *ctx) {
    if (!PT_REGS_PARM1(ctx))
        return 0;

    int i;
    u64 zero = 0, *val;

    bpf_probe_read(&i, sizeof(int), &PT_REGS_PARM1(ctx));
    // could also use `counts.increment(i)`
    val = times.lookup_or_init(&i, &zero);
    (*val)++;
    return 0;
};
""")
b.attach_uprobe(name="./hello_world_uprobe", sym="hello_world", fn_name="time")

# header
print("Tracing hello_world_uprobe()... Hit Ctrl-C to end.")

# sleep until Ctrl-C
try:
    sleep(99999999)
except KeyboardInterrupt:
    pass

# print output
print("%10s %10s" % ("TIME", "RANDOM"))
times = b.get_table("times")
for k, v in sorted(times.items(), key=lambda times: times[1].value):
    print("%10d %10d" % (v.value, k.value))
