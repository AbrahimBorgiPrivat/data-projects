using System;
using System.Collections.Generic;
using System.Linq;

namespace TabularEditorCLITool
{
    public static class CalculationGroupBuilder
    {
        public static void Create(dynamic model,
                                string groupName,
                                List<string[]> items,
                                string? description = null,
                                int? CalculationGroupPrecedence = null,
                                int? AlternateSourcePrecedence = null)
        {
            var calcGroups = ((IEnumerable<dynamic>)model.CalculationGroups).ToList();
            var existing = calcGroups.FirstOrDefault(g => g.Name == groupName);
            if (existing != null)
                existing.Delete();

            var calcGroup = model.AddCalculationGroup(groupName);
            calcGroup.Description = description ?? $"Calculation Group: {groupName}";
            calcGroup.CalculationGroupPrecedence = CalculationGroupPrecedence ?? 0;
            calcGroup.AlternateSourcePrecedence = AlternateSourcePrecedence ?? 0;

            foreach (var item in items)
            {
                string label = item[0];
                string expr  = item[1];
                calcGroup.AddCalculationItem(label, expr);
            }
        }
    }
}