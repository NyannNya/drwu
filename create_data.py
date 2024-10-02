from utils.scrape_products import web_dr_wu, remove_duplicates
from utils.product_details import create

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

remove_duplicates()
web_dr_wu()
create()
