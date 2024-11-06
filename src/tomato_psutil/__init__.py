from typing import Union
from functools import wraps
from tomato.driverinterface_1_0 import ModelInterface, Attr, Task
from tomato.models import Reply
import psutil
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def override_key(func):
    @wraps(func)
    def wrapper(self, **kwargs):
        kwargs["address"] = None
        kwargs["channel"] = None
        return func(self, **kwargs)

    return wrapper


class DriverInterface(ModelInterface):
    class DeviceManager(ModelInterface.DeviceManager):
        @property
        def _mem_total(self):
            return psutil.virtual_memory().total

        @property
        def _mem_avail(self):
            return psutil.virtual_memory().available

        @property
        def _mem_usage(self):
            return psutil.virtual_memory().percent

        @property
        def _cpu_usage(self):
            return psutil.cpu_percent(interval=None)

        @property
        def _cpu_freq(self):
            return psutil.cpu_freq().current

        @property
        def _cpu_count(self):
            return psutil.cpu_count()

        def attrs(self, **kwargs):
            return dict(
                mem_total=Attr(type=int, units="bytes"),
                mem_avail=Attr(type=int, units="bytes"),
                mem_usage=Attr(type=float, status=True, units="percent"),
                cpu_count=Attr(type=int),
                cpu_freq=Attr(type=float, units="MHz"),
                cpu_usage=Attr(type=float, status=True, units="percent"),
            )

        def do_task(self, task: Task, **kwargs) -> None:
            self.data["uts"].append(datetime.now().timestamp())
            if task.technique_name in {"mem_info", "all_info"}:
                self.data["mem_total"].append(self._mem_total)
                self.data["mem_avail"].append(self._mem_avail)
                self.data["mem_usage"].append(self._mem_usage)
            if task.technique_name in {"cpu_info", "all_info"}:
                self.data["cpu_count"].append(self._cpu_count)
                self.data["cpu_freq"].append(self._cpu_freq)
                self.data["cpu_usage"].append(self._cpu_usage)

        def get_attr(self, attr: str, **kwargs):
            if hasattr(self, f"_{attr}"):
                return getattr(self, f"_{attr}")

        def set_attr(self, **kwargs):
            pass

        def capabilities(self, **kwargs):
            return {"mem_info", "cpu_info", "all_info"}

    def __init__(self, settings=None):
        super().__init__(settings)
        key = (None, None)
        self.devmap[key] = self.CreateDeviceManager(key)

    def dev_register(self, **kwargs) -> Reply:
        return Reply(
            success=True,
            msg="psutil device always available",
            data=self.devmap[(None, None)].capabilities(),
        )

    @override_key
    def dev_teardown(self, **kwargs) -> Reply:
        return super().dev_teardown(**kwargs)

    @override_key
    def dev_reset(self, **kwargs) -> Reply:
        return super().dev_reset(**kwargs)

    @override_key
    def attrs(self, **kwargs) -> Union[Reply, None]:
        return super().attrs(**kwargs)

    def dev_set_attr(self, **kwargs) -> None:
        logger.warning("No attrs are read-write in tomato-psutil.")
        pass

    @override_key
    def dev_get_attr(self, **kwargs) -> Union[Reply, None]:
        return super().dev_get_attr(**kwargs)

    @override_key
    def dev_status(self, **kwargs) -> Union[Reply, None]:
        return super().dev_status(**kwargs)

    @override_key
    def task_start(self, **kwargs) -> Union[Reply, None]:
        return super().task_start(**kwargs)

    @override_key
    def task_data(self, **kwargs) -> Union[Reply, None]:
        return super().task_data(**kwargs)

    @override_key
    def task_status(self, **kwargs):
        return super().task_status(**kwargs)

    @override_key
    def task_stop(self, **kwargs):
        return super().task_stop(**kwargs)

    @override_key
    def capabilities(self, **kwargs):
        return super().tasks(**kwargs)
