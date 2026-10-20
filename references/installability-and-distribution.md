# Distribution/Installability

Das Distributionsartefakt heißt exakt `skill.zip` und enthält genau einen Ordner `conversion-psychology-web-builder/`. Für Claude Code den Skill-Ordner lokal unter `.claude/skills/` oder `~/.claude/skills/` entpacken/kopieren; die ZIP allein aktiviert Claude Code nicht.

Das Frontend, das ZIP-Vorschau-/Installationsbuttons anbietet, wird **nicht** vom Skill kontrolliert. Zustände für dieses Feld `prepared`, `blocked`, `not_controlled_by_skill` – nie `guaranteed`. Claude Code eigene Versions- und Berechtigungsgrenzen beachten. `agents/openai.yaml` ist ein portabler Metadatenadapter und kein Anzeichen für eine Claude-Code-Installation.
