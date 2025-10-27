using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class RelationshipBuilder
    {
        public static dynamic Create(
            dynamic model,
            string fromTableName,
            string fromColumnName,
            string fromCardinality,   // as string: "One" / "Many"
            string toTableName,
            string toColumnName,
            string toCardinality,     // as string: "One" / "Many"
            string crossFilter,       // as string: "Single" / "Both"
            bool isActive)
        {
            var fromTable = model.Tables[fromTableName];
            if (fromTable == null)
                throw new Exception("Table not found: " + fromTableName);

            var fromCol = fromTable.Columns[fromColumnName];
            if (fromCol == null)
                throw new Exception($"Column '{fromColumnName}' not found in {fromTableName}");

            var toTable = model.Tables[toTableName];
            if (toTable == null)
                throw new Exception("Table not found: " + toTableName);

            var toCol = toTable.Columns[toColumnName];
            if (toCol == null)
                throw new Exception($"Column '{toColumnName}' not found in {toTableName}");
            var relationships = ((IEnumerable<dynamic>)model.Relationships).ToList();
            foreach (var r in relationships)
            {
                if ((r.FromColumn == fromCol && r.ToColumn == toCol) ||
                    (r.FromColumn == toCol && r.ToColumn == fromCol))
                {
                    r.Delete();
                }
            }
            var rel = model.AddRelationship();
            rel.IsActive = isActive;
            rel.FromColumn = fromCol;
            rel.ToColumn = toCol;
            try { rel.FromCardinality = ParseEnumValue(model, "RelationshipEndCardinality", fromCardinality); } catch { }
            try { rel.ToCardinality = ParseEnumValue(model, "RelationshipEndCardinality", toCardinality); } catch { }
            try { rel.CrossFilteringBehavior = ParseEnumValue(model, "CrossFilteringBehavior", crossFilter); } catch { }

            Console.WriteLine($"Created relationship: {fromTableName}[{fromColumnName}] → {toTableName}[{toColumnName}]");
            return rel;
        }
        private static dynamic ParseEnumValue(dynamic model, string enumName, string valueName)
        {
            try
            {
                var asm = model.GetType().Assembly;
                var enumType = asm.GetType("TabularEditor.TOMWrapper." + enumName);
                if (enumType != null && Enum.IsDefined(enumType, valueName))
                    return Enum.Parse(enumType, valueName);
            }
            catch { }
            return valueName; 
        }
    }
}
