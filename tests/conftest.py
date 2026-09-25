"""Shared pytest fixtures for the registration test suite.

Add reusable fixtures here as needed for Section 7 of the assignment
(e.g., a fixture providing representative student data used by multiple
tests, and a yield-based fixture that sets up and cleans up a temporary
resource).
"""

# TODO: implement your fixtures here.
import pytest


@pytest.fixture
def valid_registration_data():
    """
    Reusable valid registration data.

    This fixture is intentionally used by multiple tests
    so that common setup data is not duplicated.
    """
    return {
        "current_credits": 12,
        "course_credits": 3,
        "prerequisite_met": True,
    }


@pytest.fixture
def temporary_registration_file(tmp_path):
    """
    Yield-based fixture demonstrating setup and cleanup
    of a temporary resource.
    """
    temp_file = tmp_path / "registration_test_data.txt"

    # Setup
    temp_file.write_text(
        "temporary registration test data",
        encoding="utf-8"
    )

    try:
        yield temp_file
    finally:
        # Cleanup runs even when the test fails.
        if temp_file.exists():
            temp_file.unlink()


