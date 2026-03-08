from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(slots=True)
class GitHubAPIError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class GitHubRepository:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "PortifolioMiguel",
            }
        )

    def get_user_profile(self, username: str) -> dict[str, Any]:
        return self._get_json(f"/users/{username}")

    def get_user_repositories(self, username: str) -> list[dict[str, Any]]:
        return self._get_json(f"/users/{username}/repos?per_page=100&sort=updated")

    def _get_json(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            raise GitHubAPIError("Não foi possível carregar os dados do GitHub agora.") from error
