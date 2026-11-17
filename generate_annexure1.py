import zipfile, os, shutil
from xml.sax.saxutils import escape

def make_p(runs, style=None, jc=None, space_after=120, space_before=0, bullet=False):
    pPr = '<w:pPr>'
    if style:
        pPr += f'<w:pStyle w:val="{style}"/>'
    if jc:
        pPr += f'<w:jc w:val="{jc}"/>'
    pPr += f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
    if bullet:
        pPr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    pPr += '</w:pPr>'
    
    r_xml = ""
    for r in runs:
        text = r.get("text", "")
        bold = r.get("bold", False)
        italic = r.get("italic", False)
        underline = r.get("underline", False)
        sz = r.get("sz", None)
        color = r.get("color", None)
        
        rPr = "<w:rPr>"
        if bold:
            rPr += "<w:b/><w:bCs/>"
        if italic:
            rPr += "<w:i/><w:iCs/>"
        if underline:
            rPr += '<w:u w:val="single"/>'
        if sz:
            rPr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        if color:
            rPr += f'<w:color w:val="{color}"/>'
        rPr += "</w:rPr>"
        
        esc_text = escape(text)
        r_xml += f'<w:r>{rPr}<w:t xml:space="preserve">{esc_text}</w:t></w:r>'
        
    return f'<w:p>{pPr}{r_xml}</w:p>'

def make_table(headers, rows, col_widths=None):
    tblPr = '''<w:tblPr>
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
    
    xml = f'<w:tbl>{tblPr}'
    
    if headers:
        xml += '<w:tr>'
        for i, h in enumerate(headers):
            w_attr = f'<w:tcW w:w="{col_widths[i]}" w:type="dxa"/>' if col_widths and i < len(col_widths) else '<w:tcW w:w="0" w:type="auto"/>'
            tcPr = f'<w:tcPr>{w_attr}<w:shd w:val="clear" w:color="auto" w:fill="EDEDED"/></w:tcPr>'
            p_cell = make_p([{"text": h, "bold": True, "sz": 20}], space_after=60)
            xml += f'<w:tc>{tcPr}{p_cell}</w:tc>'
        xml += '</w:tr>'
        
    for r in rows:
        xml += '<w:tr>'
        for i, c in enumerate(r):
            w_attr = f'<w:tcW w:w="{col_widths[i]}" w:type="dxa"/>' if col_widths and i < len(col_widths) else '<w:tcW w:w="0" w:type="auto"/>'
            tcPr = f'<w:tcPr>{w_attr}</w:tcPr>'
            if isinstance(c, list):
                cell_content = "".join(c)
            elif isinstance(c, dict):
                cell_content = make_p([c], space_after=60)
            else:
                cell_content = make_p([{"text": str(c), "sz": 20}], space_after=60)
            xml += f'<w:tc>{tcPr}{cell_content}</w:tc>'
        xml += '</w:tr>'
        
    xml += '</w:tbl>'
    return xml

print("Base setup verified")
