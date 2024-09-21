import os
import shutil
import pytest
from Filename_Formatting_Cleanup import rename_file, monitor_and_rename

# Fixture to set up a test directory and create test files
@pytest.fixture
def setup_test_directory():
    # Define a test directory
    test_dir = os.path.join(os.getcwd(), "Test_Files_in_Folder")

    # Clean the directory if it exists and create it fresh
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)

    # Create test file
    test_file = "another file.doc"
    open(os.path.join(test_dir, test_file), "a").close()  # Create the test file

    # Yield the test directory and file name for the test
    yield test_dir, test_file

    # Clean up the directory after the test is done
    shutil.rmtree(test_dir)

# Test function to check renaming of a single file
def test_rename_single_file(setup_test_directory):
    # Get the test directory and file from the fixture
    test_dir, test_file = setup_test_directory

    # Expected result after renaming
    expected_result = "Another_File.doc"

    # Rename the file
    new_file_name = rename_file(test_file, test_dir)
    new_path = os.path.join(test_dir, new_file_name)

    # Assert that the renaming matches the expected result
    assert new_file_name == expected_result, \
        f"Expected {expected_result} but got {new_file_name} for original file {test_file}"

    # Assert that the renamed file exists
    assert os.path.exists(new_path), f"File {new_file_name} was not found after renaming."

# Test function to check renaming and monitoring of multiple files
def test_monitor_and_rename(setup_test_directory, monkeypatch):
    # Get the test directory and file from the fixture
    test_dir, test_file = setup_test_directory

    # Expected result after renaming
    expected_result = "Another_File.doc"

    # Monkeypatch the stop_flag to stop after one iteration
    monkeypatch.setattr("Filename_Formatting_Cleanup.stop_flag", True)

    # Run the monitor and rename function with the test directory
    monitor_and_rename(test_dir)

    # Rename the file
    new_file_name = rename_file(test_file, test_dir)
    new_path = os.path.join(test_dir, new_file_name)

    # Assert that the renaming matches the expected result
    assert new_file_name == expected_result, \
        f"Expected {expected_result} but got {new_file_name} for original file {test_file}"

    # Assert that the renamed file exists
    assert os.path.exists(new_path), f"File {new_file_name} was not found after renaming."
