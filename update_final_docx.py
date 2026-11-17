import zipfile, os, shutil
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

SRC = "/Users/nitinyadav/CSE473/TimetableGenie_Annexure3b_Final.docx"
DST = "/Users/nitinyadav/CSE473/TimetableGenie_Annexure3b_Complete.docx"
TEMP_DIR = "/Users/nitinyadav/CSE473/_final_tmp"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace('w', W_NS)

def make_p_xml(text_runs, style=None, space_after=120, space_before=0, bullet=False):
    pPr = '<w:pPr>'
    if style:
        pPr += f'<w:pStyle w:val="{style}"/>'
    pPr += f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
    if bullet:
        pPr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    pPr += '</w:pPr>'
    
    r_xml = ""
    for r in text_runs:
        t = r.get("text", "")
        b = r.get("bold", False)
        i = r.get("italic", False)
        u = r.get("underline", False)
        sz = r.get("sz", 22)
        font = r.get("font", "Times New Roman")
        
        rPr = f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
        if b: rPr += '<w:b/><w:bCs/>'
        if i: rPr += '<w:i/><w:iCs/>'
        if u: rPr += '<w:u w:val="single"/>'
        rPr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
        
        r_xml += f'<w:r>{rPr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
        
    return f'<w:p xmlns:w="{W_NS}">{pPr}{r_xml}</w:p>'

def make_table_xml(headers, rows, col_widths=None):
    tblPr = f'''<w:tblPr xmlns:w="{W_NS}">
        <w:tblW w:w="0" w:type="auto"/>
        <w:tblBorders>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        </w:tblBorders>
        <w:tblLook w:val="01E0" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0"/>
    </w:tblPr>'''
    
    xml = f'<w:tbl xmlns:w="{W_NS}">{tblPr}'
    
    if headers:
        xml += '<w:tr>'
        for i, h in enumerate(headers):
            w_attr = f'<w:tcW w:w="{col_widths[i]}" w:type="dxa"/>' if col_widths and i < len(col_widths) else '<w:tcW w:w="0" w:type="auto"/>'
            tcPr = f'<w:tcPr>{w_attr}<w:shd w:val="clear" w:color="auto" w:fill="EDEDED"/></w:tcPr>'
            p = make_p_xml([{"text": h, "bold": True, "sz": 20}], space_after=60)
            xml += f'<w:tc>{tcPr}{p}</w:tc>'
        xml += '</w:tr>'
        
    for r in rows:
        xml += '<w:tr>'
        for i, c in enumerate(r):
            w_attr = f'<w:tcW w:w="{col_widths[i]}" w:type="dxa"/>' if col_widths and i < len(col_widths) else '<w:tcW w:w="0" w:type="auto"/>'
            tcPr = f'<w:tcPr>{w_attr}</w:tcPr>'
            p = make_p_xml([{"text": str(c), "sz": 20}], space_after=60)
            xml += f'<w:tc>{tcPr}{p}</w:tc>'
        xml += '</w:tr>'
        
    xml += '</w:tbl>'
    return xml

print("Script framework ready.")
