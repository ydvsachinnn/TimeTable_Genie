# TimeTable_Genie: NEP-2020 Timetable Generator & Verification Engine

**TimetableGenie** is an automated academic scheduling platform designed to solve the multidisciplinary course allocation challenges introduced by the **National Education Policy (NEP) 2020** and the **Choice Based Credit System (CBCS)** in India (developed for Smart India Hackathon Problem Statement SIH25091).

## Key Features
- **Constraint Programming Solver**: Powered by Google OR-Tools CP-SAT for conflict-free scheduling across shared faculty, classrooms, and multidisciplinary cohorts.
- **Domain Pre-Pruning**: Eliminates 70%–80% of infeasible variable assignments prior to search, dramatically accelerating convergence.
- **Decoupled Verification Engine**: An independent, polynomial-time verification module that deterministically audits the generated timetable against all institutional constraints and emits a machine-readable compliance certificate.
- **NEP-2020 Multidisciplinary Modeling**: Natively handles Major, Minor, SEC, AEC, VAC, and Open Elective course pools without requiring manual cohort splitting.

## Repository Contents
- `PATENT_SPEC.md`: Complete patent specification (Title, Description, Drawings, Claims 1–16, Abstract) drafted under Indian Patents Act 1970 format.
- `CONTENT.md`: Invention Disclosure Form (Annexure 3b / Annexure 1) text content.
- `TimetableGenie_Annexure3b_Complete.docx`: Fully formatted Word document for patent/IPR submission.
- `PRIOR_ART.md`: Prior art analysis covering 18 patent and academic literature references.
- `FILING_CHECKLIST.md`: Comprehensive filing checklist for Indian patent filing.
- `drawings/`: Architectural and procedural diagrams (FIG. 1 to FIG. 5).
- Python helper scripts for automated document processing and verification.

## Team
- **Mohammad Hamid Khan**
- **Sachin Yadav**
Lovely Professional University, Punjab, India
