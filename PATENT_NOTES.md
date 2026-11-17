# Patent Notes — TimetableGenie (Assumed Architecture)

> **Note:** No code exists yet. This documents the *planned* system design.
> When building the project, follow this as a blueprint.

## Assumed Technology Stack
- **Language:** Python 3.10+
- **Solver:** Google OR-Tools CP-SAT
- **Data format:** JSON input (courses, rooms, faculty, constraints)
- **Output:** JSON timetable + verification report

## Algorithm: CP-SAT Constraint Programming
- Decision variables: `assign[course, day, slot, room]` — boolean
- Faculty mapped to courses; room capacity checked against enrollment

## Hard Constraints (must never be violated)
1. Faculty cannot teach two courses in the same slot
2. Room cannot host two courses in the same slot
3. Student group cannot attend two courses in the same slot
4. Room capacity ≥ course enrollment
5. Course must be assigned to exactly the required number of slots per week

## Soft Constraints (optimized via penalty terms)
1. Minimize faculty idle gaps between classes
2. Spread electives across the week
3. Faculty time-of-day preferences

## NEP-2020 Specific Modeling
- Courses tagged by category: Major, Minor, SEC, AEC, VAC, Open Elective
- Elective pools: students pick from a pool → all courses in a pool must be in the same slot (or none clash for the same student group)
- Cross-department sharing: a faculty member or room can be shared across departments

## Verifier Module
- **Input:** generated timetable JSON + original constraints JSON
- **Process:** iterates over every constraint and checks it against the timetable
- **Output:** verification report (pass/fail per constraint, overall pass/fail)
- Independent of solver — can verify any timetable, not just solver output

## What's Technically Unusual
1. Solver + independent verifier as separate modules (not just internal validation)
2. NEP-2020-specific constraint categories modeled as first-class entities
3. Verification report as a deliverable artifact alongside the timetable
