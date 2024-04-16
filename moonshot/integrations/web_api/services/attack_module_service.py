from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class AttackModuleService(BaseService):

    @exception_handler
    def get_all_attack_module(self) -> list[str]:
        attack_modules = ["attack_module_1", "attack_module_2", "attack_module_3"]
        return attack_modules

    @exception_handler
    def get_attack_module_by_id(self, am_id: str) -> str: 
        attack_modules = "attack_module_3"
        return attack_modules
