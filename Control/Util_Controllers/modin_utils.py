
import warnings
import psutil
import gc
import os


def init_modin(cpu: bool = True, parallel: bool = True):
    """Initialize Modin to use all available cores on the host.

    This function should be called before any other Modin functions are used.
    """
    import modin.config as config
    from modin.config import Engine
    config.NPartitions.put(os.cpu_count())
    if cpu:
        if parallel:
            Engine.put("ray")  # Modin will use Ray
            import ray
            ray.init(runtime_env={'env_vars': {'__MODIN_AUTOIMPORT_PANDAS__': '1'}})
        else:
            Engine.put("pandas")  # Modin will use Pandas
    else:
        Engine.put("cudf")  # Modin will use cuDF
    # Engine.put("dask")  # Modin will use Dask
    # Engine.put("python")  # Modin will use Python
    os.environ["RAY_DISABLE_MEMORY_MONITOR"] = "1"
    warnings.filterwarnings("ignore")


def auto_garbage_collect(pct=80.0):
    """
    auto_garbage_collection - Call the garbage collection if memory used is greater than 80% of total available memory.
                              This is called to deal with an issue in Ray not freeing up used memory.

        pct - Default value of 80%.  Amount of memory in use that triggers the garbage collection call.
    """
    if psutil.virtual_memory().percent >= pct:
        gc.collect()
    return


def on_demand_garbage_collect():
    """
    on_demand_garbage_collect - Call the garbage collection at demand.
                                This is called to deal with an issue in Ray not freeing up used memory.
    """
    gc.collect()
    return

