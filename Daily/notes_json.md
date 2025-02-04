## 1. Identify and remove places where JSON is recreated from Markdown.

- Basically change parse_markdown() to the new load_json().

## 2. Modify all operations (day -t, day -c, day -u) to update JSON first.

## 3️. Test whether Markdown can be fully regenerated from JSON.

## 4️. Remove Markdown-based logic for updating JSON.

## 5️. Introduce day -s --sync for handling manual Markdown edits.

## 6️. Refactor and optimize for a cleaner, more extendable structure.

## New update function.

✅ Step 1: Identify the Previous Month’s JSON

    If today is 2025-03-01, day -u needs to check tasks_2025_2.json (February).
    If today is January (2025-01-01), it should check December of the previous year (tasks_2024_12.json).

📌 Logic for Finding the Previous Month

    Extract the current year and month.
    If it's January (01), switch to December (12) of the previous year.
    Otherwise, just subtract one from the current month.

✅ Step 2: Modify move_unchecked() to Load the Previous Month

Now that we know which file to look for:

    Check if the previous month's JSON exists.
    If it exists, load it and extract unchecked tasks.
    Move those tasks into the current month's JSON.
    Save both files after updating.

✅ Step 3: Handle Missing JSON Files Gracefully

    If the previous month’s JSON doesn’t exist (e.g., first time using the tool), just skip the move operation instead of throwing an error.

🚀 Final Expected Behavior

✔ Each month loads the previous month's JSON to move unchecked tasks.
✔ Handles the transition from December → January properly.
✔ If no previous JSON exists, it just moves on without breaking.
