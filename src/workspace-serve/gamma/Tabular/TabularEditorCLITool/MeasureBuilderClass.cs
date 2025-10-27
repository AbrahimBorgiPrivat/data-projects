using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class MeasureBuilder
    {
        public static readonly Dictionary<string, string> FormatStrings = new()
        {
            ["danish_currency"] = "#,0.00\\ \"kr.\";-#,0.00\\ \"kr.\";#,0.00\\ \"kr.\"",
            ["decimal_point"]   = "0.00",
            ["percent"]         = "0.##%"
        };

        public static dynamic CheckTable(dynamic model, string tableName)
        {
            var tables = ((IEnumerable<dynamic>)model.Tables).ToList();
            var table  = tables.FirstOrDefault(t => t.Name == tableName);
            if (table == null)
                table = model.AddCalculatedTable(tableName, "SELECTCOLUMNS({}, \"DoNotUse\", 1)");
            return table;
        }

        public static void AddFormattedMeasure(
            dynamic model,
            dynamic table,
            string name,
            string expression,
            string folder,
            string? description = null,
            string? format = null,
            bool overwrite = true)
        {
            var measures = ((IEnumerable<dynamic>)model.AllMeasures).ToList();
            var existing = measures.FirstOrDefault(m => m.Name == name);
            if (existing != null)
            {
                if (overwrite) existing.Delete();
                else return;
            }

            var meas = table.AddMeasure(name, expression, folder);
            meas.Description = description ?? expression;
            if (!string.IsNullOrEmpty(format))
                meas.FormatString = format;
        }

        public static void AddMultipleFormattedMeasures(dynamic model, dynamic table, List<string[]> measureList)
        {
            foreach (var entry in measureList)
            {
                string name        = entry[0];
                string expression  = entry[1];
                string folder      = entry[2];
                string description = string.IsNullOrEmpty(entry[3]) ? null : entry[3];
                string format      = string.IsNullOrEmpty(entry[4]) ? null : entry[4];
                bool overwrite     = string.IsNullOrEmpty(entry[5]) ? true : bool.Parse(entry[5]);

                AddFormattedMeasure(model, table, name, expression, folder, description, format, overwrite);
            }
        }
    }
}
