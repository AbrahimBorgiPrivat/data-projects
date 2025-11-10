using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class MeasureBuilder
    {
        public static readonly Dictionary<string, string> FormatStrings = new()
        {
            ["danish_currency"] = "#,0\\ \"kr.\";-#,0\\ \"kr.\";#,0\\ \"kr.\"",
            ["danish_currency_dec"] = "#,0.00\\ \"kr.\";-#,0.00\\ \"kr.\";#,0.00\\ \"kr.\"",  // With decimals
            ["decimal_point"] = "0.00",
            ["decimal_integer"] = "0",
            ["percent"] = "0 %;-0 %;0 %",
            ["percent_dec"] = "0.00 %;-0.00 %;0.00 %",
            ["whole_number"] = "#,0",
            ["number_with_2_dec"] = "#,0.00",
            ["number_with_1_dec"] = "#,0.0",
            ["scientific"] = "0.00E+00",
            ["date_short"] = "dd-MM-yyyy",
            ["date_long"] = "dddd, d. MMMM yyyy",
            ["datetime"] = "dd-MM-yyyy HH:mm",
            ["time_24hr"] = "HH:mm",
            ["time_12hr"] = "hh:mm tt",
            ["accounting"] = "_( #,0.00_);_( (#,0.00);_(-_);_(@_)",
            ["custom_text"] = "",
            ["boolean"] = "\"\"TRUE\";\"TRUE\";\"FALSE\"\"",
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
            string? dataCategory = null,
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
            if (!string.IsNullOrEmpty(dataCategory))
                meas.DataCategory = dataCategory;
        }

        public static void AddMultipleFormattedMeasures(dynamic model, dynamic table, List<string[]> measureList)
        {
            foreach (var entry in measureList)
            {
                string name        = entry[0];
                string expression  = entry[1];
                string folder      = entry[2];
                string description = string.IsNullOrEmpty(entry[3]) ? null : entry[3];
                string format = string.IsNullOrEmpty(entry[4]) ? null : entry[4];
                string dataCategory = (entry.Length > 5 && !string.IsNullOrEmpty(entry[5])) ? entry[5] : null;
                bool overwrite     = (entry.Length > 6 && !string.IsNullOrEmpty(entry[6])) ? bool.Parse(entry[6]) : true;

                AddFormattedMeasure(model, table, name, expression, folder, description, format, dataCategory, overwrite);
            }
        }
    }
}