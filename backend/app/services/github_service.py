"""
GitHub Integration Service
==========================
Service for fetching code from GitHub repositories.
Supports both public repos and authenticated access via personal access tokens.
"""

import base64
import logging
import re
from dataclasses import dataclass
from typing import Optional

import httpx

logger = logging.getLogger("ai_sdlc_copilot")


@dataclass
class GitHubFile:
    """Represents a file fetched from GitHub."""

    path: str
    name: str
    content: str
    sha: str
    size: int
    url: str


@dataclass
class RepoInfo:
    """Basic repository information."""

    owner: str
    repo: str
    default_branch: str
    description: str | None
    language: str | None
    private: bool


class GitHubServiceError(Exception):
    """Custom exception for GitHub service errors."""

    pass


class GitHubService:
    """
    Service for interacting with GitHub repositories.

    Supports:
    - Fetching repository information
    - Listing files in a directory
    - Fetching file contents
    - Searching for files by pattern
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str | None = None):
        """
        Initialize GitHub service.

        Args:
            token: Optional GitHub personal access token for private repos
                   or higher rate limits
        """
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-SDLC-Copilot",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    @staticmethod
    def parse_github_url(url: str) -> tuple[str, str]:
        """
        Parse a GitHub URL to extract owner and repo name.

        Supports formats:
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        - https://github.com/owner/repo/tree/branch/path
        - github.com/owner/repo
        - owner/repo

        Args:
            url: GitHub URL or owner/repo string

        Returns:
            Tuple of (owner, repo)

        Raises:
            GitHubServiceError: If URL format is invalid
        """
        # Try different patterns
        patterns = [
            # Full URL with optional .git
            r"(?:https?://)?github\.com/([^/]+)/([^/\.]+)(?:\.git)?(?:/.*)?$",
            # Simple owner/repo format
            r"^([^/]+)/([^/]+)$",
        ]

        for pattern in patterns:
            match = re.match(pattern, url.strip())
            if match:
                return match.group(1), match.group(2)

        raise GitHubServiceError(
            f"Invalid GitHub URL format: {url}. "
            "Expected format: 'owner/repo' or 'https://github.com/owner/repo'"
        )

    async def get_repo_info(self, owner: str, repo: str) -> RepoInfo:
        """
        Get repository information.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            RepoInfo object with repository details
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}",
                headers=self.headers,
            )

            if response.status_code == 404:
                raise GitHubServiceError(
                    f"Repository not found: {owner}/{repo}. "
                    "Make sure the repository exists and is public (or provide a token for private repos)."
                )
            elif response.status_code == 403:
                raise GitHubServiceError(
                    "GitHub API rate limit exceeded. Please provide a GitHub token."
                )
            elif response.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )

            data = response.json()
            return RepoInfo(
                owner=owner,
                repo=repo,
                default_branch=data.get("default_branch", "main"),
                description=data.get("description"),
                language=data.get("language"),
                private=data.get("private", False),
            )

    async def list_directory(
        self,
        owner: str,
        repo: str,
        path: str = "",
        branch: str | None = None,
    ) -> list[dict]:
        """
        List contents of a directory in the repository.

        Args:
            owner: Repository owner
            repo: Repository name
            path: Path to directory (empty for root)
            branch: Branch name (uses default branch if not specified)

        Returns:
            List of file/directory info dicts
        """
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
            params = {}
            if branch:
                params["ref"] = branch

            response = await client.get(url, headers=self.headers, params=params)

            if response.status_code == 404:
                raise GitHubServiceError(f"Path not found: {path}")
            elif response.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )

            return response.json()

    async def get_file_content(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str | None = None,
    ) -> GitHubFile:
        """
        Get the content of a file from the repository.

        Args:
            owner: Repository owner
            repo: Repository name
            path: Path to the file
            branch: Branch name (uses default branch if not specified)

        Returns:
            GitHubFile object with file content
        """
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
            params = {}
            if branch:
                params["ref"] = branch

            response = await client.get(url, headers=self.headers, params=params)

            if response.status_code == 404:
                raise GitHubServiceError(f"File not found: {path}")
            elif response.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )

            data = response.json()

            if data.get("type") != "file":
                raise GitHubServiceError(f"Path is not a file: {path}")

            # Decode base64 content
            content = base64.b64decode(data["content"]).decode("utf-8")

            return GitHubFile(
                path=data["path"],
                name=data["name"],
                content=content,
                sha=data["sha"],
                size=data["size"],
                url=data["html_url"],
            )

    async def get_multiple_files(
        self,
        owner: str,
        repo: str,
        paths: list[str],
        branch: str | None = None,
    ) -> list[GitHubFile]:
        """
        Get contents of multiple files.

        Args:
            owner: Repository owner
            repo: Repository name
            paths: List of file paths
            branch: Branch name

        Returns:
            List of GitHubFile objects
        """
        files = []
        for path in paths:
            try:
                file = await self.get_file_content(owner, repo, path, branch)
                files.append(file)
            except GitHubServiceError as e:
                logger.warning(f"Failed to fetch {path}: {e}")
        return files

    async def find_python_files(
        self,
        owner: str,
        repo: str,
        path: str = "",
        branch: str | None = None,
        max_files: int = 50,
    ) -> list[str]:
        """
        Recursively find all Python files in a directory.

        Args:
            owner: Repository owner
            repo: Repository name
            path: Starting path (empty for root)
            branch: Branch name
            max_files: Maximum number of files to return

        Returns:
            List of Python file paths
        """
        python_files = []

        async def _scan_directory(dir_path: str):
            if len(python_files) >= max_files:
                return

            try:
                contents = await self.list_directory(owner, repo, dir_path, branch)

                for item in contents:
                    if len(python_files) >= max_files:
                        break

                    if item["type"] == "file" and item["name"].endswith(".py"):
                        python_files.append(item["path"])
                    elif item["type"] == "dir":
                        # Skip common non-source directories
                        if item["name"] not in {
                            "__pycache__",
                            ".git",
                            "node_modules",
                            "venv",
                            ".venv",
                            "env",
                            ".env",
                            "dist",
                            "build",
                            ".tox",
                            ".pytest_cache",
                        }:
                            await _scan_directory(item["path"])
            except GitHubServiceError:
                pass  # Skip directories we can't access

        await _scan_directory(path)
        return python_files

    async def search_code(
        self,
        owner: str,
        repo: str,
        query: str,
        extension: str = "py",
        max_results: int = 10,
    ) -> list[dict]:
        """
        Search for code in the repository using GitHub code search.

        Note: Requires authentication for better results.

        Args:
            owner: Repository owner
            repo: Repository name
            query: Search query
            extension: File extension to filter by
            max_results: Maximum number of results

        Returns:
            List of search result items
        """
        async with httpx.AsyncClient() as client:
            search_query = f"{query} repo:{owner}/{repo} extension:{extension}"
            url = f"{self.BASE_URL}/search/code"
            params = {"q": search_query, "per_page": min(max_results, 100)}

            response = await client.get(url, headers=self.headers, params=params)

            if response.status_code == 403:
                raise GitHubServiceError(
                    "GitHub code search requires authentication. Please provide a token."
                )
            elif response.status_code != 200:
                raise GitHubServiceError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )

            data = response.json()
            return data.get("items", [])[:max_results]


# Singleton instance
_github_service: GitHubService | None = None


def get_github_service(token: str | None = None) -> GitHubService:
    """
    Get or create the GitHub service instance.

    Args:
        token: Optional GitHub token

    Returns:
        GitHubService instance
    """
    global _github_service
    if _github_service is None or token:
        _github_service = GitHubService(token)
    return _github_service
