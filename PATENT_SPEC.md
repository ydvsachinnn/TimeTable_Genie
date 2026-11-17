# PATENT SPECIFICATION

## 1. Title

**COMPUTER-IMPLEMENTED SYSTEM AND METHOD FOR GENERATING AND VERIFYING CONFLICT-FREE ACADEMIC TIMETABLES FOR MULTIDISCIPLINARY EDUCATION FRAMEWORKS**

---

## 2. Field of the Invention

The present invention relates to the field of automated academic scheduling systems, and more particularly to a computer-implemented system and method for generating and independently verifying conflict-free timetables for educational institutions operating under multidisciplinary credit-based frameworks such as the National Education Policy (NEP) 2020.

---

## 3. Background and Problems with Prior Art

Academic timetabling is a well-known combinatorial optimization problem classified as NP-hard. Existing solutions include commercial tools (aSc TimeTables, TimeTable360), open-source systems (UniTime, FET), and research prototypes using constraint programming, genetic algorithms, or integer linear programming.

However, prior art systems suffer from the following limitations:

(a) **No NEP-2020 awareness:** Existing tools are designed for fixed-stream, fixed-section structures. They do not natively model the multidisciplinary structures introduced by India's NEP-2020, including choice-based credit systems (CBCS), elective pools spanning multiple departments, minor degree programs, and category-tagged courses (Major, Minor, Skill Enhancement Courses, Ability Enhancement Courses, Value-Added Courses, and Open Electives).

(b) **No independent verification:** Existing tools validate constraints internally within the solver. They do not produce a separate, independently checkable verification report that proves all constraints are satisfied. An administrator must trust the solver output blindly.

(c) **Brittleness under cross-department constraints:** When courses, faculty, and rooms are shared across departments — as required by NEP-2020 — existing tools often produce clashes or require extensive manual adjustment.

The need exists for a system that (i) models NEP-2020 constraints as first-class entities, (ii) produces guaranteed conflict-free timetables, and (iii) generates an independent verification artifact proving constraint satisfaction.

---

## 4. Objects of the Invention

It is an object of the present invention to provide a computer-implemented method for generating academic timetables that are guaranteed to be free of scheduling conflicts under multidisciplinary education constraints.

It is a further object to provide a verification module that independently checks every constraint against the generated timetable and produces a machine-readable verification report.

It is a further object to model NEP-2020-specific academic structures — including elective pools, cross-department courses, and credit-category-tagged courses — as formal constraints within a constraint-programming solver.

---

## 5. Summary of the Invention

The present invention provides a computer-implemented system comprising:

(a) a **constraint encoder module** that receives structured input data describing courses, faculty, rooms, student groups, time slots, and NEP-2020-specific constraints, and transforms said data into a set of Boolean decision variables and constraint expressions for a constraint-programming solver;

(b) a **solver module** that processes said constraint expressions using a constraint-programming satisfiability (CP-SAT) engine to compute an assignment of courses to time slots and rooms such that all hard constraints are satisfied and soft constraints are optimized; and

(c) a **verifier module** that receives the generated timetable and the original constraint data, independently evaluates every constraint against the timetable, and produces a structured verification report indicating pass or fail status for each constraint and an overall certification of conflict-free status.

---

## 6. Brief Description of Drawings

- **FIG. 1:** System architecture diagram showing the three modules (constraint encoder, solver, verifier) and data flow between them.
- **FIG. 2:** End-to-end flowchart of the timetable generation and verification method.
- **FIG. 3:** Constraint model diagram showing hard and soft constraint categories.
- **FIG. 4:** Verifier flow diagram showing constraint-by-constraint evaluation.
- **FIG. 5:** Sample timetable output for a synthetic NEP-2020 dataset.

---

## 7. Detailed Description

### 7.1 System Architecture (FIG. 1)

The system comprises three modules executing on a processor with access to memory:

**Constraint Encoder Module:** Reads JSON-formatted input containing:
- Course list with attributes: course_id, name, department, category (Major/Minor/SEC/AEC/VAC/OpenElective), credits, required_slots_per_week, enrollment_count
- Faculty list: faculty_id, name, department, qualified_courses, unavailable_slots
- Room list: room_id, capacity, features (lab/lecture/seminar)
- Student groups: group_id, registered_courses
- Time slots: day × period matrix (e.g., 5 days × 8 periods)
- Elective pools: pool_id, list of course_ids in the pool, associated student groups

The encoder creates Boolean decision variables: `assign[c][d][s][r]` = 1 if course `c` is assigned to day `d`, slot `s`, room `r`; 0 otherwise.

**Solver Module:** Adds the following constraints to the CP-SAT model:

