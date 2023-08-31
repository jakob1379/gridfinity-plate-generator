import logging
import math
import os

from dotenv import load_dotenv

load_dotenv()


# Load and log environment variables
def get_env_variable(var_name, default=None, required=False):
    value = os.environ.get(var_name, default)
    if value:
        logging.debug(f"{var_name} loaded successfully.")
    elif required:
        logging.critical(f"Required environment variable {var_name} not set.")
        raise OSError(f"{var_name} not found.")
    return value


version = "0.1.0"

# Set default values for bottom function using environment variables or hardcoded defaults
default_columns = int(get_env_variable("DEFAULT_COLUMNS", default=3))
default_rows = int(get_env_variable("DEFAULT_ROWS", default=3))
default_output_filename = get_env_variable("DEFAULT_OUTPUT_FILENAME", default=None)
default_baseplate_width = float(get_env_variable("DEFAULT_BASEPLATE_WIDTH", default=42))
default_subtracted_square_width = float(
    get_env_variable("DEFAULT_SUBTRACTED_SQUARE_WIDTH", default=42.71)
)
default_rounded_corner_radius = float(get_env_variable("DEFAULT_ROUNDED_CORNER_RADIUS", default=4))
default_baseplate_height = float(get_env_variable("DEFAULT_BASEPLATE_HEIGHT", default=5))
default_bottom_chamfer_height = float(
    get_env_variable("DEFAULT_BOTTOM_CHAMFER_HEIGHT", default=0.985 / math.sqrt(2))
)
default_straight_wall_height = float(get_env_variable("DEFAULT_STRAIGHT_WALL_HEIGHT", default=1.8))
default_verbose = bool(get_env_variable("DEFAULT_VERBOSE", default=False))

# Log that the defaults were loaded
logging.debug("Default values loaded successfully.")
