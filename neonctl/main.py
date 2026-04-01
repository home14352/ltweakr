from neonctl.app import run
from neonctl.utils.logging_utils import setup_logging


def main() -> None:
    setup_logging()
    raise SystemExit(run())


if __name__ == "__main__":
    main()
