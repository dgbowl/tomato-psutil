from tomato.driverinterface_1_0 import ModelInterface, Attr, Task
import psutil
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


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

        def __init__(self, driver, key, **kwargs):
            super().__init__(driver, key, **kwargs)
            self._cpu_usage

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

    def dev_set_attr(self, **kwargs) -> None:
        logger.warning("No attrs are read-write in tomato-psutil.")
        pass
