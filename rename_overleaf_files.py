#!/usr/bin/env python3

from pathlib import Path
import os
import re
import subprocess
import sys

MAPPING = {
    "1.0.tex": "Stage 1 — Charter, Governance, and Templates.tex",
    "1.A.tex": "Stage 1.A — Project Charter.tex",
    "1.B.tex": "Stage 1.B — Key Risks and Mitigations.tex",
    "1.C.tex": "Stage 1.C — Assumptions and Dependencies.tex",
    "1.D.tex": "Stage 1.D — Milestone Plan and Output Order.tex",
    "1.E.tex": "Stage 1.E — Standardized Templates.tex",
    "1.F.tex": "Stage 1.F — Governance Rules and Validity Doctrine.tex",
    "2.0.tex": "Stage 2 — Measurement Standards and Test Protocol Architecture.tex",
    "2.A.tex": "Stage 2.A — Domain Taxonomy.tex",
    "2.B.tex": "Stage 2.B — Metrics and Test Inventory.tex",
    "2.C.tex": "Stage 2.C — Standardized Test Protocol Cards C1-C18.tex",
    "2.D.tex": "Stage 2.D — Performance Thresholds and Alignment for Entry Intermediate Selection-Ready.tex",
    "2.E.tex": "Stage 2.E — Data Recording and Test Logistics Conventions.tex",
    "3.0.tex": "Stage 3 — Test Calendar Deload Map and Macro Stress Pattern.tex",
    "3.A.tex": "Stage 3.A — Design Principles for Testing and Deloads.tex",
    "3.B.tex": "Stage 3.B — Phase-Level Stress and Test Map.tex",
    "3.C.tex": "Stage 3.C — Test Cadence by Metric Type.tex",
    "3.D.tex": "Stage 3.D — Integrated Phase Calendars Compact Form.tex",
    "3.E.tex": "Stage 3.E — Adjustment Rules for Illness Regression and Risk Flags.tex",
    "4.0.tex": "Stage 4 — Phase 00 Specification.tex",
    "4.A.tex": "Stage 4.A — Phase 00 Overview — Phase Row Template.tex",
    "4.B.tex": "Stage 4.B — Phase 00 Timeline and Microcycle Structure.tex",
    "4.C.tex": "Stage 4.C — Movement Menu, Regressions, and Progressions.tex",
    "4.D.tex": "Stage 4.D — Intensity, Volume, and Progression Rules — Phase 00.tex",
    "4.E.tex": "Stage 4.E — Testing Within Phase 00 and Scaled Use of Stage 2 Protocols.tex",
    "4.F.tex": "Stage 4.F — Safety, Red-Flag Criteria, and Stop Rules for Phase 00.tex",
    "4.G.tex": "Stage 4.G — Exit Standards for Phase 00 — Safe Entry to Phase 01.tex",
    "5.0.tex": "Stage 5 — Macro Design for Phases 01-13.tex",
    "5.A.tex": "Stage 5.A — Master Macro-Phase Table — Compact Overview.tex",
    "5.B.01.tex": "Stage 5.B — Detailed Phase Card — Phase 01.tex",
    "5.B.02.tex": "Stage 5.B — Detailed Phase Card — Phase 02.tex",
    "5.B.03.tex": "Stage 5.B — Detailed Phase Card — Phase 03.tex",
    "5.B.04.tex": "Stage 5.B — Detailed Phase Card — Phase 04.tex",
    "5.B.05.tex": "Stage 5.B — Detailed Phase Card — Phase 05.tex",
    "5.B.06.tex": "Stage 5.B — Detailed Phase Card — Phase 06.tex",
    "5.B.07.tex": "Stage 5.B — Detailed Phase Card — Phase 07.tex",
    "5.B.08.tex": "Stage 5.B — Detailed Phase Card — Phase 08.tex",
    "5.B.09.tex": "Stage 5.B — Detailed Phase Card — Phase 09.tex",
    "5.B.10.tex": "Stage 5.B — Detailed Phase Card — Phase 10.tex",
    "5.B.11.tex": "Stage 5.B — Detailed Phase Card — Phase 11.tex",
    "5.B.12.tex": "Stage 5.B — Detailed Phase Card — Phase 12.tex",
    "5.B.13.tex": "Stage 5.B — Detailed Phase Card — Phase 13.tex",
    "5.C.tex": "Stage 5.C — Adaptation Sequencing Narrative — 3.5-Year Logic.tex",
    "5.D.tex": "Stage 5.D — Phase Dependencies and Gating Rules.tex",
    "5.E.tex": "Stage 5.E — Alignment With Test Calendar and Deload Map.tex",
    "6.0.tex": "Stage 6 — Phase-by-Phase Equipment and Resource Build-Out Map.tex",
    "6.A.tex": "Stage 6.A — Category and Tier Definitions.tex",
    "6.B.tex": "Stage 6.B — Phase × Category Matrix Timeline View.tex",
    "6.C.tex": "Stage 6.C — Phase-Specific Acquisition Lists Delta-Based.tex",
    "6.D.tex": "Stage 6.D — Minimal vs Ideal Kit Pathways.tex",
    "6.E.tex": "Stage 6.E — Consistency, Safety, and Compliance Check.tex",
    "7.0.tex": "Stage 7 — Systems, Equipment, and Capability Overviews.tex",
    "7.01.tex": "Stage 7.01 — Strength and Resistance Training Equipment.tex",
    "7.01A.tex": "Stage 7.01-A — Shopping List Chart.tex",
    "7.02.tex": "Stage 7.02 — Hormonal Support and Adaptogens.tex",
    "7.02A.tex": "Stage 7.02-A — Shopping List Chart.tex",
    "7.03.tex": "Stage 7.03 — Foundational Health Supplements.tex",
    "7.03A.tex": "Stage 7.03-A — Shopping List Chart.tex",
    "7.04.tex": "Stage 7.04 — Performance and Auxiliary Supplements.tex",
    "7.04A.tex": "Stage 7.04-A — Shopping List Chart.tex",
    "7.05.tex": "Stage 7.05 — Cognitive Performance and Energy Enhancers.tex",
    "7.05A.tex": "Stage 7.05-A — Shopping List Chart.tex",
    "7.06.tex": "Stage 7.06 — Recovery Sleep and Stress-Support Aids.tex",
    "7.06A.tex": "Stage 7.06-A — Shopping List Chart.tex",
    "7.07.tex": "Stage 7.07 — Load-Bearing Rucking and Carry Systems.tex",
    "7.07A.tex": "Stage 7.07-A — Shopping List Chart.tex",
    "7.08.tex": "Stage 7.08 — Conditioning Endurance and Aerobic Training Tools.tex",
    "7.08A.tex": "Stage 7.08-A — Shopping List Chart.tex",
    "7.09.tex": "Stage 7.09 — Health Monitoring Diagnostics and Biometrics.tex",
    "7.09A.tex": "Stage 7.09-A — Shopping List Chart.tex",
    "7.10.tex": "Stage 7.10 — Logistics Maintenance Storage and Sustainment Equipment.tex",
    "7.10A.tex": "Stage 7.10-A — Shopping List Chart.tex",
    "7.11.tex": "Stage 7.11 — Footwear Systems and Foot Care.tex",
    "7.11A.tex": "Stage 7.11-A — Shopping List Chart.tex",
    "7.12.tex": "Stage 7.12 — Recovery Mobility and Tissue-Care Implements.tex",
    "7.12A.tex": "Stage 7.12-A — Shopping List Chart.tex",
    "7.13.tex": "Stage 7.13 — Nutrition Preparation and Hydration Systems.tex",
    "7.13A.tex": "Stage 7.13-A — Shopping List Chart.tex",
    "7.14.tex": "Stage 7.14 — Environmental Apparel, Cold Hot Wet Inclement Weather.tex",
    "7.14A.tex": "Stage 7.14-A — Shopping List Chart.tex",
    "7.15.tex": "Stage 7.15 — General Training and Daily Wear Apparel.tex",
    "7.15A.tex": "Stage 7.15-A — Shopping List Chart.tex",
    "7.16.tex": "Stage 7.16 — Operational Self-Management Systems.tex",
    "7.16A.tex": "Stage 7.16-A — Shopping List Chart.tex",
    "7.17.tex": "Stage 7.17 — Aquatic Training and Water Safety Equipment.tex",
    "7.17A.tex": "Stage 7.17-A — Shopping List Chart.tex",
    "7.18.tex": "Stage 7.18 — Testing Timing Measurement and Course-Setup Tools.tex",
    "7.18A.tex": "Stage 7.18-A — Shopping List Chart.tex",
    "7.19.tex": "Stage 7.19 — Protective and Assistive Equipment.tex",
    "7.19A.tex": "Stage 7.19-A — Shopping List Chart.tex",
    "7.20.tex": "Stage 7.20 — Personal Hygiene Health and Sanitation Items.tex",
    "7.20A.tex": "Stage 7.20-A — Shopping List Chart.tex",
    "8.0.tex": "Stage 8 — Crosswalk Gap Check and Consistency Audit Packet.tex",
    "8.A.tex": "Stage 8.A — Master Standards Index.tex",
    "8.B.tex": "Stage 8.B — Standards to Tests to Phases Crosswalk.tex",
    "8.C.tex": "Stage 8.C — Standards to Gear and Resources to Overviews Crosswalk.tex",
    "8.D.tex": "Stage 8.D — Gap Overload Inconsistency Analysis Log.tex",
    "8.E.tex": "Stage 8.E — Pre-Deploy and Implementation Checklists, Standards and Tests, Gear, Safety, Environment.tex",
    "9.0.tex": "Stage 9 — Final QA Packaging and Implementation Guide.tex",
    "9.A.tex": "Stage 9.A — Executive Program Snapshot, Deployable Summary.tex",
    "9.B.tex": "Stage 9.B — Artifact Index and Package Structure, Folder and File Convention.tex",
    "9.C.tex": "Stage 9.C — QA Summary Known Issues and Deviation Controls.tex",
    "9.D.tex": "Stage 9.D — Coach Implementation Guide, Cadence Gates Decision Rules.tex",
    "9.E.tex": "Stage 9.E — Versioning and Change-Log Framework.tex",
    "9.F.tex": "Stage 9.F — Final Deployment Checklists.tex",
    "10.0.tex": "Stage 10 — Nutrition Operating System.tex",
    "10.A.tex": "Stage 10.A — Macro Ladder, Phase 00-13.tex",
    "10.B.tex": "Stage 10.B — Adjustment Rules.tex",
    "10.C.tex": "Stage 10.C — Hydration and Electrolytes Operating System.tex",
    "10.D.tex": "Stage 10.D — Troubleshooting Ladders.tex",
    "11.0.tex": "Stage 11 — Pre-Selection Conditioning and Recovery.tex",
    "11.A.tex": "Stage 11.A — Pre-Selection Conditioning Overview.tex",
    "11.B.tex": "Stage 11.B — Final Preparation and Test Optimization.tex",
    "11.C.tex": "Stage 11.C — Recovery and Injury Prevention in Final Phases.tex",
    "11.D.tex": "Stage 11.D — Nutritional Adjustments for Final Selection.tex",
    "12.0.tex": "Stage 12 — Operational Controls, Recording Standards, and Sustainment.tex",
    "12.A.tex": "Stage 12.A — Standard Test Log Template.tex",
    "12.B.tex": "Stage 12.B — Validity Tags Definitions and Examples.tex",
    "12.C.tex": "Stage 12.C — Environment Recording Standards — Routes, Pool Units, Weather, Surface.tex",
    "12.D.tex": "Stage 12.D — Emergency Stop Rules and Escalation Flow.tex",
    "12.E.tex": "Stage 12.E — Maintenance Handoff Checklist Post Phase 13 Sustainment.tex",
}

