class ConfigValidationError(Exception):
    """Raised when there is an error in the config file."""

    def __init__(self, custom_msg):
        self.custom_msg = custom_msg
        super().__init__()

    def __str__(self):
        return f"{self.custom_msg}"
