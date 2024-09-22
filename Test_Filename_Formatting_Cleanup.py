import os
import pytest
import shutil
from Filename_Formatting_Cleanup import rename_file


@pytest.fixture(scope="function")
def setup_test_directory(tmpdir):
    """Fixture to set up a temporary directory for testing."""

    # Create a test directory
    test_dir = tmpdir.mkdir("test_monitor_dir")

    # List of test files with various naming conventions
    test_files = [
        "test_file_1.txt",
        "another___file.doc",
        "too_many______underscores.txt",
        "_leading_underscores.txt",
        "trailing_underscores_.txt",
        "____both_leading_and_trailing____underscores.txt",
        "Hello__World.txt",
        "random.file.name.jpg",
        "a random file.txt",
        "Multiple---Hyphens-and___underscores.txt",
        "Mixed_CAPS_and_normal.doc",
        "file@with!invalid#chars$.txt",
        "hello-in_the_middle.txt",
        "TEST_FILE_WITH___MIXED__underscores.txt",
        "____leading_and_trailing_underscores___.txt",
        "file name with spaces.txt",
        "three ___ underscores_with_spaces.txt",
        "two __ underscores_with_spaces.txt",
        "hyphens with - spaces",
        "mixed capitals ACC",
    ]

    # Create the files in the directory
    for file_name in test_files:
        test_dir.join(file_name).write("")

    # Provide the directory and file list for the test
    yield test_dir, test_files

    # Cleanup after test
    shutil.rmtree(test_dir)


def test_rename_files(setup_test_directory):
    """Test the rename_file function on different types of files."""

    test_dir, test_files = setup_test_directory

    # Expected results mapping original file names to their expected renamed versions
    expected_results = {
        "test_file_1.txt": "Test_File_1.txt",
        "another___file.doc": "Another___File.doc",
        "too_many______underscores.txt": "Too_Many_Underscores.txt",
        "_leading_underscores.txt": "Leading_Underscores.txt",
        "trailing_underscores_.txt": "Trailing_Underscores.txt",
        "____both_leading_and_trailing____underscores.txt": "Both_Leading_and_Trailing_Underscores.txt",
        "Hello__World.txt": "Hello__World.txt",
        "random.file.name.jpg": "Random_File_Name.jpg",
        "a random file.txt": "A_Random_File.txt",
        "Multiple---Hyphens-and___underscores.txt": "Multiple-Hyphens-and___Underscores.txt",
        "Mixed_CAPS_and_normal.doc": "Mixed_CAPS_and_Normal.doc",
        "file@with!invalid#chars$.txt": "Filewithinvalidchars.txt",
        "hello-in_the_middle.txt": "Hello-in_the_Middle.txt",
        "TEST_FILE_WITH___MIXED__underscores.txt": "TEST_FILE_WITH___MIXED__Underscores.txt",
        "____leading_and_trailing_underscores___.txt": "Leading_and_Trailing_Underscores.txt",
        "file name with spaces.txt": "File_Name_with_Spaces.txt",
        "three ___ underscores_with_spaces.txt": "Three___Underscores_with_Spaces.txt",
        "two __ underscores_with_spaces.txt": "Two__Underscores_with_Spaces.txt",
        "hyphens with - spaces": "Hyphens_with-Spaces",
        "mixed capitals ACC": "Mixed_Capitals_ACC",
    }

    # Test renaming files
    for file_name in test_files:
        # Call rename_file
        new_file_name = rename_file(file_name, str(test_dir))
        assert (
            new_file_name == expected_results[file_name]
        ), f"Expected {expected_results[file_name]} but got {new_file_name} for original file {file_name}"
        assert os.path.exists(
            os.path.join(str(test_dir), new_file_name)
        ), f"File {new_file_name} was not found after renaming."

    print("All tests passed!")
