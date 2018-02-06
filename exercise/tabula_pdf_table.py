# coding: utf-8

## pip install tabula-py
#
# Actually, it extracted the table in PDF by tabula-java commond line.
# dependences: java jdk >= v1.7.0
#

import tabula
import pandas as pd

# Convert to DataFrame.
# df = tabula.read_pdf("c.pdf")

# Convert to CSV.
tabula.convert_into("c.pdf", "c.csv", output_format="csv", pages="all", multiple_tables=True)

print("Done")
