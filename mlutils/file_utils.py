try:
    import os
    import shutil
    from zipfile import ZipFile
except Exception:
    raise Exception(f'Try installing the required dependencies!')


def kaggle(origin_path: str, dataset_urls=None, copy=True):
    root_dir = "/root/.kaggle"
    file_name = "kaggle.json"
    file_loc = os.path.join(root_dir, file_name)

    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)

    if copy:
        shutil.copy(origin_path, root_dir)
    else:
        shutil.move(origin_path, root_dir)

    os.chmod(file_loc, 600)
    print(f"\n'kaggle.json' file has been copied to {file_loc}!")

    if dataset_urls is not None:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()

        for dataset in dataset_urls:
            api.dataset_download_cli(dataset)

        print(f"\nDataset has been successfully downloaded!")


def unzip(path: str):
    zip_ref = ZipFile(path, 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()

    print(f'\n\'{path}\' has been extracted!')


def ws_setup(ws_name: str, data_origins: list):
    loc = os.getcwd()
    ws_path = os.path.join(loc, ws_name)

    if os.path.isdir(ws_path):
        raise Exception(f'\'{ws_name}\' directory already exists!')
    else:
        os.mkdir(ws_path)

    for data in data_origins:
        shutil.move(data, ws_path)

    os.chdir(ws_path)

    print(f'\n current workspace directory \'{os.getcwd()}\'')
