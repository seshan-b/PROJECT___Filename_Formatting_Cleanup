import os
import re
import logging
import time
import sys

# Global stop flag to control the monitoring loop
stop_flag = False

# Constants
TRIVIAL_WORDS = {
    "a",
    "an",
    "and",
    "at",
    "by",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}

# Log file configuration
log_file = "Filename_Formatting_Cleanup__Logs.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_file_rename(original_name, new_name):
    """Log the renaming of a file."""
    logging.info(f"File renamed from '{original_name}' to '{new_name}'")


def replace_underscores(match):
    underscores = match.group(0)
    if len(underscores) == 3:
        return "___"  # Preserve exactly 3 underscores
    elif len(underscores) >= 4:
        return "_"   # Reduce 4 or more underscores to 1
    return underscores  # Keep 1 or 2 underscores unchanged


def clean_file_name(name):
    # First handle special characters and spaces
    name = name.replace(".", "_")
    name = name.strip("_")  # Remove leading/trailing underscores
    name = re.sub(r"\s+", "_", name)  # Replace spaces with single underscore

    # Replace multiple (4 or more) underscores with single underscore
    name = re.sub(r"_{4,}", "_", name)

    # Clean up other characters
    name = re.sub(r"_?-_?", "-", name)  # Clean up around hyphens
    name = re.sub(r"-{2,}", "-", name)  # Reduce multiple hyphens
    name = re.sub(r"\s*-\s*", "-", name)  # Clean spaces around hyphens
    name = re.sub(r"[^a-zA-Z0-9_\-]", "", name)

    # Handle numbered sections
    match = re.search(r"\((\d+)\)", name)
    if match:
        number = match.group(1)
        name = re.sub(r"\(\d+\)", f"-{number}", name)

    return name


def title_case_filename(name):
    # Split by underscores and hyphens, preserve separators
    parts = re.split(r"([_-]+)", name)
    result = []
    first_word = True
    for part in parts:
        if re.fullmatch(r"[_-]+", part):
            result.append(part)
        elif part.isupper():
            result.append(part)
        elif part:
            # Lowercase trivial words unless first word
            if part.lower() in TRIVIAL_WORDS and not first_word:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
            first_word = False
    return "".join(result)


def rename_file(file_name: str, directory: str) -> str:
    base_name, ext = os.path.splitext(file_name)
    base_name = clean_file_name(base_name)
    base_name = title_case_filename(base_name)
    ext = ext.upper()  # Convert all extensions to upper case
    new_file_name = f"{base_name}{ext}"
    old_path = os.path.join(directory, file_name)
    new_path = os.path.join(directory, new_file_name)
    os.rename(old_path, new_path)
    log_file_rename(file_name, new_file_name)
    print(f"Renamed: {file_name} -> {new_file_name}")
    return new_file_name


# def monitor_and_rename(folder_to_monitor):
#     """Monitor the folder and rename files based on rules."""
#     while not stop_flag:
#         try:
#             for file_name in os.listdir(folder_to_monitor):
#                 full_path = os.path.join(folder_to_monitor, file_name)
#                 if os.path.isfile(full_path):
#                     # Rename the file
#                     new_file_name = rename_file(file_name, folder_to_monitor)
#                     if new_file_name != file_name:
#                         new_path = os.path.join(folder_to_monitor, new_file_name)
#                         print(f"Renamed: {full_path} -> {new_path}")
#         except OSError as e:
#             logging.error(f"File operation error: {str(e)}")
#         except Exception as e:
#             logging.error(f"Unexpected error: {str(e)}")
#         finally:
#             time.sleep(5)  # Wait before checking again


if __name__ == "__main__":
    folder_to_monitor = sys.argv[1] if len(sys.argv) > 1 else None
    if folder_to_monitor:
        try:
            monitor_and_rename(folder_to_monitor)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
        finally:
            logging.info("Script terminated.")
    else:
        print("Please provide a folder to monitor.")
