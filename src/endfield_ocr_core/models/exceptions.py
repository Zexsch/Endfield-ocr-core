class RegionNotFoundException(Exception):
    def __init__(self, region):
        super().__init__(f"Unable to find region: {region}")


class ItemNotFoundException(Exception):
    def __init__(self, item):
        super().__init__(f"Unable to find item: {item}")


class MarketBBoxNotFound(Exception):
    def __init__(self):
        super().__init__("Unable to crop to Market region.")


class NotANumberException(Exception):
    def __init__(self, text: str):
        super().__init__(f"Found OCR is not a number: {text}")
