import os  # Module for interacting with the operating system
import sys  # Module for accessing command-line arguments
import time  # Module for adding delays between operations
import re  # Module for working with regular expressions
import logging  # Module for logging messages

# Global stop flag to control the infinite loop in the monitoring function
stop_flag = False

# Configure logging to log messages into a file with a specific format
log_file = "Filename_Formatting_Cleanup__Logs.txt"  # Log file name
logging.basicConfig(
    filename=log_file,  # Specify the log file
    level=logging.INFO,  # Log level set to INFO (logs informational messages)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)

logging.info("Script started. Monitoring initiated.")  # Log the start of the script

# Check if a folder path is provided as a command-line argument
if len(sys.argv) > 1:
    folder_to_monitor = sys.argv[1]  # Assign the first argument to folder_to_monitor
else:
    # If no folder path is provided, print an error message and log the error
    print("Please provide the folder path to monitor.")
    logging.error("No folder path provided. Exiting the script.")
    sys.exit(1)  # Exit the script with status code 1 (indicating an error)

# Regular expression pattern to replace any character not in A-Z, a-z, 0-9, _, - with an underscore
pattern = re.compile(r"[^a-zA-Z0-9_\-]")

# Set of trivial words that should not be capitalized unless they are the first or last word
trivial_words = {
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


def custom_title_case(name):
    """
    Convert a string to title case, capitalizing trivial words only if they are
    the first or last word in the string. Sequences of multiple capital letters
    (e.g., 'ACC') are left unchanged.
    """
    words = name.split("_")  # Split the name by underscores into words
    title_cased_words = []  # Initialize a list to store title-cased words

    for i, word in enumerate(words):
        sub_words = word.split()  # Split by spaces to handle multi-word blocks
        sub_words_cased = []  # Initialize a list to store cased sub-words

        for j, sub_word in enumerate(sub_words):  # Iterate over sub-words
            # Handle hyphenated words
            hyphenated_parts = sub_word.split("-")
            for k, part in enumerate(hyphenated_parts):
                if re.match(r"[A-Z]{2,}", part):  # Check if the part is in all caps
                    hyphenated_parts[k] = part  # Keep all caps as they are
                elif (
                    (i == 0 and j == 0 and k == 0)
                    or (
                        i == len(words) - 1
                        and j == len(sub_words) - 1
                        and k == len(hyphenated_parts) - 1
                    )
                    or part.lower() not in trivial_words
                ):
                    hyphenated_parts[k] = (
                        part.capitalize()
                    )  # Capitalize important parts
                else:
                    hyphenated_parts[k] = part.lower()  # Keep trivial parts lowercase

            sub_words_cased.append(
                "-".join(hyphenated_parts)
            )  # Rejoin hyphenated parts

        title_cased_words.append(
            " ".join(sub_words_cased)
        )  # Join sub-words back together with spaces

    return "_".join(
        title_cased_words
    )  # Join the title-cased words back together with underscores


def log_file_rename(original_name, new_name, operation="rename"):
    """
    Log the file renaming operation.

    Parameters:
    - original_name: The original file name.
    - new_name: The new file name after renaming.
    - operation: The type of operation, default is 'rename'.
    """
    if operation == "rename":
        logging.info(
            f"File name changed from '{original_name}' to '{new_name}'"
        )  # Log the renaming action


def rename_file(file_name):
    """
    Rename a file by applying title case rules, replacing spaces and invalid characters,
    and removing leading/trailing underscores or hyphens. The file extension remains unchanged.
    All leading/trailing underscores are removed. In-between underscores are preserved.
    """
    name, extension = os.path.splitext(
        file_name
    )  # Split the file name from its extension

    name = custom_title_case(name)  # Apply custom title casing to the file name

    # Handle hyphens with spaces around them by title-casing words around them
    name = re.sub(r"\s*-\s*", "-", name)

    # Replace invalid characters with underscores
    new_name = pattern.sub("_", name)

    # Replace multiple hyphens with a single hyphen, but retain hyphen as a separator
    new_name = re.sub(r"-+", "-", new_name)

    # # Remove multiple underscores and strip leading/trailing underscores or hyphens
    # new_name = re.sub(r"_+", "_", new_name).strip("_-")

    # Always remove leading/trailing underscores or hyphens
    new_name = new_name.strip("_-")

    # If the file name changes, log the action
    if new_name + extension != file_name:
        log_file_rename(file_name, new_name + extension)

    return new_name + extension  # Return the new file name with its original extension


def monitor_and_rename():
    """
    Monitor the specified folder for files and rename them according to the rules
    defined in the rename_file function. The loop runs continuously until stop_flag is set.
    """
    while not stop_flag:  # Run the loop until stop_flag is True
        try:
            for file_name in os.listdir(
                folder_to_monitor
            ):  # List all files in the folder
                original_file_path = os.path.join(
                    folder_to_monitor, file_name
                )  # Get the full path of the file
                if os.path.isfile(
                    original_file_path
                ):  # Ensure it's a file (not a directory)
                    print(f"Found file: {original_file_path}")
                    new_file_name = rename_file(
                        file_name
                    )  # Get the new file name after renaming
                    new_file_path = os.path.join(
                        folder_to_monitor, new_file_name
                    )  # Create new file path

                    if new_file_name != file_name:  # If the file name has changed
                        print(f"Renaming file: {original_file_path} -> {new_file_path}")
                        os.rename(original_file_path, new_file_path)  # Rename the file
                        print(f"File renamed: {original_file_path} -> {new_file_path}")
                    else:
                        print(f"No renaming needed for: {file_name}")
        except OSError as e:
            logging.error(
                f"File operation error: {str(e)}"
            )  # Log file operation errors
        except Exception as e:
            logging.error(
                f"Unexpected error: {str(e)}"
            )  # Log any other unexpected errors
        finally:
            time.sleep(5)  # Wait for 5 seconds before checking the folder again


# Main execution block
if __name__ == "__main__":
    try:
        monitor_and_rename()  # Start monitoring and renaming files
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")  # Log any error that occurs
    finally:
        logging.info("Script terminated.")  # Log that the script has terminated
