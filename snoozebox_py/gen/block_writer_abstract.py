from abc import ABC

class BlockWriter(ABC):
    subject: str

    def write(self, config: dict) -> None:
        pass

    def write_test(self, config: dict) -> None:
        pass

    def write_docker_compose(self, config: dict) -> None:
        pass
    
    def write_config(self, config: dict) -> None:
        pass
    

        

