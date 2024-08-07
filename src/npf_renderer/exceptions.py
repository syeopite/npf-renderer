class RenderErrorDisclaimerError(Exception):
    """Raised when the rendered result may contain errors.

    This is primarily used as a warning. As such the rendered result (wrong as it may be) is
    passed along and can be retrieved.

    """

    def __init__(self, message, rendered_result):
        super().__init__(message)

        self.rendered_result = rendered_result
