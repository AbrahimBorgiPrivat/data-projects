#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\tv1\Tabular\Measures\KPI\MEASURES";
var measureList = new List<string[]> {
    new[] { "SESSIONS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SESSIONS.dax")),
            "KPI \\ SESSIONS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "MINUTES WATCHED - AVG",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MINUTES WATCHED - AVG.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["decimal_integer"],"true" },
    new[] { "MINUTES WATCHED",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MINUTES WATCHED.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["decimal_integer"],"true" },
        // SESSIONS \\ STREAMING MEASURES
    new[] { "SESSIONS KPI",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SESSIONS KPI.dax")),
            "KPI \\ SESSIONS \\ STREAMING", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "STREAMING SESSIONS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "STREAMING SESSIONS.dax")),
            "KPI \\ SESSIONS \\ STREAMING", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "STREAMING SESSIONS - TARGET",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "STREAMING SESSIONS - TARGET.dax")),
            "KPI \\ SESSIONS \\ STREAMING", "",MeasureBuilder.FormatStrings["percent"],"true" },
    new[] { "STREAMING SESSIONS PERC",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "STREAMING SESSIONS PERC.dax")),
            "KPI \\ SESSIONS \\ STREAMING", "",MeasureBuilder.FormatStrings["percent"],"true" },
        //SESSIONS \\ EPISODES MEASURES
    new[] { "EPISODES WATCHED PR. SESSION",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "EPISODES WATCHED PR. SESSION.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["decimal_integer"],"true" },
    new[] { "EPISODES WATCHED TO END PERC",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "EPISODES WATCHED TO END PERC.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["percent"],"true" },
    new[] { "EPISODES WATCHED TO END",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "EPISODES WATCHED TO END.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "EPISODES WATCHED",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "EPISODES WATCHED.dax")),
            "KPI \\ SESSIONS \\ EPISODES", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
        // USERS MEASURES
    new[] { "USERS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "USERS.dax")),
            "KPI \\ USERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "ACTIVE USERS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "ACTIVE USERS.dax")),
            "KPI \\ USERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "ACTIVE USERS PERC",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "ACTIVE USERS PERC.dax")),
            "KPI \\ USERS", "",MeasureBuilder.FormatStrings["percent"],"true" }

};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
