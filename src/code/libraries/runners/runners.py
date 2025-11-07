import importlib
from libraries.utils import runtime, path_config

def main(runtime_vars: dict):
    module_name = runtime_vars.get("module_name")
    function_name = runtime_vars.get("function_name")
    if not module_name or not function_name:
        raise ValueError("Both 'module_name' and 'function_name' must be defined in runtime JSON")
    module = importlib.import_module(module_name)
    funct = getattr(module, function_name, None)
    if not funct:
        raise ImportError(f"Function '{function_name}' not found in module '{module_name}'")
    result = funct(runtime_vars)
    return result

if __name__ == "__main__":
    path = path_config.RUNTIME_PATH / "airport" / "simulations" / "runtime" / "passports.json"
    runtime_vars = runtime.load_runtime_vars(JSON_PATH=path)
    output = main(runtime_vars)
    print(output[0:2])