import os
import re
import logging
import time

# Global stop flag to control the monitoring loop
stop_flag = False

# Log file configuration to log events
log_file = "Filename_Formatting_Cleanup__Logs.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Set of trivial words that should not be capitalized unless first or last
trivial_words = {"a", "an", "and", "at", "by", "for", "in", "of", "on", "or", "the", "to", "with"}

# Function to capitalize words based on position
def capitalize_word(word, first, last):
    # Capitalize if it's the first/last word or not a trivial word
    if first or last or word.lower() not in trivial_words:
        return word.capitalize()
    # Otherwise return in lowercase
    return word.lower()

# Function to convert filenames to title case
def custom_title_case(name):
    """Convert filename string to title case, handling spaces, underscores, and hyphens."""
    # Split words by spaces or underscores
    words = re.split(r"[\s_]+", name)
    # Apply capitalization rules to each word
    return "_".join(
        " ".join(capitalize_word(part, i == 0, i == len(words) - 1)
                 for part in word.split("-"))
        for i, word in enumerate(words)
    )

# Function to log file renaming actions
def log_file_rename(original_name, new_name):
    """Log the renaming of a file."""
    logging.info(f"File renamed from '{original_name}' to '{new_name}'")

# Function to rename a file according to title case rules
def rename_file(file_name, folder_to_monitor):
    """Rename a file based on title case rules and other formatting."""
    # Split the file name and extension
    name, extension = os.path.splitext(file_name)
    # Apply custom title case to the name
    name = custom_title_case(name)
    # Replace spaces and periods with underscores
    name = re.sub(r"\s+", "_", name).replace(".", "_")
    # Remove invalid characters
    name = re.sub(r"[^a-zA-Z0-9_\-]", "", name)
    # Replace multiple hyphens with a single hyphen, and strip leading/trailing underscores
    name = re.sub(r"-+", "-", name).strip("_-")

    # Combine the modified name and extension
    new_name = name + extension

    # Get original and new file paths
    original_path = os.path.join(folder_to_monitor, file_name)
    new_path = os.path.join(folder_to_monitor, new_name)

    # If the name has changed, rename the file
    if new_name != file_name:
        os.rename(original_path, new_path)
        log_file_rename(file_name, new_name)

    return new_name

# Function to monitor a folder and rename files continuously
def monitor_and_rename(folder_to_monitor):
    """Monitor the folder and rename files based on rules."""
    # Loop until stop_flag is set to True
    while not stop_flag:
        try:
            # Loop through files in the folder
            for file_name in os.listdir(folder_to_monitor):
                # Get the full path of the file
                full_path = os.path.join(folder_to_monitor, file_name)
                # Ensure it's a file, not a directory
                if os.path.isfile(full_path):
                    # Rename the file
                    new_file_name = rename_file(file_name, folder_to_monitor)
                    new_path = os.path.join(folder_to_monitor, new_file_name)
                    # If the file name changed, print the action
                    if new_file_name != file_name:
                        print(f"Renamed: {full_path} -> {new_path}")
        except OSError as e:
            # Log any file operation errors
            logging.error(f"File operation error: {str(e)}")
        except Exception as e:
            # Log unexpected errors
            logging.error(f"Unexpected error: {str(e)}")
        finally:
            # Wait for 5 seconds before checking again
            time.sleep(5)

# Main function to start monitoring
if __name__ == "__main__":
    folder_to_monitor = sys.argv[1] if len(sys.argv) > 1 else None
    if folder_to_monitor:
        try:
            monitor_and_rename(folder_to_monitor)  # Start monitoring and renaming files
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")  # Log any errors
        finally:
            logging.info("Script terminated.")  # Log when the script terminates
    else:
        print("Please provide a folder to monitor.")
