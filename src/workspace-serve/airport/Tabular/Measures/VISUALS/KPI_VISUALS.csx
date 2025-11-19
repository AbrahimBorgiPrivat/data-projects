#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\airport\Tabular\Measures\VISUALS\MEASURES";
var measureList = new List<string[]> {
    new[] { "COLOR CAPACITY RATE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "COLOR CAPACITY RATE.dax")),
            "VISUALS \\ COLORS", "", null, "custom_text", "true" },
    new[] { "COLOR DELAYED FLIGHTS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "COLOR DELAYED FLIGHTS.dax")),
            "VISUALS \\ COLORS", "", null, "custom_text", "true" },
    new[] { "COLOR SEAT VISUAL",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "COLOR SEAT VISUAL.dax")),
            "VISUALS \\ COLORS", "", null, "custom_text", "true" },
    new[] { "COLOR PASSENGER SEQURITY",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "COLOR PASSENGER SEQURITY.dax")),
            "VISUALS \\ COLORS", "", null, "custom_text", "true" },

    new[] { "MEDIAN CHECKIN UNTIL TRAVEL (TEXT)",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDIAN CHECKIN UNTIL TRAVEL (TEXT).dax")),
            "VISUALS \\ TEXT", "",MeasureBuilder.FormatStrings["custom_text"],"true" },
    new[] { "MEDIAN DELAY (TEXT)",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDIAN DELAY (TEXT).dax")),
            "VISUALS \\ TEXT", "",MeasureBuilder.FormatStrings["custom_text"],"true" },
    new[] { "MEDIAN SECURITY UNTIL TRAVEL (TEXT)",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "MEDIAN SECURITY UNTIL TRAVEL (TEXT).dax")),
            "VISUALS \\ TEXT", "",MeasureBuilder.FormatStrings["custom_text"],"true" },

    new[] { "SEATS VISUAL - NUMBER OF VALID SEATS",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL - NUMBER OF VALID SEATS.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "SEATS VISUAL MAX X VALUE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL MAX X VALUE.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "SEATS VISUAL MIN Y VALUE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL MIN Y VALUE.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "SEATS VISUAL SEATS PER ROW",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL SEATS PER ROW.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "SEATS VISUAL X VALUE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL X VALUE.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "SEATS VISUAL Y VALUE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SEATS VISUAL Y VALUE.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "TIDSREJSE X-AXIS BOARDER",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TIDSREJSE X-AXIS BOARDER.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
    new[] { "CONSTANT ONE",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "CONSTANT ONE.dax")),
            "VISUALS \\ NUMBERS", "",MeasureBuilder.FormatStrings["whole_number"],"true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
