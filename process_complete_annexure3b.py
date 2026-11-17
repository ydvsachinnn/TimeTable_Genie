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
        color = r.get("color", None)
        
        rPr = f'<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
        if b: rPr += '<w:b/><w:bCs/>'
        if i: rPr += '<w:i/><w:iCs/>'
        if u: rPr += '<w:u w:val="single"/>'
        if color: rPr += f'<w:color w:val="{color}"/>'
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

def update_docx():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    
    with zipfile.ZipFile(SRC, 'r') as zin:
        zin.extractall(TEMP_DIR)
        
    xml_path = os.path.join(TEMP_DIR, 'word', 'document.xml')
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {'w': W_NS}
    body = root.find('w:body', ns)
    
    # 1. Fill Table 37 missing Sr. Nos.
    tables = body.findall('w:tbl', ns)
    t37 = tables[3] # Table 37 is the 4th table in body
    for row_idx, val in [(1, '1'), (2, '2'), (3, '3')]:
        row = t37.findall('w:tr', ns)[row_idx]
        cell0 = row.findall('w:tc', ns)[0]
        # find p and r or create
        p = cell0.find('w:p', ns)
        if p is None:
            p = ET.SubElement(cell0, f'{{{W_NS}}}p')
        r = p.find('w:r', ns)
        if r is None:
            r = ET.SubElement(p, f'{{{W_NS}}}r')
        t = r.find('w:t', ns)
        if t is None:
            t = ET.SubElement(r, f'{{{W_NS}}}t')
        t.text = val

    # Fill signature placeholders in Table 10 and 12
    t10 = tables[0]
    row5_t10 = t10.findall('w:tr', ns)[5].findall('w:tc', ns)[1]
    p_sig1 = row5_t10.find('w:p', ns)
    if p_sig1 is not None:
        r_sig1 = ET.SubElement(p_sig1, f'{{{W_NS}}}r')
        t_sig1 = ET.SubElement(r_sig1, f'{{{W_NS}}}t')
        t_sig1.text = "__________________________"
        
    t12 = tables[1]
    row5_t12 = t12.findall('w:tr', ns)[5].findall('w:tc', ns)[1]
    p_sig2 = row5_t12.find('w:p', ns)
    if p_sig2 is not None:
        r_sig2 = ET.SubElement(p_sig2, f'{{{W_NS}}}r')
        t_sig2 = ET.SubElement(r_sig2, f'{{{W_NS}}}t')
        t_sig2.text = "__________________________"

    # 2. Build additional elements to insert after element 85 (Worked example section)
    elems_to_insert_after_85 = []
    
    # Schedule Grid Table
    t_ex_headers = ["Day", "Slot 1 (09:00–10:00)", "Slot 2 (10:00–11:00)", "Slot 3 (11:15–12:15)", "Slot 4 (12:15–01:15)"]
    t_ex_widths = [1400, 2100, 2100, 2100, 2100]
    t_ex_rows = [
        ["Monday", "CS101 (R2, F1, G1)", "CS102 (R2, F1, G2)", "---", "---"],
        ["Tuesday", "MA201 (R3, F2, G1)", "---", "EC301 (R3, F3, G1)", "SK201 (R3, F3, G2)"],
        ["Wednesday", "CS101 (R2, F1, G1)", "CS102 (R2, F1, G2)", "HS101 (R1, F4, G1+G2)", "---"],
        ["Thursday", "MA201 (R3, F2, G1)", "---", "EC301 (R3, F3, G1)", "SK201 (R3, F3, G2)"],
        ["Friday", "CS101 (R2, F1, G1)", "CS102 (R2, F1, G2)", "---", "---"]
    ]
    elems_to_insert_after_85.append(ET.fromstring(make_table_xml(t_ex_headers, t_ex_rows, t_ex_widths)))
    elems_to_insert_after_85.append(ET.fromstring(make_p_xml([], space_after=120)))
    
    # 7. Pseudocode of Core Procedures
    elems_to_insert_after_85.append(ET.fromstring(make_p_xml([{"text": "7. Pseudocode of Core Scheduling and Independent Verification Procedures", "bold": True, "sz": 22}], space_before=120, space_after=80)))
    
    pseudo_lines = [
        "ALGORITHM 1: GenerateAndVerifyTimetable(input_data)",
        "Input: Structured academic JSON dataset (courses, faculty, rooms, cohorts, elective pools, time matrix)",
        "Output: Conflict-free Timetable T and machine-readable Verification Certificate V",
        "1:  model ← Initialize CP-SAT Constraint Programming Model()",
        "2:  FOR each course c ∈ C, day d ∈ D, slot s ∈ S, room r ∈ R DO:",
        "3:      IF Capacity(r) < Enrollment(c) OR Faculty(c) unavailable at (d, s) THEN",
        "4:          x[c, d, s, r] ← 0  // Domain Pre-Pruning (prunes 70%–80% of variable search space)",
        "5:      ELSE:",
        "6:          x[c, d, s, r] ← model.NewBoolVar(name=f'assign_{c}_{d}_{s}_{r}')",
        "7:  // Enforce Hard Constraints",
        "8:  FOR each faculty f ∈ F, day d ∈ D, slot s ∈ S DO:",
        "9:      model.Add(SUM_{c ∈ Courses(f), r ∈ R} x[c, d, s, r] ≤ 1)  // Faculty Non-Overlap",
        "10: FOR each room r ∈ R, day d ∈ D, slot s ∈ S DO:",
        "11:     model.Add(SUM_{c ∈ C} x[c, d, s, r] ≤ 1)  // Room Non-Overlap",
        "12: FOR each cohort g ∈ G, day d ∈ D, slot s ∈ S DO:",
        "13:     model.Add(SUM_{c ∈ Registered(g), r ∈ R} x[c, d, s, r] ≤ 1)  // Cohort Non-Overlap",
        "14: FOR each elective pool P, cohort g, day d ∈ D, slot s ∈ S DO:",
        "15:     model.Add(SUM_{c ∈ (P ∩ Registered(g)), r ∈ R} x[c, d, s, r] ≤ 1)  // Elective Pool Non-Clash",
        "16: FOR each course c ∈ C DO:",
        "17:     model.Add(SUM_{d ∈ D, s ∈ S, r ∈ R} x[c, d, s, r] = RequiredSlots(c))  // Slot Coverage",
        "18: // Optimize Soft Constraints (Objective Function Minimization)",
        "19: objective ← w1 * TotalFacultyGaps + w2 * DayClusteringPenalty + w3 * PreferenceViolations",
        "20: model.Minimize(objective)",
        "21: solver ← CP-SAT Solver Instance()",
        "22: status ← solver.Solve(model)",
        "23: IF status == OPTIMAL OR status == FEASIBLE THEN:",
        "24:     timetable T ← ExtractCourseAssignments(solver, x)",
        "25:     certificate V ← VerifyConstraints(timetable=T, constraints=input_data)  // Decoupled Audit",
        "26:     RETURN (T, V)",
        "27: ELSE:",
        "28:     RETURN ('INFEASIBLE: Input constraints mathematically unsatisfiable', NULL)",
        "",
        "ALGORITHM 2: VerifyConstraints(timetable T, constraints C)",
        "Input: Generated Timetable T, Raw Institutional Constraints C",
        "Output: Auditable Verification Report with Boolean PASS/FAIL and Violation Coordinates",
        "1:  report ← InitializeVerificationReport(status='PASS', violations=[])",
        "2:  FOR each constraint_type ∈ [FacultyNonOverlap, RoomNonOverlap, CohortNonOverlap, Capacity, ElectivePool] DO:",
        "3:      violations[constraint_type] ← EvaluateDeterministicConstraint(timetable=T, rule=constraint_type)",
        "4:      IF length(violations[constraint_type]) > 0 THEN:",
        "5:          report.status ← 'FAIL'",
        "6:          report.violations.append(violations[constraint_type])",
        "7:  report.certificate_id ← GenerateCryptographicHash(T, report.status, timestamp=NOW())",
        "8:  RETURN report"
    ]
    for pl in pseudo_lines:
        b_flag = pl.startswith("ALGORITHM") or pl.startswith("Input:") or pl.startswith("Output:")
        elems_to_insert_after_85.append(ET.fromstring(make_p_xml([{"text": pl, "bold": b_flag, "font": "Courier New", "sz": 18}], space_after=30)))
    elems_to_insert_after_85.append(ET.fromstring(make_p_xml([], space_after=120)))

    # 8. Brief Description of Accompanying Drawings
    elems_to_insert_after_85.append(ET.fromstring(make_p_xml([{"text": "8. Brief Description of the Accompanying Drawings", "bold": True, "sz": 22}], space_before=120, space_after=80)))
    drawings_desc = [
        ("FIG. 1: ", "Schematic block diagram illustrating the overall system architecture of TimetableGenie, showing the functional decoupling between the Constraint Encoder Module, the CP-SAT Optimization Solver Engine, and the Independent Constraint Verifier Module."),
        ("FIG. 2: ", "Flowchart illustrating the end-to-end execution workflow of the automated conflict-free timetable generation and verification method."),
        ("FIG. 3: ", "Hierarchical classification diagram illustrating the constraint model, separating mandatory hard constraints from penalty-weighted soft optimization preferences."),
        ("FIG. 4: ", "Flowchart illustrating the deterministic audit logic executed by the Independent Constraint Verifier Module for issuing a machine-checkable compliance certificate."),
        ("FIG. 5: ", "Visual timetable grid matrix representing the clash-free schedule generated for the worked example under NEP-2020 multidisciplinary curriculum structures.")
    ]
    for fig_id, fig_text in drawings_desc:
        elems_to_insert_after_85.append(ET.fromstring(make_p_xml([{"text": fig_id, "bold": True, "sz": 20}, {"text": fig_text, "sz": 20}], space_after=60, bullet=True)))
    elems_to_insert_after_85.append(ET.fromstring(make_p_xml([], space_after=140)))

    # Insert after element 85 (find element with text "Verification Audit: 100% PASS")
    idx_85 = None
    for idx, el in enumerate(body):
        t = ''.join([n.text for n in el.iterfind('.//w:t', ns) if n.text]).strip()
        if "Verification Audit: 100% PASS" in t:
            idx_85 = idx
            break
            
    if idx_85 is not None:
        for offset, new_el in enumerate(elems_to_insert_after_85):
            body.insert(idx_85 + 1 + offset, new_el)
            
    # 3. Build Patent Claims and Abstract to insert before NOC
    elems_before_noc = []
    
    # 12. PATENT CLAIMS
    elems_before_noc.append(ET.fromstring(make_p_xml([{"text": "12. PATENT CLAIMS (Complete Specification Claims under the Indian Patents Act, 1970)", "bold": True, "sz": 24, "color": "002060"}], space_before=180, space_after=100)))
    elems_before_noc.append(ET.fromstring(make_p_xml([{"text": "We claim:", "bold": True, "italic": True, "sz": 22}], space_after=80)))
    
    claims = [
        ("Claim 1 (Independent - Method): ", "A computer-implemented method for generating and independently verifying a conflict-free academic timetable for a multidisciplinary education framework, the method comprising: (a) receiving, by a processor, structured academic input data comprising a plurality of courses each tagged with a curriculum category, a plurality of faculty members with availability constraints, a plurality of rooms with physical capacity attributes, a plurality of student cohorts with registered course selections, a time matrix of available weekly time slots, and one or more elective pools each comprising a subset of courses selectable by overlapping student cohorts; (b) encoding, by the processor, said structured academic input data into a constraint-programming model comprising a four-dimensional matrix of Boolean decision variables representing possible assignments of courses to time-slot-and-room pairs, and constraint expressions representing hard constraints including faculty non-overlap, room non-overlap, student cohort non-overlap, room capacity satisfaction, slot coverage requirements, and elective pool non-clash; (c) applying, by the processor, a domain pre-pruning reduction to eliminate decision variables violating room capacity or faculty availability prior to solving; (d) solving, by the processor, said constraint-programming model using a constraint-programming satisfiability (CP-SAT) engine to compute an assignment satisfying all hard constraints while minimizing soft-constraint penalties; (e) generating, by the processor, a timetable data structure mapping each course to an assigned day, slot, and room; and (f) independently verifying, by a verifier module executing on the processor and decoupled from said CP-SAT engine, said timetable data structure against said structured academic input data by deterministically evaluating each hard constraint and emitting a machine-checkable verification report certifying conflict-free compliance."),
        ("Claim 2 (Independent - System): ", "A computer-implemented system for generating and independently verifying a conflict-free academic timetable, the system comprising: a processor; a memory coupled to the processor and storing executable instructions that, when executed, cause the processor to implement: a constraint encoder module configured to ingest structured academic input data including courses tagged with National Education Policy (NEP) 2020 curriculum categories and elective pool definitions, and to generate a constraint-programming model with four-dimensional Boolean decision variables and constraint expressions; a domain reduction engine configured to pre-prune decision variables having room capacity less than course enrollment or unavailable faculty; an optimization solver module configured to solve said constraint-programming model using a CP-SAT engine and to output a timetable data structure; and an independent verifier module functionally decoupled from said solver module, configured to receive said timetable data structure and said structured academic input data, to deterministically evaluate all hard constraints, and to emit a machine-readable compliance certificate certifying zero constraint violations."),
        ("Claim 3 (Independent - Computer-Readable Medium): ", "A non-transitory computer-readable storage medium storing computer-executable program instructions that, when executed by a processor, cause the processor to perform the method of claim 1."),
        ("Claim 4 (Dependent): ", "The method as claimed in claim 1, wherein the curriculum categories comprise Major courses, Minor disciplines, Skill Enhancement Courses (SEC), Ability Enhancement Courses (AEC), Value-Added Courses (VAC), and Open Electives as defined under the National Education Policy 2020 framework."),
        ("Claim 5 (Dependent): ", "The method as claimed in claim 1, wherein the elective-pool non-clash constraint ensures that for any student cohort associated with an elective pool, no two courses within said elective pool are assigned to an identical day-and-slot combination."),
        ("Claim 6 (Dependent): ", "The method as claimed in claim 1, wherein the constraint-programming model further comprises soft constraint expressions representing faculty idle-gap minimization across daily schedules, course-spread maximization across distinct academic days, and faculty time-window preferences, each associated with a configurable penalty weight."),
        ("Claim 7 (Dependent): ", "The method as claimed in claim 1, wherein the machine-checkable verification report is an exportable data object comprising, for each verified constraint, a unique constraint identifier, an execution pass or fail status, and a list of conflict coordinates identifying violating entities upon occurrence of a constraint violation."),
        ("Claim 8 (Dependent): ", "The method as claimed in claim 1, wherein the verifier module is functionally independent of the solver module and is configured to audit academic timetables generated by any external third-party scheduling source."),
        ("Claim 9 (Dependent): ", "The method as claimed in claim 1, wherein the Boolean decision variables are defined over a four-dimensional index space of course index c, day index d, time slot index s, and room index r."),
        ("Claim 10 (Dependent): ", "The method as claimed in claim 1, wherein the domain pre-pruning reduction eliminates between 70% and 80% of total possible Boolean decision variables prior to invoking the CP-SAT engine."),
        ("Claim 11 (Dependent): ", "The system as claimed in claim 2, wherein the structured academic input data, the timetable data structure, and the compliance certificate are encoded in JavaScript Object Notation (JSON) format."),
        ("Claim 12 (Dependent): ", "The system as claimed in claim 2, wherein the system further comprises an input validation module configured to audit the structured academic input data for logical and mathematical feasibility prior to variable encoding."),
        ("Claim 13 (Dependent): ", "The method as claimed in claim 1, wherein the method further comprises, upon the verifier module reporting a FAIL status, generating an automated conflict diagnostic report highlighting the exact intersecting resources and time slots to guide resolution."),
        ("Claim 14 (Dependent): ", "The method as claimed in claim 1, wherein courses, faculty members, and physical laboratories are shared across multiple disparate academic departments, and wherein faculty non-overlap and room non-overlap constraints operate across departmental boundaries without manual partitioning."),
        ("Claim 15 (Dependent): ", "The method as claimed in claim 1, wherein the method further incorporates inter-campus transit buffer constraints enforcing a minimum interval of non-assigned time slots for faculty and students transitioning between distant physical facilities."),
        ("Claim 16 (Dependent): ", "The method as claimed in claim 6, wherein the CP-SAT engine minimizes a scalar weighted sum of soft penalty terms as an objective function while strictly maintaining feasibility across all hard constraints.")
    ]
    
    for c_title, c_body in claims:
        elems_before_noc.append(ET.fromstring(make_p_xml([{"text": c_title, "bold": True, "sz": 20}, {"text": c_body, "sz": 20}], space_after=80)))
    elems_before_noc.append(ET.fromstring(make_p_xml([], space_after=140)))
    
    # 13. ABSTRACT OF THE INVENTION
    elems_before_noc.append(ET.fromstring(make_p_xml([{"text": "13. ABSTRACT OF THE INVENTION", "bold": True, "sz": 24, "color": "002060"}], space_before=120, space_after=100)))
    abstract_text = "A computer-implemented system and method for generating and independently verifying conflict-free academic timetables for multidisciplinary education frameworks. The system comprises a constraint encoder module that transforms structured academic input data—including courses tagged with NEP-2020 curriculum categories, elective pools, faculty availability, rooms, and student cohorts—into a constraint-programming model with four-dimensional Boolean decision variables. A domain reduction engine executes pre-pruning to eliminate infeasible variables. A solver module processes the model using a CP-SAT engine to compute conflict-free assignments satisfying all hard constraints including faculty non-overlap, room non-overlap, student cohort non-overlap, room capacity, and elective pool non-clash. A decoupled verifier module independently evaluates every constraint against the generated timetable and emits a machine-checkable compliance certificate proving zero conflicts. (119 words)"
    elems_before_noc.append(ET.fromstring(make_p_xml([{"text": abstract_text, "sz": 20}], space_after=180)))
    
    # Insert before NOC element
    idx_noc = None
    for idx, el in enumerate(body):
        t = ''.join([n.text for n in el.iterfind('.//w:t', ns) if n.text]).strip()
        if "NO OBJECTION CERTIFICATE" in t:
            idx_noc = idx
            break
            
    if idx_noc is not None:
        for offset, new_el in enumerate(elems_before_noc):
            body.insert(idx_noc + offset, new_el)

    # Save modified xml
    tree.write(xml_path, xml_declaration=True, encoding='utf-8')
    
    # Re-zip to DST
    with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root_dir, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                full_p = os.path.join(root_dir, file)
                rel_p = os.path.relpath(full_p, TEMP_DIR)
                zout.write(full_p, rel_p)
                
    shutil.rmtree(TEMP_DIR)
    print(f"Successfully generated: {DST}")

if __name__ == '__main__':
    update_docx()
