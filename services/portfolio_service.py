from __future__ import annotations

from collections import Counter
from typing import Any

from repositories.github_repository import GitHubAPIError, GitHubRepository


class PortfolioService:
    def __init__(self, repository: GitHubRepository | None = None) -> None:
        self.repository = repository or GitHubRepository()

    def build_portfolio(self, username: str) -> dict[str, Any]:
        try:
            profile = self.repository.get_user_profile(username)
            repositories = self.repository.get_user_repositories(username)
        except GitHubAPIError:
            return self._fallback_portfolio(username)

        visible_repositories = [repo for repo in repositories if not repo.get("fork")]
        featured_repositories = sorted(
            visible_repositories,
            key=lambda repo: (repo.get("stargazers_count", 0), repo.get("pushed_at", "")),
            reverse=True,
        )[:6]

        languages = Counter(
            repo.get("language")
            for repo in visible_repositories
            if repo.get("language")
        )

        top_languages = [language for language, _ in languages.most_common(4)]
        total_stars = sum(repo.get("stargazers_count", 0) for repo in visible_repositories)
        total_forks = sum(repo.get("forks_count", 0) for repo in visible_repositories)

        return {
            "profile": {
                "name": profile.get("name") or username,
                "username": profile.get("login") or username,
                "bio": (profile.get("bio") or "Construindo soluções web com foco em evolução constante.").strip(),
                "avatar_url": profile.get("avatar_url"),
                "location": profile.get("location") or "Brasil",
                "blog": self._normalize_link(profile.get("blog")),
                "github_url": profile.get("html_url") or f"https://github.com/{username}",
                "followers": profile.get("followers", 0),
                "following": profile.get("following", 0),
                "public_repos": profile.get("public_repos", len(visible_repositories)),
                "top_languages": top_languages,
                "summary": self._build_summary(top_languages),
            },
            "stats": {
                "projects": len(visible_repositories),
                "stars": total_stars,
                "forks": total_forks,
                "followers": profile.get("followers", 0),
            },
            "projects": [self._serialize_repository(repo) for repo in featured_repositories],
            "all_projects_url": f"https://github.com/{username}?tab=repositories",
            "has_error": False,
        }

    def _serialize_repository(self, repo: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": repo.get("name"),
            "description": repo.get("description") or "Projeto publicado no GitHub sem descrição cadastrada.",
            "language": repo.get("language") or "Em evolução",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "url": repo.get("html_url"),
            "homepage": self._normalize_link(repo.get("homepage")),
            "updated_at": self._format_date(repo.get("pushed_at") or repo.get("updated_at")),
        }

    def _build_summary(self, top_languages: list[str]) -> str:
        if not top_languages:
            return "Projetos selecionados diretamente do GitHub com foco em evolução contínua."

        if len(top_languages) == 1:
            return f"Projetos com maior presença em {top_languages[0]}."

        featured_stack = ", ".join(top_languages[:-1]) + f" e {top_languages[-1]}"
        return f"Projetos com maior presença em {featured_stack}."

    def _fallback_portfolio(self, username: str) -> dict[str, Any]:
        return {
            "profile": {
                "name": "Miguel Antonio",
                "username": username,
                "bio": "Buscando cada dia mais conhecimento na área de programação.",
                "avatar_url": "https://avatars.githubusercontent.com/u/106715490?v=4",
                "location": "Brasil",
                "blog": None,
                "github_url": f"https://github.com/{username}",
                "followers": 7,
                "following": 9,
                "public_repos": 9,
                "top_languages": ["HTML", "Python", "CSS"],
                "summary": "Projetos publicados diretamente do GitHub com foco em front-end e aplicações web.",
            },
            "stats": {
                "projects": 9,
                "stars": 2,
                "forks": 1,
                "followers": 7,
            },
            "projects": [
                {
                    "name": "PI",
                    "description": "Meu PI sobre Gestão de Investimentos.",
                    "language": "Python",
                    "stars": 0,
                    "forks": 1,
                    "url": f"https://github.com/{username}/PI",
                    "homepage": None,
                    "updated_at": "08 dez 2025",
                },
                {
                    "name": "Desenvolvimento-Web",
                    "description": "Exercícios de desenvolvimento web.",
                    "language": "HTML",
                    "stars": 0,
                    "forks": 0,
                    "url": f"https://github.com/{username}/Desenvolvimento-Web",
                    "homepage": None,
                    "updated_at": "12 fev 2026",
                },
                {
                    "name": "projeto-android",
                    "description": "Projeto Android criado no Curso de HTML e CSS.",
                    "language": "HTML",
                    "stars": 1,
                    "forks": 0,
                    "url": f"https://github.com/{username}/projeto-android",
                    "homepage": None,
                    "updated_at": "21 mar 2023",
                },
            ],
            "all_projects_url": f"https://github.com/{username}?tab=repositories",
            "has_error": True,
        }

    def _format_date(self, value: str | None) -> str:
        if not value:
            return "Atualizado recentemente"

        months = {
            "01": "jan",
            "02": "fev",
            "03": "mar",
            "04": "abr",
            "05": "mai",
            "06": "jun",
            "07": "jul",
            "08": "ago",
            "09": "set",
            "10": "out",
            "11": "nov",
            "12": "dez",
        }

        date_part = value.split("T", maxsplit=1)[0]
        year, month, day = date_part.split("-")
        return f"{day} {months.get(month, month)} {year}"

    def _normalize_link(self, link: str | None) -> str | None:
        if not link:
            return None

        if link.startswith(("http://", "https://")):
            return link

        return f"https://{link}"
