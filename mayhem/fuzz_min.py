#!/usr/bin/env python3
"""Atheris fuzz harness for python-minifier.

python_minifier.minify() parses arbitrary Python source and unparses it into
its most compact representation. This harness feeds fuzzer-generated text to
minify(); Atheris instruments the imported python_minifier modules so
libFuzzer steers the minifier toward new code paths.

Run modes (driven by the compiled launcher `fuzz_min` / `-standalone`):
  * fuzzing      — `python3 fuzz_min.py [libFuzzer args]`
  * single input — `python3 fuzz_min.py <file>` (libFuzzer runs it once)
"""
import os
import sys

# fuzz_helpers.py lives alongside this harness — make it importable when the
# launcher execs us by absolute path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import atheris
import fuzz_helpers

# Instrument the library under test so the fuzzer gets coverage feedback.
with atheris.instrument_imports(include=['python_minifier']):
    import python_minifier


def TestOneInput(data: bytes) -> None:
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        python_minifier.minify(fdp.ConsumeRemainingString())
    except SyntaxError:
        # Malformed Python source is expected fuzzer input — not a defect.
        return
    except ValueError as e:
        if 'source code' in str(e):
            return
        raise
    except RecursionError:
        # CPython's compile()/ast recursion limit on deeply nested input —
        # an interpreter resource limit, not a python_minifier defect.
        return


def main() -> None:
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
