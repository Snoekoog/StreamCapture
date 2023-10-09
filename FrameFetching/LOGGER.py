from .GLOBAL import LOGGER_CONFIG, LOGGER_COLORS


def log(msg : str, origin : str = None) -> None:


    origin = "[" + origin + "]" if origin else ""

    print(LOGGER_COLORS.OKGREEN + "[" + LOGGER_CONFIG.SCRIPT_NAME + "]" + origin + ": " + msg + LOGGER_COLORS.ENDC)

def warn(msg : str, origin : str = None) -> None:

    origin = "[" + origin + "]" if origin else ""

    print(LOGGER_COLORS.WARNING + "[" + LOGGER_CONFIG.SCRIPT_NAME + "]" + origin + ": " + msg + LOGGER_COLORS.ENDC)

def error(msg : str, origin : str = None) -> None:

    origin = "[" + origin + "]" if origin else ""

    print(LOGGER_COLORS.FAIL + "[" + LOGGER_CONFIG.SCRIPT_NAME + "]" + origin + ": " + msg + LOGGER_COLORS.ENDC)

def note(msg : str, origin : str = None) -> None:

    origin = "[" + origin + "]" if origin else ""

    print(LOGGER_COLORS.OKCYAN + "[" + LOGGER_CONFIG.SCRIPT_NAME + "]" + origin + ": " + msg + LOGGER_COLORS.ENDC)