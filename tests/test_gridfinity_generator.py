import pytest

from gridfinity_plate_generator import gridfinity_generator


# Takes in no arguments, should raise an exception


def test_base_no_args() -> None:
    with pytest.raises(ValueError):
        gridfinity_generator.base()


# Tests base function with correct inputs (using defaults)


def test_base_correct_rows_cols_inputs() -> None:
    try:
        gridfinity_generator.base(columns=3, rows=3)
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


# Tests base function using widht/length with correct inputs (using defaults)


def test_base_correct_widht_length_inputs() -> None:
    try:
        gridfinity_generator.base(length=100, width=100)
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


# Tests base function with incorrect input type


def test_base_incorrect_inputs() -> None:
    with pytest.raises(TypeError):
        gridfinity_generator.base(columns="three", rows=3)  # type: ignore


# Takes in no arguments, should raise an exception


def test_bottom_no_args() -> None:
    with pytest.raises(ValueError):
        gridfinity_generator.bottom()


# Tests bottom function with correct inputs (using defaults)


def test_bottom_correct_inputs() -> None:
    try:
        gridfinity_generator.bottom(columns=3, rows=3)
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


# Tests bottom function using widht/length with correct inputs (using defaults)


def test_bottom_correct_widht_length_inputs() -> None:
    try:
        gridfinity_generator.bottom(length=100, width=100)
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")


# Tests bottom function with incorrect input type


def test_bottom_incorrect_inputs() -> None:
    with pytest.raises(TypeError):
        gridfinity_generator.bottom(columns="three", rows=3)  # type: ignore
