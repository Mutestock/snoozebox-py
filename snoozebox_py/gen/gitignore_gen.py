import requests
from utils.pathing import get_relative_project_root_directory

GITIGNORE_IO_URL: str = "https://www.toptal.com/developers/gitignore/api/python"


def write_git_ignore(config) -> None:
    file_writer = open(get_relative_project_root_directory(config) + "/.gitignore", "w")
    print("fetching https://www.toptal.com/developers/gitignore/api/python ...")
    res = requests.get("https://www.toptal.com/developers/gitignore/api/python")
    to_ignore = ["data", "logs", res.text]
    file_writer.write("\n".join(to_ignore))
    file_writer.close()
