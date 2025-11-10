using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class CalculatedTableBuilder
    {
        private static string FormatValue(string input, string formatType)
        {
            if (string.IsNullOrEmpty(input))
                return "\"\"";

            string safe = input.Replace("\"", "\\\"");

            switch (formatType.ToLower())
            {
                case "int64":
                case "double":
                case "decimal":
                    return double.TryParse(input, out _) ? input : "0";

                case "boolean":
                    return (input.ToLower() == "true" || input == "1") ? "TRUE" : "FALSE";

                default:
                    return "\"" + safe + "\"";
            }
        }

        private static void AddColumnWithType(dynamic model, string tableName, string colName, string formatType, string daxExpression)
        {
            var table = ((IEnumerable<dynamic>)model.Tables).FirstOrDefault(t => t.Name == tableName);
            if (table == null)
            {
                Console.WriteLine($"Table '{tableName}' not found when adding column '{colName}'.");
                return;
            }
            var col = table.AddCalculatedColumn(colName, daxExpression);
            try {
                var asm = model.GetType().Assembly;
                var enumType = asm.GetType("TabularEditor.TOMWrapper.DataType");

                if (enumType != null)
                {
                    // Make sure we treat it as a string[] instead of dynamic
                    string[] names = (string[])Enum.GetNames(enumType);

                    string match = names
                        .FirstOrDefault(n => string.Equals(n, formatType, StringComparison.OrdinalIgnoreCase));

                    if (match != null)
                        col.DataType = Enum.Parse(enumType, match, true);
                    else
                        col.DataType = Enum.Parse(enumType, "String");
                }
            }
            catch {
                try { col.DataType = formatType; } catch { }
            }
        }
        public static dynamic Create(
            dynamic model,
            string tableName,
            List<string[]> entries,
            List<string> colNames,
            List<string> formats,
            string description = null)
        {
            if (formats.Count != colNames.Count)
                throw new Exception("colNames must have the same number of elements as formats.");

            var tables = ((IEnumerable<dynamic>)model.Tables).ToList();
            var existing = tables.FirstOrDefault(t => t.Name == tableName);
            if (existing != null)
            {
                existing.Delete();
                Console.WriteLine($"Deleted existing table '{tableName}'.");
            }

            List<string> lines = new();
            for (int i = 0; i < entries.Count; i++)
            {
                string[] rowValues = entries[i];
                if (rowValues.Length > colNames.Count)
                    throw new Exception("Row has more columns than colNames.");

                var formatted = rowValues.Select((v, idx) => FormatValue(v, formats[Math.Min(idx, formats.Count - 1)]));
                string row = "(" + string.Join(", ", formatted) + ")";
                lines.Add(row);
            }
            var dax = "{\n" + string.Join(",\n    ", lines) + "\n}";
            var table = model.AddCalculatedTable(tableName, dax);
            table.Description = description ?? dax;

            for (int i = 0; i < colNames.Count; i++)
            {
                string colName = colNames[i];
                string formatType = formats[i];
                AddColumnWithType(model, tableName, colName, formatType, $"[Value{i + 1}]");
            }

            Console.WriteLine($"Created calculated table '{tableName}' with {colNames.Count} columns.");
            return table;
        }
    }
}