## Overview

This tool is a personal CLI-based task and note manager. It allows me to manage a directory of Markdown files using JSON as the structured data backend.

The goal is to provide easy task and note management while ensuring that Markdown files are always human-readable and up-to-date.

Eventually, this system could evolve into a web-based interface with a database, but for now, JSON remains the source of truth.

```
~/Notes/Daily/
    ├── 2025/
    │   ├── 2025_01_jan.json  # Json file for january
    │   ├── 2025_01_jan.md    # January tasks & notes
    │   ├── 2025_02_feb.json
    │   ├── 2025_02_feb.md
    │   └── ...
    ├── 2026/
    │   ├── 2026_01_jan.json
    │   ├── 2026_01_jan.md
    │   └── ...
```

## Commands & Behavior

| **Command**       | **Description**                                          | **Where It Happens**         |
| ----------------- | -------------------------------------------------------- | ---------------------------- |
| **`day -t`**      | Add a new task to today’s task list.                     | Updates JSON then markdown   |
| **`day -n`**      | Add a note to today’s notes section.                     | Updates JSON then markdown   |
| **`day -c NUM`**  | Mark a task as completed (by task number from `day -l`). | Updates JSON then markdown   |
| **`day -u`**      | Move all unchecked tasks of the year today’s task list.  | Updates JSON then Markdown   |
| **`day -l`**      | List all unfinished tasks.                               | Reads JSON                   |
| **`day -lc`**     | List all completed tasks.                                | Reads JSON                   |
| **`day -lt TAG`** | List all unfinished tasks with a specific tag.           | Reads JSON                   |
| **`day -ltags`**  | List all available tags.                                 | Reads JSON                   |
| **`day -o`**      | Open today’s Markdown file in an editor.                 | Opens Markdown               |
| **`day -e`**      | Parse Markdown and update JSON if the file was edited.   | Reads Markdown, Updates JSON |

---

## Future Expansion Plan

### Phase 1: CLI-Based Task Manager (Current Plan)

- Fully functional CLI tool for managing tasks and notes.
- Markdown remains human-readable and always up-to-date.
- JSON ensures structured storage, making it easy to manage & search.

### Phase 2: Introduce a Web Interface

- Frontend for easier task management (React, Vue, or Svelte).
- JSON API for task interaction (Flask or FastAPI as a lightweight backend).
- Sync CLI & Web App (CLI updates the same JSON that the web app reads).

### Phase 3: Full Database Integration

- Migrate JSON data into PostgreSQL or SQLite.
- Enable multi-user support (if needed).
- CLI still functions, but as an optional interface to the database.

## Phases of Development

### Phase 1: Markdown-First (Current Phase)

- The program works, but JSON is rebuilt from Markdown every time.
- Operations modify Markdown directly, then JSON is reconstructed.
- No real advantage of JSON yet—it's just being used as a temporary structure.

### Phase 2: JSON as the Source of Truth (Next Step)

- All operations modify JSON first.
- Markdown files are only updated to reflect changes from JSON.
- Keeps Markdown as a read-only interface, making the logic much cleaner.
- This makes the code more understandable, maintainable, and extendable.
- Searching, filtering, and editing become easier because JSON is structured.

### Phase 3: Introduce a Web Interface

- A basic frontend that interacts with the same JSON structure.
- A lightweight API (Flask/FastAPI) to serve JSON data.
- CLI and Web App both work with the same data, but Markdown remains for local viewing.

### Phase 4: Full Database Integration

- Migrate JSON data into PostgreSQL or SQLite.
- Enable multi-user support (if needed).
- CLI remains functional but interacts with the database instead of JSON.

## Syncing Md and Json
