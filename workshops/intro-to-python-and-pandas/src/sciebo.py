from pathlib import Path
import requests
from typing import Union
from tqdm import tqdm

def download_file(public_url, to_filename):
    """Downloads a file from a shared URL on Sciebo."""
    _make_parent_folders(to_filename)

    r = requests.get(public_url + "/download", stream=True)
    num_bytes = int(r.headers['Content-Length'])
    progress_bar = tqdm(desc=f"Downloading {to_filename}", unit='B', unit_scale=True, total=num_bytes)
    with open(to_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            progress_bar.update(len(chunk))


def download_folder(public_url, to_filename):
    """Downloads a folder from a shared URL on Sciebo."""
    _make_parent_folders(to_filename)
    
    r = requests.get(public_url + "/download", stream=True)
    progress_bar = tqdm()
    with open(to_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            progress_bar.update(len(chunk))


def download_from_sciebo(public_url, to_filename, is_file = True):
    """Wrapper function: Downloads a file or folder from a shared URL on Sciebo."""
    download_fun = download_file if is_file else download_folder
    download_fun(public_url=public_url, to_filename=to_filename)


def _make_parent_folders(path: Union[Path, str]) -> None:
    # Create the parent folders if a longer path was described
    path = Path(path)
    if len(path.parts) > 1:
        Path(to_filename).parent.mkdir(parents=True, exist_ok=True)