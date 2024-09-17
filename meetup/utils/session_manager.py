from enum import StrEnum
from typing import Dict, Optional, Self
import httpx

from .global_errors import ServerTimeOutError


class RequestMethods(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"


class SessionManager:
    def __init__(self, headers: Dict[str, str], timeout: int = 60) -> None:
        self.client = httpx.Client(headers=headers, timeout=timeout)
        self.aclient: httpx.AsyncClient = None

    def __await__(self) -> Self:
        return self.async_init(self.client.headers, self.client.timeout).__await__()

    async def async_init(self, headers: Dict[str, str], timeout: int = 60) -> None:
        self.aclient = httpx.AsyncClient(headers=headers, timeout=timeout)

    def send_requst(
        self,
        url: str,
        request_method: RequestMethods = RequestMethods.GET,
        params: Optional[Dict[str, str]] = None,
    ):
        try:
            request = self.client.build_request(
                request_method.value, url, params=params
            )
            response = self.client.send(request)
        except httpx.HTTPStatusError as e:
            raise ServerTimeOutError(location=url) from e
        return response

    async def asend_requst(
        self,
        url,
        request_method: RequestMethods = RequestMethods.GET,
        params: Optional[Dict[str, str]] = None,
    ):
        if self.aclient is None:
            return None
        try:
            request = await self.aclient.build_request(
                request_method.value, url, params=params
            )
            response = await self.aclient.send(request)
        except httpx.HTTPStatusError as e:
            raise ServerTimeOutError(location=url) from e
        return response

    def close(self):
        self.client.close()

    async def aclose(self):
        if self.aclient is None:
            return None
        self.aclient.aclose()


class Session(SessionManager):

    # def __await__(self) -> Self:
    #     return self.async_init(self.client.headers, self.client.timeout).__await__()

    # def async_init(self, headers: Dict[str, str], timeout: int = 60) -> None:
    #     self.aclient = httpx.AsyncClient(headers=headers, timeout=timeout)

    def get(self, url: str, params: Optional[Dict[str, str]] = None):
        return self.send_requst(url, params=params)
