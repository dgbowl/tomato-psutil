import time

from tomato_psutil import DriverInterface, Task

kwargs = {"address": None, "channel": None}
NAME = "psutil"


def test_create_teardown_device():
    interface = DriverInterface()
    print(f"{interface=}")
    ret = interface.cmp_register(name=NAME, **kwargs)
    assert ret.success
    print(f"{interface.devmap=}")
    assert NAME in interface.devmap
    ret = interface.cmp_quit(name=NAME)
    assert ret.success
    assert NAME not in interface.devmap


def test_get_attr():
    interface = DriverInterface()
    ret = interface.cmp_register(name=NAME, **kwargs)
    ret = interface.cmp_attrs(name=NAME)
    assert ret.success
    assert "mem_total" in ret.data
    ret = interface.cmp_get_attr(attr="mem_total", name=NAME)
    assert ret.success
    assert isinstance(ret.data, int) and ret.data > 1e6


def test_task_random():
    interface = DriverInterface()
    interface.cmp_register(name=NAME, **kwargs)
    task = Task(
        component_role="a1",
        max_duration=1.0,
        sampling_interval=0.1,
        technique_name="mem_info",
    )
    ret = interface.task_start(task=task, name=NAME)
    print(f"{ret=}")
    assert ret.success
    time.sleep(0.2)

    ret = interface.cmp_status(name=NAME)
    print(f"{ret=}")
    assert ret.success
    assert ret.data.state == "task"
    while ret.data.state == "task":
        time.sleep(0.2)
        ret = interface.cmp_status(name=NAME)
    ret = interface.task_data(name=NAME)
    assert ret.success
    print(f"{ret.data=}")
    assert ret.data.uts.shape == (10,)
    assert ret.data["mem_usage"].shape == (10,)
