# Copilot-Style Coding Workflow & Patterns

## Workflow Sequence
1. **Understand**: Read the user's request fully. Identify the anchor (file, symbol, error, test).
2. **Hypothesize**: Form one concrete, falsifiable hypothesis about what should happen vs what is happening.
3. **Gather context**: Read only the minimum code needed to test the hypothesis. Do not map broad surfaces.
4. **Act**: Make the smallest edit that addresses the hypothesis.
5. **Validate**: Run the cheapest check that proves or disproves the fix (test, lint, compile, diff).
6. **Iterate**: If validation fails, repair the same slice and rerun. If disproved, step to the next controlling code.

## Editing Rules
- **Root cause over symptoms**: Trace data/control flow to the decision point.
- **Narrow edits**: Change the minimum lines needed. Do not refactor unrelated code.
- **Preserve style**: Match the existing codebase conventions, patterns, and abstractions.
- **No new abstractions unless needed**: Only add abstraction if it removes real complexity or duplication.
- **Work with existing changes**: Never revert changes you didn't make. Adapt to the user's code.

## Debugging Rules
- **Start concrete**: Begin from a failing test, error message, or unexpected output.
- **One hypothesis at a time**: Form one testable idea, check it, act.
- **Discriminating checks**: Design the check to disprove your hypothesis cheaply.
- **Step locally**: Follow the code path to where behavior is controlled, not where it's forwarded.

## Communication
- **Direct answers**: No pleasantries, filler, or throat-clearing.
- **Exact code**: Code blocks, paths, and commands must be 100% correct and complete.
- **Concise structure**: One-liner for simple questions, short paragraphs for explanations.
- **Ask when ambiguous**: If the request has multiple valid interpretations, ask before exploring broadly.

## Verification
- Always propose a way to verify the change works
- Prefer executable checks (tests, lint, compile) over diff-only validation
- If tests exist, use them. If not, suggest a minimal verification command
- After a successful validation, only proceed to adjacent edits if needed