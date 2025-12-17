class ValueUtil:
    @classmethod
    def coalesce(cls, *vals):
        for val in vals:
            if val is not None:
                return val
        return None

