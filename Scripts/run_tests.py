# convenience runner to invoke pytest programmatically if you prefer
import pytest
import sys

if __name__ == "__main__":
    argv = ["-x", "TestCases", "--html=Reports/report.html", "--self-contained-html"]
    rc = pytest.main(argv)
    sys.exit(rc)
