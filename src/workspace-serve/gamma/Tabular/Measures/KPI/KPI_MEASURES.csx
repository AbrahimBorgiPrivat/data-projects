#r "netstandard"
#r ".\src\workspace-serve\gamma\Tabular\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES - CUSTOM");
var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\gamma\Tabular\Measures\KPI\MEASURES";
var measureList = new List<string[]> {
    new[] { "REALISERET",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "REALISERET.dax")).Replace("\"", "\"\""),
            "KPI ", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "REALISERET - SPLY",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "REALISERET - SPLY.dax")).Replace("\"", "\"\""),
            "KPI ", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "FORECAST",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "FORECAST.dax")).Replace("\"", "\"\""),
            "KPI ", "",MeasureBuilder.FormatStrings["danish_currency"],"true" },
    new[] { "FORECAST - W.O. FILTER",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "FORECAST - W.O. FILTER.dax")).Replace("\"", "\"\""),
            "KPI ", "",MeasureBuilder.FormatStrings["danish_currency"],"true" }
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
