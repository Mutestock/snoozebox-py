from abc import ABC

class BlockWriter(ABC):
    subject: str

    def write(self, config: dict) -> None:
        pass

    def write_test(self, config: dict) -> None:
        pass

    def docker_compose_write(self, config: dict) -> None:
        pass
    
    def config_write(self, config: dict) -> None:
        pass
    

        

