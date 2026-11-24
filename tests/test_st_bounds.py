"""ST tokens past the switch tables are dropped, not written past them.

switch_clusters[] holds four switches. A fifth ST token used to be written one
entry past its end, over switch_clusters_cnt (built with -fsanitize=address,
the stub stops in parse_config on it). Now it is ignored like an RT token past
MAX_RELAYS, and the first four keep working.
"""
from client import StubProc
from conftest import Device
from zcl_consts import ZCL_ATTR_ONOFF_CONFIGURATION_SWITCH_ACTIONS, ZCL_CLUSTER_ON_OFF_SWITCH_CONFIG

CFG = "StubManufacturer;StubDevice;ST01;ST02;ST03;ST04;ST05;M;"


def test_a_fifth_st_token_is_ignored():
    proc = StubProc(device_config=CFG).start()
    try:
        device = Device(proc)
        for ep in range(1, 5):
            device.read_zigbee_attr(
                ep, ZCL_CLUSTER_ON_OFF_SWITCH_CONFIG, ZCL_ATTR_ONOFF_CONFIGURATION_SWITCH_ACTIONS
            )
        res = proc.exec(
            f"zcl_read 5 0x{ZCL_CLUSTER_ON_OFF_SWITCH_CONFIG:04X} 0x{ZCL_ATTR_ONOFF_CONFIGURATION_SWITCH_ACTIONS:04X}"
        )
        assert not res.ok
        assert proc.is_running()
    finally:
        proc.stop()
