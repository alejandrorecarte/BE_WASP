class DbException(Exception):
    def __init__(self, message: str):
        # Llamamos al constructor de la clase base (Exception)
        super().__init__(message)
        self.message = message


class ControlledException(Exception):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
