import glob
import os
import re
from datetime import datetime

from server.config import settings


def get_migration_file_name():
    files = glob.glob("alembic/versions/*.py")
    files = [os.path.basename(file) for file in files]

    current_time = datetime.utcnow().strftime("%d_%m_%Y_%H_%M_%S")
    revision = 0
    if len(files) > 0:
        versions = []
        for file in files:
            versions.append(re.search("V" + "(.*)" + "____", file).group(1))
        versions.sort()
        latest_version = versions[-1:][0]
        revision = int(latest_version) + 1
    return f"{revision}____{current_time}"


if __name__ == "__main__":
    file_name = get_migration_file_name()
    command = f"alembic revision --autogenerate -m {file_name}"

    if settings.FASTAPI_CONFIG != "production":
        os.system(command)

    os.system("alembic upgrade head")
