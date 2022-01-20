from importlib import import_module
from types import ModuleType
from pkgutil import iter_modules
from apps.feedback.bots.vk.base import BaseVkBot
import apps.feedback.bots.vk.endpoints


def has_init_endpoints_method(module: ModuleType) -> bool:
    return hasattr(module, "init_endpoints") and callable(module.init_endpoints)


def init_endpoints(app: BaseVkBot):
    package = apps.feedback.bots.vk.endpoints
    prefix = package.__name__ + "."
    for _, name, _ in iter_modules(package.__path__, prefix):
        module = import_module(name)
        if has_init_endpoints_method(module):
            module.init_endpoints(app)
