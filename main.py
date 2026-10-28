import requests


def get_repos(username: str) -> list[dict]:
    url = f"https://api.github.com/users/{username}/repos"

    page = 1
    repositories = []

    while True:
        response = requests.get(
            url,
            params={"per_page": 100, "page": page, "sort": "updated"},
            timeout=10,
        )
        response.raise_for_status()

        page_repositories = response.json()
        if not page_repositories:
            break

        repositories.extend(page_repositories)
        page += 1

    return repositories
