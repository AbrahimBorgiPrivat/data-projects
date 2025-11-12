#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var tableName = "_PARAMETER - MEASURES";
var entries = new List<string[]> {
    // --- Sessions ---
    new[] { "Sessioner", "_MEASURES", "SESSIONS" },
    new[] { "Minutter pr. Session", "_MEASURES", "MINUTES WATCHED - AVG" },
    new[] { "Minutter Total", "_MEASURES", "MINUTES WATCHED" },
    // --- Streaming ---
    new[] { "Streaming Sessioner", "_MEASURES", "STREAMING SESSIONS" },
    new[] { "Andel Streaming Sessioner", "_MEASURES", "STREAMING SESSIONS PERC" },
    // --- Episoder ---
    new[] { "Episoder pr. Session", "_MEASURES", "EPISODES WATCHED PR. SESSION" },
    new[] { "Andel Færdigsete Episoder", "_MEASURES", "EPISODES WATCHED TO END PERC" },
    new[] { "Færdigsete Episoder", "_MEASURES", "EPISODES WATCHED TO END" },
    new[] { "Sete Episoder", "_MEASURES", "EPISODES WATCHED" },
    // --- Brugere ---
    new[] { "Brugere", "_MEASURES", "USERS" },
    new[] { "Aktive Brugere", "_MEASURES", "ACTIVE USERS" },
    new[] { "Andel Aktive Brugere", "_MEASURES", "ACTIVE USERS PERC" },
};

FieldParameterBuilder.Create(Model, tableName, entries);
Info("Table created: " + tableName);