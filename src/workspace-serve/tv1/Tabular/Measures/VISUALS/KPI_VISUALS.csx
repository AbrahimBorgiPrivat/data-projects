#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\tv1\Tabular\Measures\VISUALS\MEASURES";
var measureList = new List<string[]> {
    new[] { "PROGRAM IMAGE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "PROGRAM IMAGE.dax")),
            "VISUALS \\ URL IMG", "", null, "ImageUrl", "true" },
    new[] { "WATCHED TIME FORMATTED",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "WATCHED TIME FORMATTED.dax")),
            "VISUALS \\ TEXT", "",MeasureBuilder.FormatStrings["custom_text"],"true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
