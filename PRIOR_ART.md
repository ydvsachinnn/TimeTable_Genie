# Prior Art Analysis — TimetableGenie: NEP-2020 Timetable Generator

**Prepared for:** Patent Application (Indian Patent Act 1970 / PCT)
**Date:** 2026-11-17
**Status:** Pre-filing research — to be updated after code review (Step 1)

---

## 1. Patent Literature

| # | Reference | Type | What It Does | How TimetableGenie Potentially Differs |
|---|-----------|------|-------------|---------------------------------------|
| 1 | **US20080057482A1** — *"System for scheduling classes and managing educational resources"* | US Patent Application (Published) | Automates class scheduling for K-12/post-secondary. Handles curriculum modules, prerequisites, student competence levels, teacher qualifications/workloads, and "academy" sub-groupings. Uses optimization/assignment algorithms to allocate students to classes. | US20080057482A1 focuses on competence-based student allocation and K-12 academy structures. TimetableGenie targets NEP-2020 multidisciplinary structures (majors, minors, elective pools, cross-department courses) and includes a **dedicated verification/proof step** that produces a machine-checkable certificate of constraint satisfaction — a feature not disclosed in this patent. |
| 2 | **US8052426B2** — *Administrative scheduling / multi-constraint optimization* | US Patent (Granted) | Hierarchical multi-constraint optimization with dynamic backtracking for academic scheduling bottlenecks. | Focuses on generic hierarchical backtracking. TimetableGenie uses [TO CONFIRM: specific solver — likely CP-SAT or similar] with NEP-2020-specific constraint encoding and a separate verifier module. |
| 3 | **US10726368B2** — *Satellite scheduling using GA + SA* | US Patent (Granted) | Hybrid Genetic Algorithm + Simulated Annealing for satellite mission scheduling. | Different domain entirely (satellite scheduling). Relevant only as prior art for the general technique of hybrid metaheuristics applied to scheduling. TimetableGenie's constraint model is education-specific. |

---

## 2. Academic Papers

| # | Reference | What It Does | How TimetableGenie Potentially Differs |
|---|-----------|-------------|---------------------------------------|
| 4 | **Murray, Müller & Rudová** — *"Modeling and Solution of a Complex University Course Timetabling Problem"* (Purdue / Masaryk Univ.; backbone of UniTime/CPSolver) | Foundational work on real-world university timetabling via constraint satisfaction. Iterative Forward Search (IFS) algorithm. Won ITC 2007. | UniTime/CPSolver does not target NEP-2020 structures. It does not produce a separate, independently verifiable proof/certificate of correctness. TimetableGenie's verifier is a distinguishing feature [TO CONFIRM after code review]. |
| 5 | **Zhang & Lau** — *"Constructing University Timetable Using Constraint Satisfaction Programming Approach"* | Early CSP-based university timetabling. Evaluates variable/value ordering, arc consistency, solver performance. | Foundational CSP work without NEP-specific constraints, without verification output, and without modern CP-SAT solver capabilities. |
| 6 | **"Solving the Course-timetabling Problem of Cairo University Using Max-SAT"** (arXiv) | Translates hard/soft scheduling constraints to propositional logic; solves via Max-SAT solvers. | Max-SAT approach is an alternative to CP-SAT. Interesting parallel: both reduce timetabling to formal logic. However, this paper does not produce a separately verifiable certificate, nor does it target Indian NEP-2020 structures. |
| 7 | **"Timetable Optimizer: Automated University Schedule Generation Using CP-SAT and LLM Intelligence"** (2026, Semantic Scholar) | Production-grade system: OR-Tools CP-SAT + LLM (Gemini API) for parsing natural-language constraints. 5-dimensional binary decision variables. Pre-pruning eliminates ~80% of variables. | Very close technically (CP-SAT-based). Key potential differences: (a) TimetableGenie includes a **verifier/certificate** step, (b) targets NEP-2020 specifically, (c) [TO CONFIRM: does it use LLM integration? If not, different architecture]. **This is the closest prior art — overlap must be carefully addressed.** |
| 8 | **"Intelligent Timetable and Workload Manager using CP-SAT Solver"** (ResearchGate) | CP-SAT for educational timetabling with workload balancing. | Similar solver technology. TimetableGenie's potential novelty lies in the NEP-2020 constraint model and verifier, not the solver choice alone. |

---

## 3. Commercial / Open-Source Software