EDITABLE_SUFFIXES = {".tex", ".bib", ".cls", ".sty", ".md"}
ROOT = Path(".").resolve()


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, text=True, capture_output=True)


def ensure_git_repo() -> None:
    try:
        run("git", "rev-parse", "--is-inside-work-tree")
    except subprocess.CalledProcessError:
        print("Not inside a Git repository.", file=sys.stderr)
        sys.exit(1)


def rename_files() -> list[tuple[str, str]]:
    renamed = []
    for old, new in MAPPING.items():
        old_path = ROOT / old
        new_path = ROOT / new

        if not old_path.exists():
            continue

        if new_path.exists():
            if old_path.resolve() != new_path.resolve():
                print(f"Target already exists, skipping: {new}", file=sys.stderr)
            continue

        old_path.rename(new_path)
        renamed.append((old, new))

    return renamed


def update_text_references() -> list[Path]:
    changed_files = []
    ordered = sorted(MAPPING.items(), key=lambda kv: len(kv[0]), reverse=True)

    command_patterns = [
        r"(\\(?:input|include|subfile)\s*\{)([^{}]+)(\})",
        r"(\\(?:includegraphics)(?:\[[^\]]*\])?\s*\{)([^{}]+)(\})",
        r"(\\(?:bibliography|addbibresource)\s*\{)([^{}]+)(\})",
    ]

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EDITABLE_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        original = text

        for old, new in ordered:
            old_stem = old[:-4]
            new_stem = new[:-4]

            def replacer(match: re.Match) -> str:
                prefix, body, suffix = match.groups()
                value = body.strip()

                if value == old:
                    value = new
                elif value == old_stem:
                    value = new_stem
                elif value.endswith("/" + old):
                    value = value[: -len(old)] + new
                elif value.endswith("/" + old_stem):
                    value = value[: -len(old_stem)] + new_stem

                return f"{prefix}{value}{suffix}"

            for pattern in command_patterns:
                text = re.sub(pattern, replacer, text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files.append(path)

    return changed_files


def git_commit_and_push() -> None:
    run("git", "add", "-A")

    diff = run("git", "diff", "--cached", "--quiet", check=False)
    if diff.returncode == 0:
        return

    if os.getenv("GITHUB_ACTIONS") == "true":
        run("git", "config", "user.name", "github-actions[bot]")
        run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    run("git", "commit", "-m", "Rename stage files to descriptive titles")

    if os.getenv("GITHUB_ACTIONS") == "true":
        run("git", "push")


def main() -> None:
    ensure_git_repo()
    rename_files()
    update_text_references()
    git_commit_and_push()


if __name__ == "__main__":
    main()
