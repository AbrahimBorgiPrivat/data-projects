using System;
using System.Collections.Generic;
using System.Linq;
using System.Text; 

namespace TabularEditorCLITool
{
    public static class MCodeTableBuilder
    {
        public static void Create(
            dynamic model,
            string tableName,
            string mCode,
            List<string[]> columns,
            string description = null)
        {
            bool createdTempDS = false;
            if (((IEnumerable<dynamic>)model.DataSources).Count() == 0)
            {
                model.AddDataSource("TEMP. DATASOURCE");
                createdTempDS = true;
            }
            var tables = ((IEnumerable<dynamic>)model.Tables).ToList();
            var existing = tables.FirstOrDefault(t => t.Name == tableName);
            if (existing != null)
            {
                existing.Delete();
                try
                {
                    Console.WriteLine($"Deleted existing table '{tableName}'.");
                }
                catch { }
            }
            var table = model.AddTable(tableName);
            table.AddMPartition("MPART " + tableName, mCode);
            table.Description = description ?? mCode;
            try { table.Partitions[0].Delete(); } catch { }
            foreach (var col in columns)
            {
                var column = table.AddDataColumn(col[0]);
                if (!string.IsNullOrEmpty(col[1]))
                {
                    try
                    {
                        column.DataType = Enum.Parse(column.DataType.GetType(), col[1]);
                    }
                    catch
                    {
                        try { column.DataType = col[1]; } catch { }
                    }
                }
            }
            if (createdTempDS)
            {
                try { model.DataSources[0].Delete(); } catch { }
            }

            Console.WriteLine($"Created M table '{tableName}' successfully.");
        }
        public static string BuildMCode(
            List<string[]> rows,
            Dictionary<string, string> typedColumns)
        {
            var sb = new StringBuilder();
            var columns = typedColumns.Keys.ToList();
            sb.AppendLine("let");
            sb.AppendLine("    Source = Table.FromRows({");
            for (int i = 0; i < rows.Count; i++)
            {
                var rowValues = rows[i];
                if (rowValues.Length != typedColumns.Count)
                    throw new Exception($"Row {i + 1} has {rowValues.Length} values, but expected {typedColumns.Count} based on typedColumns definition.");
                var formattedValues = rowValues.Select(v => v == null ? "null" : long.TryParse(v, out _) ? v : $"\"{v.Replace("\"", "\"\"")}\"");
                sb.AppendLine($"        {{ {string.Join(", ", formattedValues)} }}{(i < rows.Count - 1 ? "," : "")}");
            }
            sb.AppendLine($"    }},");
            sb.AppendLine($"    {{ {string.Join(", ", columns.Select(c => $"\"{c}\""))} }}),");

            var typeMappings = string.Join(",\n        ",
                typedColumns.Select(kvp => $"{{\"{kvp.Key}\", {kvp.Value}}}"));
            sb.AppendLine($"    change_type = Table.TransformColumnTypes(Source, {{\n        {typeMappings}\n    }})");
            sb.AppendLine("in");
            sb.AppendLine("    change_type");
            return sb.ToString();
        }
    }
}