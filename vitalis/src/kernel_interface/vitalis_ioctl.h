#ifndef VITALIS_IOCTL_H
#define VITALIS_IOCTL_H

#include <linux/ioctl.h>

// Define our custom IOCTL magic number and command codes
#define VITALIS_MAGIC 'v'

// Command to request a high-priority CPU thread from the kernel
#define VITALIS_SET_PRIORITY _IOW(VITALIS_MAGIC, 1, int)

// Command to fetch current kernel-level resource telemetry
#define VITALIS_GET_TELEMETRY _IOR(VITALIS_MAGIC, 2, struct vitalis_state *)

#endif
