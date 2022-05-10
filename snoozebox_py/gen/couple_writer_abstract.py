from abc import ABC


class CoupleWriter(ABC):
    subject: str

    def write(self, config: dict) -> None:
        pass

    def write_test(self, config: dict) -> None:
        pass

