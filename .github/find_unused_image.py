import argparse
from pathlib import Path
from typing import Optional

import yaml


def find_unused_media(img_path: Optional[Path] = None, dry_run: bool = False) -> None:
    # load mkdocs.yml
    file = Path("mkdocs.yml")
    with file.open(mode="r", encoding="utf-8") as f:
        # remove all !! pairs from the yaml file
        data = f.read()
        data = data.replace("!!", "")
        config = yaml.safe_load(data)

    docs_dir = Path.cwd() / Path(config.get("docs_dir", "docs"))
    attachment_folder = config.get("extra", {}).get("attachments")
    print(f"Using docs directory: {attachment_folder}")
    if attachment_folder and isinstance(attachment_folder, dict):
        attachment_folder = attachment_folder.get("folder")
    if not attachment_folder and img_path:
        attachment_folder = img_path
    elif not attachment_folder:
        raise ValueError("No attachment folder found in mkdocs.yml or provided as argument.")
    assets_dir = Path(docs_dir, attachment_folder)
    print(f"Looking for unused images in {assets_dir}...")
    if img_path:
        assets_dir = img_path

    images = [
        file
        for file in assets_dir.rglob("*")
        if file.is_file() and file.suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg"}
    ]
    md_files = [file for file in docs_dir.rglob("*.md") if file.is_file()]

    # Search for images in markdown files

    used_images = []

    for md_file in md_files:
        file_path = Path(md_file)
        for image in images:
            with file_path.open("r", encoding="utf-8") as f:
                if image.name in f.read():
                    used_images.append(image)

    # compare the two lists
    unused_images = [image for image in images if image not in used_images]

    # delete unused images

    if unused_images:
        print(f"Found {len(unused_images)} unused images in {assets_dir}. Deleting...")
        for image in unused_images:
            if not dry_run:
                print(image)
                Path(image).unlink()
            else:
                print(f"Would delete {image}")
    else:
        print(f"Found no unused images in {assets_dir}.")


if __name__ == "__main__":
    # use argparse to get the path to the assets folder
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to the assets folder")
    parser.add_argument("--dry-run", action="store_true", help="Do not delete unused images")
    args = parser.parse_args()
    path = Path(args.path) if args.path else None
    find_unused_media(img_path=path, dry_run=args.dry_run)
