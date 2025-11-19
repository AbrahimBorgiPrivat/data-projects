#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var tableName = "_CUSTOMTABLE - NUMBERS";
List<string> colNames = new List<string>
{
    "SEATS"
};

List<string> formats = new List<string>
{
    "int64"
};

string dax = "GENERATESERIES(1,1000,1)"; 

Table calcTab = CalculatedTableBuilder.Create(
    model: Model,
    tableName: tableName,
    dax: dax,
    colNames: colNames,
    formats: formats
);
Info("Table created: " + tableName);