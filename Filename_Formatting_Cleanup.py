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
    """Replace sequences of underscores based on specific rules."""
    underscores = match.group(0)
    if len(underscores) == 3:
        return "___"  # Preserve exactly 3 underscores
    elif len(underscores) > 3:
        return "_"  # Reduce 4 or more underscores to 1
    return underscores  # Keep 1 or 2 underscores unchanged


def clean_file_name(name):
    """
    Cleans the file name by removing invalid characters, replacing periods with underscores,
    trimming leading/trailing underscores, and normalizing spaces and hyphens.
    """
    # Replace periods with underscores
    name = name.replace(".", "_")
    # Remove leading and trailing underscores
    name = name.strip("_")
    # Replace spaces around exactly three underscores with no spaces
    name = re.sub(r"\s*___\s*", "___", name)
    # Replace spaces around exactly two underscores with no spaces
    name = re.sub(r"\s*__\s*", "__", name)
    # Replace multiple consecutive spaces with a single underscore
    name = re.sub(r" +", "_", name)
    # **Remove underscores around hyphens**
    name = re.sub(r"_?-_?", "-", name)
    # Reduce multiple consecutive hyphens to a single hyphen
    name = re.sub(r"-{2,}", "-", name)
    # Remove invalid characters (anything that is not alphanumeric, underscore, or hyphen)
    name = re.sub(r"[^a-zA-Z0-9_\-]", "", name)
    # Remove spaces around hyphens
    name = re.sub(r"\s*-\s*", "-", name)
    return name


def capitalize_words(name):
    """Capitalizes words in the file name according to rules for trivial words."""
    # Split by sequences of underscores or hyphens
    words = re.split(r"([_-]+)", name)
    result = []

    for i, word in enumerate(words):
        if not word:
            continue  # Skip empty strings
        if re.fullmatch(r"[_-]+", word):
            result.append(word)  # Keep separators as they are
        else:
            if word.isupper():
                result.append(word)  # Preserve fully capitalized words
            else:
                # Capitalize the word if it's not trivial or it's the first word
                if i == 0 or word.lower() not in TRIVIAL_WORDS:
                    result.append(word.capitalize())
                else:
                    result.append(word.lower())
    return "".join(result)


def rename_file(file_name: str, directory: str) -> str:
    """Rename a file according to specific formatting rules."""
    # Split the file name into base and extension
    base_name, ext = os.path.splitext(file_name)

    # Clean the base name
    base_name = clean_file_name(base_name)

    # Replace sequences of underscores based on specific rules
    base_name = re.sub(r"_+", replace_underscores, base_name)

    # Capitalize words in the base name
    base_name = capitalize_words(base_name)

    # Combine with extension to form the new file name
    new_file_name = f"{base_name}{ext}"
    old_path = os.path.join(directory, file_name)
    new_path = os.path.join(directory, new_file_name)

    # Rename the file in the filesystem
    os.rename(old_path, new_path)

    # Log the renaming action
    log_file_rename(file_name, new_file_name)

    print(f"Renamed: {file_name} -> {new_file_name}")
    return new_file_name


def monitor_and_rename(folder_to_monitor):
    """Monitor the folder and rename files based on rules."""
    while not stop_flag:
        try:
            for file_name in os.listdir(folder_to_monitor):
                full_path = os.path.join(folder_to_monitor, file_name)
                if os.path.isfile(full_path):
                    # Rename the file
                    new_file_name = rename_file(file_name, folder_to_monitor)
                    if new_file_name != file_name:
                        new_path = os.path.join(folder_to_monitor, new_file_name)
                        print(f"Renamed: {full_path} -> {new_path}")
        except OSError as e:
            logging.error(f"File operation error: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
        finally:
            time.sleep(5)  # Wait before checking again


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
