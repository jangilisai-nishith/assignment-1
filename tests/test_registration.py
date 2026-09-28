"""Test suite for src/registration.py.

This file is intentionally left for you to implement. See the assignment
handout for the required test-design work:

  - Section 4: Equivalence partitioning
  - Section 5: Boundary-value analysis
  - Section 6: Positive and negative testing with pytest
  - Section 7: Parametrization and fixtures
  - Section 8: Organize and demonstrate the test suite (markers, README)

`registration` is importable directly (see pyproject.toml's `pythonpath`
setting), e.g.:

    from registration import can_register, calculate_registration_fee
"""

# TODO: implement your tests here.
import pytest

from registration import can_register, calculate_registration_fee




@pytest.mark.unit
@pytest.mark.positive
def test_registration_allowed_for_typical_valid_student(
    valid_registration_data
):
    """
    A student with valid credits, valid course credits,
    and the prerequisite satisfied should be allowed
    to register.
    """
    assert can_register(**valid_registration_data) is True




@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_prerequisite_not_met(
    valid_registration_data
):
    """
    Registration must fail when the prerequisite
    has not been completed.
    """
    assert (
        can_register(
            valid_registration_data["current_credits"],
            valid_registration_data["course_credits"],
            False,
        )
        is False
    )




@pytest.mark.unit
@pytest.mark.boundary
@pytest.mark.parametrize(
    "current_credits, course_credits, expected",
    [
      
        (-1, 1, False),   
        (0, 1, True),     
        (1, 1, True),     

  
        (14, 1, True),    
        (15, 1, True),    
        (16, 1, False),   

        
        (10, 0, False),   # below lower boundary
        (10, 1, True),    # exact lower boundary
        (10, 2, True),    # just above lower boundary

       
        (10, 3, True),    # just below upper boundary
        (10, 4, True),    # exact upper boundary
        (10, 5, False),   # just above upper boundary

       
        (14, 3, True),    # resulting total = 17
        (14, 4, True),    # resulting total = 18
        (15, 4, False),   # resulting total = 19
    ],
)
def test_registration_boundary_values(
    current_credits,
    course_credits,
    expected,
):
    assert (
        can_register(
            current_credits,
            course_credits,
            True
        )
        is expected
    )




@pytest.mark.unit
@pytest.mark.negative
def test_registration_rejected_when_total_credits_exceed_18():
    """
    Both individual inputs are valid, but the resulting
    credit load would be 19, so registration must fail.
    """
    assert can_register(15, 4, True) is False


@pytest.mark.unit
@pytest.mark.positive
@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits, expected_fee",
    [
        (0, 0.0),
        (1, 100.0),

        
        (11, 1100.0),
        (12, 1200.0),
        (13, 1275.0),

        # Upper boundary
        (17, 1575.0),
        (18, 1650.0),
    ],
)
def test_registration_fee_for_valid_boundary_values(
    total_credits,
    expected_fee,
):
    assert calculate_registration_fee(total_credits) == expected_fee




@pytest.mark.unit
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits",
    [
        -1,     
        19,     
    ],
)
def test_registration_fee_rejects_invalid_credit_values(
    total_credits,
):
    with pytest.raises(ValueError):
        calculate_registration_fee(total_credits)




@pytest.mark.unit
def test_temporary_resource_fixture_creates_test_file(
    temporary_registration_file
):
    """
    Demonstrates that the temporary resource exists during
    the test. The fixture removes it during teardown.
    """
    assert temporary_registration_file.exists()

    assert (
        temporary_registration_file.read_text(encoding="utf-8")
        == "temporary registration test data"
    )

    temporary_registration_file.write_text(
        "updated temporary data",
        encoding="utf-8"
    )

    assert (
        temporary_registration_file.read_text(encoding="utf-8")
        == "updated temporary data"
    )