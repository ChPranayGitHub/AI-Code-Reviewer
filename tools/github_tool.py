from git import Repo
import os

def clone_repo(repo_url):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    destination = os.path.join("repos", repo_name)

    if not os.path.exists(destination):
        Repo.clone_from(repo_url, destination)

    return destination