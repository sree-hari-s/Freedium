import warnings
from typing import Any, Dict, Optional

from httpx import (
    AsyncClient,
    AsyncHTTPTransport,
    Client,
    HTTPTransport,
    Response,
    Timeout,
)

from .config import RequestConfig


# https://github.com/encode/httpx/discussions/1748
class Request:
    __slots__ = ("config", "_in_context_manager")

    def __init__(self, config: Optional[RequestConfig] = None):
        self.config = config or RequestConfig()
        self._in_context_manager = False
        warnings.warn(
            "Request should be used as a context manager using 'with' or 'async with' "
            "to ensure proper resource cleanup",
            stacklevel=2,
        )

    @property
    def proxy_url(self) -> Optional[str]:
        return self.config.proxy.url if self.config.proxy else None

    @property
    def _transport(self) -> HTTPTransport:
        return HTTPTransport(retries=self.config.retries)

    @property
    def _client(self) -> Client:
        return Client(
            transport=self._transport,
            proxies=self.proxy_url,
        )

    @property
    def _async_transport(self) -> AsyncHTTPTransport:
        return AsyncHTTPTransport(retries=self.config.retries)

    @property
    def _async_client(self) -> AsyncClient:
        return AsyncClient(
            transport=self._async_transport,
            proxies=self.proxy_url,
        )

    @property
    def _timeout_client(self) -> Timeout:
        timeout = Timeout(timeout=self.config.timeout)
        return timeout

    def __enter__(self):
        self._in_context_manager = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()

    async def __aenter__(self):
        self._in_context_manager = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_client.aclose()

    def __del__(self):
        self._client.close()
        # asyncio.run(self._async_client.aclose()) # TODO: doesn't work

    def _check_context_manager(self):
        if not self._in_context_manager:
            warnings.warn(
                "Request is not being used as a context manager. This may lead to "
                "resource leaks. Use 'with' or 'async with' statement.",
                stacklevel=2,
            )

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return self._client.get(
            url,
            params=params,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return self._client.post(
            url,
            json=data,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return self._client.put(
            url,
            json=data,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return self._client.delete(
            url,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    async def aget(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return await self._async_client.get(
            url,
            params=params,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    async def apost(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return await self._async_client.post(
            url,
            json=data,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    async def aput(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return await self._async_client.put(
            url,
            json=data,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )

    async def adelete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = True,
    ) -> Response:
        self._check_context_manager()
        return await self._async_client.delete(
            url,
            headers=headers,
            follow_redirects=follow_redirects,
            timeout=self._timeout_client,
        )
