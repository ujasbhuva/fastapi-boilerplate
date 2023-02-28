import argparse
import glob
import os
import re
from datetime import datetime

from server.config import settings

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--downgrade", help="Downgrade")
args = parser.parse_args()


def get_migration_files():
    files = glob.glob("alembic/versions/*.py")
    files = [os.path.basename(file) for file in files]

    versions = []
    for file in files:
        versions.append(int(re.search("V" + "(.*)" + "__", file).group(1)))
    versions.sort()

    sorted_files = []
    for i in versions:
        for j in files:
            if j.startswith(f"V{i}__"):
                sorted_files.append(j)

    return sorted_files


def get_migration_file_name():
    files = get_migration_files()
    current_time = datetime.utcnow().strftime("%d_%m_%y_%H_%M")
    revision = 0
    if len(files) > 0:
        latest_version = int(re.search("V" + "(.*)" + "__", files[-1:][0]).group(1))
        revision = latest_version + 1
    return f"{revision}__{current_time}"


if __name__ == "__main__":
    "alembic downgrade"
    if args.downgrade:
        downgrade_count = int(args.downgrade)
        files = get_migration_files()

        if downgrade_count < len(files):
            command = f"alembic downgrade -{downgrade_count}"
            os.system(command)
            remove_files = files[::-1][:downgrade_count]
            for remove_file in remove_files:
                os.remove("alembic/versions/" + remove_file)
        else:
            print(
                "Cannot perform operation as downgrade count is more than available versions"
            )

    else:
        if settings.FASTAPI_CONFIG != "production":
            file_name = get_migration_file_name()
            command = f"alembic revision --autogenerate -m {file_name}"
            os.system(command)

        os.system("alembic upgrade head")
