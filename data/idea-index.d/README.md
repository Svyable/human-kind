# Idea index fragments

`data/idea-index.yaml` is the legacy aggregate. New trusted agent intake materializations use one file per landed idea here instead of appending to that shared YAML file.

Each `HK-####.yaml` file contains exactly one idea-index mapping with the same fields used by the legacy aggregate. Repository validators treat the aggregate and these fragments as one landed index namespace and reject duplicate IDs or dossier mismatches.

This layout lets independent intake PRs add independent files, so two valid agent submissions do not conflict merely because they were created from the same `main` commit.
