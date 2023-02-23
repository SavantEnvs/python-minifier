#!/usr/bin/env python3
import decimal
import random

import atheris
import sys
import fuzz_helpers
import random

with atheris.instrument_imports(include=['python_minifier']):
    import python_minifier

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        python_minifier.minify(fdp.ConsumeRemainingString())
    except SyntaxError:
        return -1
    except ValueError as e:
        if 'source code' in str(e):
            return -1
        raise e
    except Exception as e:
        print(type(e))
        print(e)
        raise e



def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
