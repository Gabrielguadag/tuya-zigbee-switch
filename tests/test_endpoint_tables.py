"""The last endpoint of a full layout must be as usable as the first.

The per-cluster lookup tables are indexed by endpoint number, which starts at
1, and were sized 10 for up to 10 endpoints: endpoint 10 registered itself one
entry past the end of its table. Four switches and six relays (MAX_RELAYS is
6) is such a layout. A plain build does not always show the overwrite; built
with -fsanitize=address, the stub stops on it in relay_cluster_add_to_endpoint.
"""
from client import StubProc
from conftest import Device
from zcl_consts import ZCL_ATTR_START_UP_ONOFF, ZCL_CLUSTER_ON_OFF

CFG = "StubManufacturer;StubDevice;SA0u;SA1u;SA2u;SA3u;RB0;RB1;RB2;RB3;RB4;RB5;"
RELAY_EPS = range(5, 11)
STARTUP = [0, 1, 2, 0, 1, 2]


def test_every_relay_endpoint_of_a_ten_endpoint_layout():
    proc = StubProc(device_config=CFG).start()
    try:
        device = Device(proc)
        for ep, mode in zip(RELAY_EPS, STARTUP):
            device.write_zigbee_attr(ep, ZCL_CLUSTER_ON_OFF, ZCL_ATTR_START_UP_ONOFF, mode)
        for ep, mode in zip(RELAY_EPS, STARTUP):
            assert device.read_zigbee_attr(ep, ZCL_CLUSTER_ON_OFF, ZCL_ATTR_START_UP_ONOFF) == str(mode)
        assert proc.is_running()
    finally:
        proc.stop()
