import httpx
from enum import StrEnum
from typing import TypeVar, Dict, Optional

from .global_errors import ServerTimeOutError

RequestSession = TypeVar("RequestSession", "requests.Session", None)


class RequestMethods(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"


class SessionManager:
    def __init__(self, url: str, headers: Dict[str, str], timeout:int=60) -> None:
        self.url = url
        self.client = httpx.Client(headers=headers, timeout=timeout)

    def send_requst(
        self,
        request_method: RequestMethods = RequestMethods.GET,
        params: Optional[Dict[str, str]] = None,
    ):
        try:
            request = self.client.build_request(
                request_method.value, self.url, params=params)
            response = self.client.send(request)
        except httpx.HTTPStatusError as e:
            raise ServerTimeOutError(location=self.url) from e
        return response

    def close(self):
        self.client.close()

       