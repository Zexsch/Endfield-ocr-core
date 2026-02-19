class RegionNotFoundException(Exception):
    def __init__(self, region):
        super().__init__(f"Unable to find region: {region}")
