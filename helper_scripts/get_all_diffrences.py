import os, datetime
import pandas as pd
from helper_scripts.check_diffrences import CheckDiffrences


def All_diffrences(old_stock, new_stock, old_po, new_po, report_path):
    stock_data = CheckDiffrences(
        old_file_path=old_stock, new_file_path=new_stock, data_type="stock"
    )()
    raw_old_stock = stock_data[0]
    raw_new_stock = stock_data[1]
    diff_stock = stock_data[2]

    po_data = CheckDiffrences(
        old_file_path=old_po, new_file_path=new_po, data_type="po"
    )()
    raw_old_po = po_data[0]
    raw_new_po = po_data[1]
    diff_po = po_data[2]

    now = datetime.datetime.now()
    filename = f"Report_stock_po_diff_check_{now.strftime('%d%m%Y_%H%M')}.xlsx"
    report_file_path = os.path.join(report_path, filename)

    with pd.ExcelWriter(report_file_path, engine="openpyxl") as writer:
        diff_stock.to_excel(writer, sheet_name="Stock_diffrence", index=True)
        diff_po.to_excel(writer, sheet_name="PO_diffrence", index=True)

        diff_stock.to_excel(writer, sheet_name="Stock_diffrence", index=True)
        diff_po.to_excel(writer, sheet_name="PO_diffrence", index=True)

        raw_old_po.to_excel(writer, sheet_name="PO_old_raw", index=False)
        raw_new_po.to_excel(writer, sheet_name="PO_new_raw", index=False)

        raw_old_stock.to_excel(writer, sheet_name="Stock_old_raw", index=False)
        raw_new_stock.to_excel(writer, sheet_name="Stock_new_raw", index=False)

    return None
