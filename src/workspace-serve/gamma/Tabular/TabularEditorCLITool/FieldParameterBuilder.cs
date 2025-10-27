using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class FieldParameterBuilder
    {
        public static dynamic Create(dynamic model, string tableName, List<string[]> entries, string? description = null)
        {
            // Delete existing table if it already exists
            var tables = ((IEnumerable<dynamic>)model.Tables).ToList();
            var existing = tables.FirstOrDefault(t => t.Name == tableName);
            if (existing != null)
                existing.Delete();

            // Build the DAX expression for the calculated table
            var lines = new List<string>();
            for (int i = 0; i < entries.Count; i++)
            {
                var e = entries[i];
                lines.Add(string.Format("(\"{0}\", NAMEOF('{1}'[{2}]), {3})", e[0], e[1], e[2], i));
            }

            var dax = "{\n" + string.Join(",\n    ", lines) + "\n}";
            var table = model.AddCalculatedTable(tableName, dax);
            table.Description = description ?? dax;

            // Add calculated columns
            var nameCol  = table.AddCalculatedTableColumn("Name",  "[Value1]");
            var fieldCol = table.AddCalculatedTableColumn("Field", "[Value2]");
            var orderCol = table.AddCalculatedTableColumn("Order", "[Value3]");

            // Configure sorting and grouping
            nameCol.SortByColumn = orderCol;
            nameCol.GroupByColumns.Add(fieldCol);

            fieldCol.SortByColumn = orderCol;
            fieldCol.SetExtendedProperty("ParameterMetadata", "{\"version\":3,\"kind\":2}", 1); // 1 = ExtendedPropertyType.Json
            fieldCol.IsHidden = true;
            orderCol.IsHidden = true;

            return table;
        }
    }
}
