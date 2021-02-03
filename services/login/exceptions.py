# ---------------------------------------------------------------------
# Additional  exceptions
# ---------------------------------------------------------------------
# Copyright (C) 2021 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

import http

from typing import Any, Dict, Optional


class StarletteHTTPException(Exception):
    def __init__(self, status_code: int, error: str = None) -> None:
        if error is None:
            error = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.error = error

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, error={self.error!r})"


class HTTPException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        error: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, error=error)
        self.headers = headers
