from enum import StrEnum
from typing import Dict, Optional, Self, Union
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
    def __init__(self, headers: Dict[str, str] = None, timeout: int = 60) -> None:
        self.headers = headers
        self.timeout = timeout
        self.client = httpx.Client(headers=self.headers, timeout=self.timeout)
        self.aclient: httpx.AsyncClient = None

    def send_requst(
        self,
        url: str,
        request_method: RequestMethods = RequestMethods.GET,
        params: Optional[Dict[str, str]] = None,
    ):
        if self.client is None:
            return None  #TODO: add a logger here
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
            return None  #TODO: add a logger here
        try:
            request = self.client.build_request(
                request_method.value, url, params=params
            )
            response = await self.aclient.send(request)
        except httpx.HTTPStatusError as e:
            raise ServerTimeOutError(location=url) from e
        return response

    def __enter__(self) -> Self:
        return self

    async def __aenter__(self) -> Self:
        self.aclient = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.client.close()

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.aclient.aclose()


class Session(SessionManager):

    def get(self, url: str, params: Optional[Dict[str, str]] = None):
        return self.send_requst(url, params=params)

    async def aget(self, url: str, params: Optional[Dict[str, str]] = None):
        return await self.asend_requst(url, params=params)
