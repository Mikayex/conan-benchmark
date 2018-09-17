#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform

if __name__ == "__main__":
    # The shared option is not supported on Windows so it is explicitly disabled
    builder = build_template_default.get_builder(shared_option_name=('' if platform.system() == 'Windows' else None))

    builder.run()
