import os
from zipfile import ZipFile
import shutil


def kaggle(token_path: str, datasets=None, copy=True):
    root_dir = "/root/.kaggle"
    file_name = "kaggle.json"
    file_loc = os.path.join(root_dir, file_name)

    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)

    if copy:
        shutil.copy(token_path, root_dir)
        status = "copied"
    else:
        shutil.move(token_path, root_dir)
        status = "moved"

    os.chmod(file_loc, 600)
    print(f"'kaggle.json' file have been {status} to {file_loc}!")

    if datasets is not None:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()

        if type(datasets) == str:
            datasets = [datasets]

        for dataset in datasets:
            api.dataset_download_cli(dataset)

        print(f"\nDataset has been successfully downloaded!")


def unzip(path: str, output_dir: str):
    with ZipFile(path, "r") as zf:
        zf.extractall(output_dir)

    print(f"'{path}' has been extracted!")


def ws_setup(ws_name: str, data_origins: list):
    loc = os.getcwd()
    ws_path = os.path.join(loc, ws_name)

    if not os.path.isdir(ws_path):
        os.mkdir(ws_path)
    else:
        raise Exception(f'"{ws_name}" directory already exists!')

    for data in data_origins:
        shutil.move(data, ws_path)

    os.chdir(ws_path)

    print(f'current workspace directory "{os.getcwd()}"')
