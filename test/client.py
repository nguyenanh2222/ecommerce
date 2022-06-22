import typing
from typing import Any
from typing import Dict, MutableMapping
from urllib.parse import urljoin

import requests
from starlette.testclient import Params, DataType, Cookies, FileType, AuthType, TimeOut


class HyperClient(requests.Session):
    _context: Dict = {}

    def __init__(
            self,
            base_url: str = "http://localhost:8000",
    ):
        super().__init__()
        self.base_url = base_url

    def request(  # type: ignore
            self,
            method: str,
            url: str,
            params: Params = None,
            data: DataType = None,
            headers: MutableMapping[str, str] = None,
            cookies: Cookies = None,
            files: FileType = None,
            auth: AuthType = None,
            timeout: TimeOut = None,
            allow_redirects: bool = None,
            proxies: MutableMapping[str, str] = None,
            hooks: typing.Any = None,
            stream: bool = None,
            verify: typing.Union[bool, str] = None,
            cert: typing.Union[str, typing.Tuple[str, str]] = None,
            json: typing.Any = None,
    ) -> requests.Response:
        url = urljoin(self.base_url, url)
        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )

    @property
    def context(self) -> Dict:
        return self._context

    def get_context(self, key) -> Any:
        return self._context.get(key)

    def put_context(self, d: Dict) -> Any:
        self._context.update(d)


client = HyperClient()
