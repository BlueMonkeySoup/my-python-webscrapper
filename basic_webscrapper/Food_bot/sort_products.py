# Tar csv filerna och kollar hur frekvent en produkt är på rea
# Inget mer ska kodas. Hemsidan har ändrats helt.

from files.count_products import ProductSorter

init = ProductSorter()
init.read_write_new_csv_files