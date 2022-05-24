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

    def write_all(self, config: dict) -> None:
        self.write(config)
        self.write_test(config)
        self.write_docker_compose(config)
        self.write_config(config)
