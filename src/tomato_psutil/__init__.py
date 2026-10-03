import logging
from datetime import UTC, datetime

import psutil
import xarray as xr
from tomato.driverinterface_3_0 import (
    Attr,
    ModelComponent,
    ModelInterface,
    Settings,
    Task,
)
from tomato.driverinterface_3_0.decorators import coerce_val
from tomato.driverinterface_3_0.types import Val

logger = logging.getLogger(__name__)


class Settings(Settings):
    idle_measurement_interval: int | None = 10


class DriverInterface(ModelInterface):
    pass


class Component(ModelComponent):
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
        _ = self._cpu_usage

    def attrs(self, **kwargs):
        return {
            "mem_total": Attr(type=int, units="bytes"),
            "mem_avail": Attr(type=int, units="bytes"),
            "mem_usage": Attr(type=float, status=True, units="percent"),
            "cpu_count": Attr(type=int),
            "cpu_freq": Attr(type=float, units="MHz"),
            "cpu_usage": Attr(type=float, status=True, units="percent"),
        }

    def prepare_task(self, task: Task, **kwargs: dict) -> None:
        self.task = task

    def do_measure(self, **kwargs) -> None:
        data_vars = {}
        if self.task is None or self.task.technique_name in {"mem_info", "all_info"}:
            data_vars["mem_total"] = (["uts"], [self._mem_total], {"units": "bytes"})
            data_vars["mem_avail"] = (["uts"], [self._mem_avail], {"units": "bytes"})
            data_vars["mem_usage"] = (["uts"], [self._mem_usage], {"units": "percent"})
        if self.task is None or self.task.technique_name in {"cpu_info", "all_info"}:
            data_vars["cpu_count"] = (["uts"], [self._cpu_count])
            data_vars["cpu_freq"] = (["uts"], [self._cpu_freq], {"units": "MHz"})
            data_vars["cpu_usage"] = (["uts"], [self._cpu_usage], {"units": "percent"})

        uts = datetime.now(UTC).timestamp()
        self.last_data = xr.Dataset(
            data_vars=data_vars,
            coords={"uts": (["uts"], [uts])},
        )

    def get_attr(self, attr: str, **kwargs):
        if hasattr(self, f"_{attr}"):
            return getattr(self, f"_{attr}")

    @coerce_val
    def set_attr(self, attr: str, val: Val, **kwargs):
        pass

    def capabilities(self, **kwargs):
        return {"mem_info", "cpu_info", "all_info"}

    def quit(self, **kwargs):
        pass