| # | Reference | What It Does | How TimetableGenie Potentially Differs |
|---|-----------|-------------|---------------------------------------|
| 9 | **UniTime** (Apereo Foundation, open-source, LGPL) | Comprehensive university scheduling: CPSolver (IFS algorithm), course timetabling, exam scheduling, student sectioning. Interactive solver with suggestions. Supports Minimal Perturbation. Won ITC 2007. | UniTime is the gold standard but: (a) Java-based enterprise system, not lightweight; (b) no NEP-2020-specific constraint model; (c) no independently verifiable proof of constraint satisfaction — it validates internally but does not emit a machine-checkable certificate. |
| 10 | **FET** (Free Timetabling Software, open-source) | Desktop app using advanced constraint-satisfaction heuristics. Infinitely customizable rules. Free. | Highly flexible but: (a) no NEP-2020 awareness; (b) no formal verifier/proof output; (c) not cloud/API-based. |
| 11 | **aSc TimeTables** (Commercial) | Commercial desktop-first scheduler. Advanced constraint solver, substitution management, mobile publishing. Globally used. | Commercial product. Proprietary solver. No NEP-2020 focus. No verifier/certificate. |
| 12 | **TimeTable360** (Commercial, India-focused) | Cloud SaaS for Indian schools/colleges. Handles parallel elective groups, lab batches, multi-section management. "AI Timetable Doctor" health scoring. | **Most relevant commercial competitor for the Indian market.** Handles CBCS/NEP patterns. However: (a) proprietary, closed implementation; (b) no disclosed formal verification/proof-of-correctness step; (c) [TO CONFIRM: does TimetableGenie's algorithm/architecture differ from TimeTable360's approach?]. |
| 13 | **ChronoSolve** (GitHub: `nihal1294/chronosolve`) | Configurable CP-SAT scheduler with Tauri desktop app. Hard + soft constraints via configuration. | Open-source CP-SAT timetabling. No NEP-2020 focus. No verifier. |
| 14 | **Academic Timetabling Platform** (GitHub: `andresrubiop/academic-timetabling`) | Research platform: OR-Tools CP-SAT + LNS refinement, FastAPI + PostgreSQL + Next.js. What-if analysis. | Research-oriented. No NEP-2020 model. No formal verification output. |

---

## 4. NEP-2020 / CBCS-Specific Tools

| # | Reference | What It Does | Overlap / Difference |
|---|-----------|-------------|---------------------|
| 15 | Various Indian campus ERPs (Entab, CollPoll, custom-built) | University management systems with scheduling modules adapted for CBCS credit-framework mapping. | Generic ERP scheduling, not specialized solver-based. No formal verification. Overlap: same problem domain (NEP-2020 timetabling in India). |
| 16 | SIH hackathon projects (various years) | Student-built prototypes targeting NEP-related scheduling. Typically use GA, backtracking, or CP-SAT. | Direct competitors in concept. TimetableGenie's potential edge: the **verifier/certificate mechanism** [TO CONFIRM]. |

---

## 5. Formal Verification in Scheduling (Related Art)

| # | Reference | What It Does | Relevance |
|---|-----------|-------------|-----------|
| 17 | **SMT-based schedule verification** (Z3 / CVC5) | Encodes scheduling constraints in first-order logic; SMT solver finds schedule + proves correctness. Can emit proof certificates (LFSC / Alethe formats). | Closest conceptual match to TimetableGenie's verifier. However, typically applied in safety-critical domains (aviation, medical), not university timetabling. If TimetableGenie implements a lightweight constraint-checking verifier (not a full SMT proof), the approach differs. [TO CONFIRM: what exactly does TimetableGenie's verifier produce?] |
| 18 | **Proof-producing computation** paradigm | Untrusted solver generates solution + certificate; trusted lightweight kernel verifies independently. | This paradigm is well-known in verification research but **rarely applied to educational timetabling**. If TimetableGenie implements this pattern, it is a distinguishing architectural feature. |

---

## 6. Summary: Potentially Novel & Inventive Aspects

Based on the prior art survey (to be refined after code review in Step 1):

### Likely Novel (if implemented as described)
1. **Verifier/Certificate Architecture:** A separate verification module that takes the generated timetable and independently proves all constraints are satisfied, producing a machine-checkable proof or certificate. This "solver + verifier" separation is well-known in formal methods but **rarely applied to educational timetabling** and not disclosed in any of the identified prior art.
2. **NEP-2020-Specific Constraint Encoding:** A constraint model specifically designed for NEP-2020 structures — choice-based credits, cross-department elective pools, major/minor/skill-enhancement/value-added course categories, multi-batch lab rotations under the new framework.

### Possibly Novel (depends on implementation details)
3. **Specific data structures** for encoding NEP-2020 course hierarchies and student elective clusters.
4. **Integration of solver + verifier in a single pipeline** with guaranteed conflict-free output.

### NOT Novel (overlaps with prior art)
- Using CP-SAT / constraint programming for timetabling (well-established).
- Hard vs. soft constraint separation (standard technique).
- Room/faculty/student clash avoidance (fundamental requirement).
- Pre-pruning of variable domains (documented in multiple papers).
- Using genetic algorithms or simulated annealing for timetabling (extensive prior art).

---

## 7. Honest Assessment of Overlap

> [!WARNING]
> **The core scheduling algorithm (likely CP-SAT-based) is well-covered by prior art.** The claim strategy must NOT rely on the choice of solver alone. The patent's strength depends on:
> 1. The **verifier/certificate** mechanism (must be technically concrete, not just "we check the output")
> 2. The **specific NEP-2020 constraint model** (must be more than just "we added Indian rules to a generic solver")
> 3. **Technical effect** framing for Section 3(k) compliance

---

## 8. Questions for Inventors (to resolve after code review)

- [ ] What exactly does the verifier produce? Is it a structured certificate, a report, or a boolean check?
- [ ] Is the verifier independent of the solver (can it verify solutions from any source)?
- [ ] What solver is used — CP-SAT, ILP, custom heuristic, or hybrid?
- [ ] Are there any LLM/NLP components for constraint parsing?
- [ ] How are NEP-2020 course categories (Major, Minor, SEC, AEC, VAC) modeled in the data structures?
- [ ] Has the system been demonstrated publicly at SIH or elsewhere before filing?
- [ ] Is the GitHub repository public? Since when?
