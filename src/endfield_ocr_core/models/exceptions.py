class RegionNotFoundException(Exception):
    def __init__(self, region):
        super().__init__(f"Unable to find region: {region}")


class ItemNotFoundException(Exception):
    def __init__(self, item):
        super().__init__(f"Unable to find item: {item}")
