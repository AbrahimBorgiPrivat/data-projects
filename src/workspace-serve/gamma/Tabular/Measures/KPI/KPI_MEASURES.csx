#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES - CUSTOM");
var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\gamma\Tabular\Measures\KPI\MEASURES";
var measureList = new List<string[]> {
    new[] { "REALISERET",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "REALISERET.dax")),
            "KPI \\ REALISERET", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "REALISERET - SPLY",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "REALISERET - SPLY.dax")),
            "KPI \\ REALISERET", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "FORECAST",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "FORECAST.dax")),
            "KPI \\ FC", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "FORECAST - NOT BU",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "FORECAST - NOT BU.dax")),
            "KPI \\ FC", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "MEDLEMSBETALINGER",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDLEMSBETALINGER.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "MEDLEMSBETALINGER YTD",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDLEMSBETALINGER YTD.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "MEDLEMSBETALINGER - SPLY",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDLEMSBETALINGER - SPLY.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "MEDLEMSBETALINGER YTD - SPLY",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDLEMSBETALINGER YTD - SPLY.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "NEW_REWON MEMBERS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "NEW_REWON MEMBERS.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "NEW_REWON MEMBERS - YTD",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "NEW_REWON MEMBERS - YTD.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "RESIGNING_MEMBERS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "RESIGNING_MEMBERS.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "RESIGNING_MEMBERS - YTD",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "RESIGNING_MEMBERS - YTD.dax")),
            "KPI \\ MEDLEMMER", "",MeasureBuilder.FormatStrings["whole_number"],"true" }
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