*Hard Constraints:*
1. **Faculty non-overlap:** For each faculty member and each (day, slot) pair, at most one of the faculty member's courses is assigned.
2. **Room non-overlap:** For each room and each (day, slot) pair, at most one course is assigned.
3. **Student group non-overlap:** For each student group and each (day, slot) pair, at most one of the group's registered courses is assigned.
4. **Room capacity:** A course is assigned to a room only if room.capacity ≥ course.enrollment_count.
5. **Slot coverage:** Each course is assigned to exactly the number of slots specified by required_slots_per_week.
6. **Faculty availability:** A course is not assigned to a slot where its faculty member is unavailable.
7. **Elective pool non-clash:** Courses within the same elective pool assigned to the same (day, slot) must not conflict for any student group that could choose among them.

*Soft Constraints (added as penalty terms to the objective function):*
1. Minimize total idle gaps for each faculty member across each day.
2. Prefer spreading a course's slots across different days.
3. Respect faculty time-of-day preferences.

The solver invokes the CP-SAT engine, which explores the solution space using constraint propagation and backtracking search. If a feasible solution is found, it outputs a timetable as a JSON structure mapping each course to its assigned (day, slot, room) tuples.

**Verifier Module:** Receives the timetable JSON and original input data. For each hard constraint listed above, it iterates over all relevant entities and checks the condition. It produces a verification report:

```json
{
  "overall_status": "PASS",
  "constraints_checked": 7,
  "results": [
    {"constraint": "faculty_non_overlap", "status": "PASS", "violations": []},
    {"constraint": "room_non_overlap", "status": "PASS", "violations": []},
    ...
  ]
}
```

If any constraint fails, `overall_status` is "FAIL" and the violations array lists the specific conflicting assignments.

### 7.2 Worked Example (Synthetic Dataset)

**Input:**
- 6 courses: CS101 (Major, 3 slots/week, enrollment 60), CS102 (Major, 3 slots/week, 60), MA201 (Minor, 2 slots/week, 40), EC301 (Open Elective, 2 slots/week, 30), HS101 (AEC, 1 slot/week, 80), SK201 (SEC, 2 slots/week, 35)
- 4 faculty: F1 (CS101, CS102), F2 (MA201), F3 (EC301, SK201), F4 (HS101)
- 3 rooms: R1 (capacity 80), R2 (capacity 60), R3 (capacity 40)
- 2 student groups: G1 (CS101, MA201, HS101, EC301), G2 (CS102, SK201, HS101)
- 1 elective pool: Pool-1 = {EC301, SK201} (G1 students may choose either)
- 5 days × 6 slots = 30 available time slots

**Solver output (partial):**

| Course | Day | Slot | Room |
|--------|-----|------|------|
| CS101  | Mon | 1    | R2   |
| CS101  | Wed | 1    | R2   |
| CS101  | Fri | 1    | R2   |
| CS102  | Mon | 2    | R2   |
| MA201  | Tue | 1    | R3   |
| MA201  | Thu | 1    | R3   |
| EC301  | Tue | 3    | R3   |
| SK201  | Tue | 4    | R3   |
| HS101  | Wed | 3    | R1   |
| ...    | ... | ...  | ...  |

**Verifier output:** All 7 hard constraints checked → PASS. No violations.

### 7.3 Pseudocode of Core Method

```
FUNCTION GenerateAndVerifyTimetable(input_data):
    // Step 1: Encode
    model ← new CP-SAT Model
    FOR each course c, day d, slot s, room r:
        assign[c][d][s][r] ← model.NewBoolVar()

    // Step 2: Add hard constraints
    FOR each faculty f, day d, slot s:
        model.Add( SUM(assign[c][d][s][r] for c in f.courses, all r) <= 1 )
    FOR each room r, day d, slot s:
        model.Add( SUM(assign[c][d][s][r] for all c) <= 1 )
    FOR each group g, day d, slot s:
        model.Add( SUM(assign[c][d][s][r] for c in g.courses, all r) <= 1 )
    // ... (capacity, coverage, availability, elective pool constraints)

    // Step 3: Add soft constraints as penalties
    objective ← minimize( gaps_penalty + spread_penalty + preference_penalty )
    model.Minimize(objective)

    // Step 4: Solve
    solver ← new CP-SAT Solver
    status ← solver.Solve(model)
    IF status == FEASIBLE or OPTIMAL:
        timetable ← extract assignments from solver
    ELSE:
        RETURN "No feasible timetable found"

    // Step 5: Verify independently
    report ← Verify(timetable, input_data)
    RETURN timetable, report

FUNCTION Verify(timetable, input_data):
    report ← empty
    FOR each constraint_type in [faculty, room, group, capacity, coverage, availability, elective_pool]:
        violations ← check_constraint(constraint_type, timetable, input_data)
        report.add(constraint_type, "PASS" if violations is empty else "FAIL", violations)
    report.overall ← "PASS" if all passed else "FAIL"
    RETURN report
```

