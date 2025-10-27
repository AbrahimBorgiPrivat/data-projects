using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class MCodeTableBuilder
    {
        public static void Create(
            dynamic model,
            string tableName,
            string mCode,
            List<string[]> columns)
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
            try { table.Partitions[0].Delete(); } catch { }
            foreach (var col in columns)
            {
                var column = table.AddDataColumn(col[0]);
                if (!string.IsNullOrEmpty(col[1]))
                {
                    try
                    {
                        var dataTypeEnum = Enum.Parse(Type.GetType("TabularEditor.TOMWrapper.DataType, TabularEditor.TOMWrapper"), col[1]);
                        column.DataType = dataTypeEnum;
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
    }
}
