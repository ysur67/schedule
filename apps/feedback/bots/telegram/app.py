from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

import apps.feedback.bots.telegram.endpoints
from apps.feedback.bots.telegram.base import BaseTelegramBot


def has_init_endpoints_method(module: ModuleType) -> bool:
    return hasattr(module, "init_endpoints") and callable(module.init_endpoints)


def init_endpoints(app: BaseTelegramBot):
    package = apps.feedback.bots.telegram.endpoints
    prefix = package.__name__ + "."
    for _, name, _ in iter_modules(package.__path__, prefix):
        module = import_module(name)
        if has_init_endpoints_method(module):
            module.init_endpoints(app)