---

## 8. Claims

**Independent Claim 1 (Method):**

1. A computer-implemented method for generating and verifying a conflict-free academic timetable for a multidisciplinary education framework, the method comprising: (a) receiving, by a processor, structured input data comprising a plurality of courses each tagged with a curriculum category, a plurality of faculty members, a plurality of rooms with capacity attributes, a plurality of student groups with course registrations, a set of available time slots, and one or more elective pools each comprising a subset of courses selectable by overlapping student groups; (b) encoding, by the processor, said input data into a constraint-programming model comprising Boolean decision variables representing possible assignments of courses to time-slot-and-room pairs, and constraint expressions representing hard constraints including faculty non-overlap, room non-overlap, student-group non-overlap, room capacity satisfaction, slot coverage requirements, and elective-pool non-clash; (c) solving, by the processor, said constraint-programming model using a CP-SAT solver engine to compute an assignment satisfying all hard constraints; (d) generating, by the processor, a timetable data structure mapping each course to its assigned day, slot, and room; and (e) independently verifying, by a verifier module executing on the processor, said timetable against said input data by evaluating each hard constraint and producing a structured verification report indicating pass or fail status per constraint and an overall conflict-free certification.

**Independent Claim 2 (System):**

2. A computer-implemented system for generating and verifying a conflict-free academic timetable, the system comprising: a processor; a memory coupled to the processor and storing instructions that, when executed, cause the processor to implement: a constraint encoder module configured to receive structured academic input data including courses tagged with NEP-2020 curriculum categories and elective pool definitions, and to generate a constraint-programming model with Boolean decision variables and hard and soft constraint expressions; a solver module configured to solve said constraint-programming model using a CP-SAT engine and to output a timetable data structure; and a verifier module configured to receive said timetable and said input data, to independently evaluate each constraint, and to produce a verification report certifying conflict-free status.

**Independent Claim 3 (Computer-Readable Medium):**

3. A non-transitory computer-readable medium storing instructions that, when executed by a processor, cause the processor to perform the method of claim 1.

**Dependent Claims:**

4. The method of claim 1, wherein the curriculum categories comprise Major, Minor, Skill Enhancement Course, Ability Enhancement Course, Value-Added Course, and Open Elective as defined under India's National Education Policy 2020.

5. The method of claim 1, wherein the elective-pool non-clash constraint ensures that for any student group associated with an elective pool, no two courses within that pool are assigned to the same day-and-slot combination.

6. The method of claim 1, wherein the constraint-programming model further comprises soft constraint expressions representing faculty idle-gap minimization, course-spread maximization across days, and faculty time-preference satisfaction, each associated with a numerical penalty weight.

7. The method of claim 1, wherein the verification report is a structured machine-readable data object comprising, for each hard constraint, a constraint identifier, a pass or fail status, and a list of any violating assignments.

8. The method of claim 1, wherein the verifier module is functionally independent of the solver module and is capable of verifying timetables generated by any source.

9. The method of claim 1, wherein the Boolean decision variables are defined over a four-dimensional space of courses, days, time slots, and rooms.

10. The method of claim 1, wherein the encoding step further comprises applying domain reduction to eliminate decision variables corresponding to assignments that violate room capacity or faculty availability constraints prior to invoking the solver.

11. The system of claim 2, wherein the structured academic input data and the timetable data structure are encoded in JSON format.

12. The system of claim 2, wherein the system further comprises an input validation module that checks the input data for internal consistency prior to encoding.

13. The method of claim 1, wherein the method further comprises, upon the verifier module reporting a FAIL status, outputting the list of violations to enable manual correction.

14. The method of claim 1, wherein courses are shared across multiple departments and the faculty non-overlap and room non-overlap constraints operate across departmental boundaries.

15. The system of claim 2, wherein the system is configured to process cross-department course assignments where a single faculty member teaches courses listed under two or more academic departments.

16. The method of claim 6, wherein the solver minimizes a weighted sum of penalty terms as an objective function while satisfying all hard constraints.

---

## 9. Abstract

A computer-implemented system and method for generating and verifying conflict-free academic timetables for multidisciplinary education frameworks. The system comprises a constraint encoder that transforms structured academic input data — including courses tagged with curriculum categories, elective pools, faculty, rooms, and student groups — into a constraint-programming model with Boolean decision variables. A solver module processes the model using a CP-SAT engine to compute assignments satisfying hard constraints including faculty non-overlap, room non-overlap, student-group non-overlap, room capacity, and elective-pool non-clash. A verifier module independently evaluates every constraint against the generated timetable and produces a structured verification report certifying conflict-free status. The system specifically models multidisciplinary structures including cross-department courses and choice-based credit categories. (119 words)
