import xml.etree.ElementTree as ET
import csv

# Parse the XML file
tree = ET.parse('./FX_MAS_NEWT_OTHR.xml')
root = tree.getroot()

# Open a CSV file for writing
with open('CSV_Output.csv', mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)

    # Write headers (you can define specific fields you want to extract)
    headers = ['RptgCtrPty_LEI', 'CtrPtySd', 'TradrLctn', 'BookgLctn', 'TxId', 'FrstLeg_Amt', 'ScndLeg_Amt', 'XchgRate', 'XchgRateBsis', 'PmtPyer_LEI', 'PmtRcvr_LEI']
    csv_writer.writerow(headers)

    # Find and iterate over each relevant report data in the XML structure
    for rpt in root.findall(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Rpt"):
        row = []
        # Extract specific elements within the report
        rptg_ctr_pty = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}RptgCtrPty/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Id/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Lgl/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}LEI")
        ctr_pty_sd = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}DrctnOrSd/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}CtrPtySd")
        tradr_lctn = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}TradrLctn")
        bookg_lctn = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}BookgLctn")
        tx_id = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}TxId/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}UnqTxIdr")
        frst_leg_amt = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}FrstLeg/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Amt/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Amt")
        scnd_leg_amt = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}ScndLeg/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Amt/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Amt")
        xchg_rate = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}XchgRate")
        base_ccy = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}BaseCcy")
        qtd_ccy = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}QtdCcy")
        pmt_pyer_lei = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}PmtPyer/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Lgl/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}LEI")
        pmt_rcvr_lei = rpt.find(".//{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}PmtRcvr/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Lgl/{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}LEI")

        # Add extracted values to row
        row.append(rptg_ctr_pty.text if rptg_ctr_pty is not None else "")
        row.append(ctr_pty_sd.text if ctr_pty_sd is not None else "")
        row.append(tradr_lctn.text if tradr_lctn is not None else "")
        row.append(bookg_lctn.text if bookg_lctn is not None else "")
        row.append(tx_id.text if tx_id is not None else "")
        row.append(frst_leg_amt.text if frst_leg_amt is not None else "")
        row.append(scnd_leg_amt.text if scnd_leg_amt is not None else "")
        row.append(xchg_rate.text if xchg_rate is not None else "")
        row.append(f"{base_ccy.text}/{qtd_ccy.text}" if base_ccy is not None and qtd_ccy is not None else "")
        row.append(pmt_pyer_lei.text if pmt_pyer_lei is not None else "")
        row.append(pmt_rcvr_lei.text if pmt_rcvr_lei is not None else "")

        # Write the row to the CSV file
        csv_writer.writerow(row)

print("CSV conversion complete. Check CSV_Output.csv.")
