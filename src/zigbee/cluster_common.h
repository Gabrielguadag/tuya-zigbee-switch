#ifndef _CLUSTER_COMMON_H_
#define _CLUSTER_COMMON_H_

#include <stddef.h>

#define SETUP_ATTR_FOR_TABLE(table, attr_index, attr_id, attr_type, flag_val, attr_data) \
        table[attr_index].attribute_id = attr_id;                                        \
        table[attr_index].data_type_id = attr_type;                                      \
        table[attr_index].flag         = flag_val;                                       \
        table[attr_index].size         = (uint8_t)sizeof(attr_data);                     \
        table[attr_index].value        = (uint8_t *)&attr_data;

#define SETUP_ATTR(attr_index, attr_id, attr_type, flag_val, attr_data)                     \
        SETUP_ATTR_FOR_TABLE(cluster->attr_infos, attr_index, attr_id, attr_type, flag_val, \
                             attr_data)

/* Endpoint numbers run 1..ZIGBEE_MAX_ENDPOINTS (endpoints[] in
 * config_parser.c). The per-cluster lookup tables are indexed by endpoint
 * NUMBER, not by position, so they need one entry more than there are
 * endpoints: sized at 10 for up to 10 endpoints, endpoint 10 was written one
 * past the end of each. ENDPOINT_LOOKUP bounds the read. */
#define ZIGBEE_MAX_ENDPOINTS    10
#define ENDPOINT_TABLE_SIZE     (ZIGBEE_MAX_ENDPOINTS + 1)
#define ENDPOINT_LOOKUP(table, ep) \
        ((ep) < (sizeof(table) / sizeof((table)[0])) ? (table)[ep] : NULL)
#define ENDPOINT_REGISTER(table, ep, cluster)                  \
        do {                                                   \
            if ((ep) < (sizeof(table) / sizeof((table)[0]))) { \
                (table)[ep] = (cluster);                       \
            }                                                  \
        } while (0)

#ifndef STRINGIFY
#define _STRINGIFY(x)                      #x
#define STRINGIFY(x)                       _STRINGIFY(x)
#endif

#define DEF_STR(string, name)              struct { uint8_t len; char str[sizeof(string) - 1]; \
} const name = { sizeof(string) - 1, string }
#define DEF_STR_NON_CONST(string, name)    struct { uint8_t len; char str[sizeof(string) - 1]; \
}       name = { sizeof(string) - 1, string }

#endif
