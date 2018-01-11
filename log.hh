#ifndef __LOG_HH__
#define __LOG_HH__

#include <cstdio>
#include <cstdlib>
#include <cerrno>
#include <cstring>


#define panic(fmt, ...) \
    do { \
        fprintf(stderr, "Panic: " fmt " [%s]\n", ##__VA_ARGS__, __FUNCTION__); \
        exit(0); \
    } while (false)


#endif // __LOG_HH__
