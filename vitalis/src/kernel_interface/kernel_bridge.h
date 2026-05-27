#ifndef VITALIS_KERNEL_BRIDGE_H
#define VITALIS_KERNEL_BRIDGE_H

// Core interface for kernel-to-user space communication
struct vitalis_state {
    unsigned long cpu_load;
    unsigned long memory_usage;
    int kernel_hook_active;
};

#endif
