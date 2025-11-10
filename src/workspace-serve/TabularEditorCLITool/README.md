# TabularEditorCLITool – Helper Library for Tabular Editor Automation

This project is a reusable **C# class library** designed to extend the scripting capabilities of **Tabular Editor 2**.  
It provides dynamic helper classes for building, modifying, and maintaining **Tabular models** programmatically.

---

## Purpose

`TabularEditorCLITool` contains reusable builder utilities that simplify common automation tasks in Tabular Editor, including:

- Creating and formatting **measures**
- Building **calculated tables** and **field parameter tables**
- Managing **calculation groups**
- Defining **relationships** between tables dynamically
- Creating **Power Query (M)** based tables

Each builder class uses **`dynamic`** typing to work directly with Tabular Editor’s in-memory model objects, without requiring access to hidden SDK assemblies.

---

## Folder Structure

```
TabularEditorCLITool/
│
├─ CalculatedTableBuilder.cs      # Create DAX-based calculated tables
├─ CalculationGroupBuilder.cs     # Create and populate calculation groups
├─ FieldParameterBuilder.cs       # Create field parameter tables
├─ MCodeTableBuilder.cs           # Create Power Query (M) tables
├─ MeasureBuilderClass.cs         # Create and format measures dynamically
├─ RelationshipBuilder.cs         # Create or update relationships
└─ TabularEditorCLITool.csproj    # Project definition file
```

---

## Requirements

### 1. .NET SDK
You need the **.NET 8 SDK (x64)** to build this library.

Download from: [https://dotnet.microsoft.com/en-us/download/dotnet/8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Verify installation:
```powershell
dotnet --version
```

### 2. Tabular Editor 2
The library is intended for use with **Tabular Editor 2 (v2.27 or newer)**.

Install from: [https://tabulareditor.com/](https://tabulareditor.com/)

Default installation path:
```
C:\Program Files (x86)\Tabular Editor\TabularEditor.exe
```

---

## Build Instructions

1. Navigate to the project folder:
   ```powershell
   cd "src\workspace-serve\Semantic Model\TabularScripts\TabularEditorCLITool"
   ```

2. Build the DLL:
   ```powershell
   dotnet build -c Release
   ```

3. The compiled DLL will be located here:
   ```text
   TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll
   ```

---

## Usage in Tabular Editor Scripts

Reference the compiled DLL from any `.csx` script executed through Tabular Editor CLI or GUI.

### Example:

```csharp
#r "netstandard"
#r ".\src\workspace-serve\TabularEditorCLITool.dll"
using TabularEditorCLITool;

// Create or find a table
var calcTable = MeasureBuilder.CheckTable(Model, "_MEASURES - CUSTOM");

// Define measures
var measureList = new List<string[]> {
    new[] { "Revenue", "[Sales]", "Financials", "", MeasureBuilder.FormatStrings["danish_currency"], "true" },
    new[] { "Margin %", "DIVIDE([Profit],[Sales])", "Financials", "", MeasureBuilder.FormatStrings["percent"], "true" }
};

// Add measures to the model
MeasureBuilder.AddMultipleFormattedMeasures(Model, calcTable, measureList);
```

### Run the script from PowerShell:

```powershell
& "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe" `
  ".\src\workspace-serve\Semantic Model\Finans.SemanticModel\definition\model.tmdl" `
  -S ".\src\workspace-serve\Semantic Model\TabularScripts\Measures\Financials\MEASURES.csx" -D
```

---

## Helper Classes Overview

| Class | Description |
|--------|--------------|
| **MeasureBuilder** | Create and format measures with custom folders, descriptions, and formats |
| **CalculationGroupBuilder** | Build and populate calculation groups dynamically |
| **FieldParameterBuilder** | Create field parameter tables for dynamic visuals |
| **MCodeTableBuilder** | Create tables using Power Query (M) code |
| **CalculatedTableBuilder** | Create calculated tables from DAX expressions |
| **RelationshipBuilder** | Create or update relationships between tables |

All methods are designed to work dynamically inside Tabular Editor scripts, without static type dependencies.

---

## Example: Building a Calculated Table

```csharp
using TabularEditorCLITool;

var entries = new List<string[]>
{
    new[] { "Product A", "100", "TRUE" },
    new[] { "Product B", "200", "FALSE" }
};

var colNames = new List<string> { "Product", "Quantity", "Active" };
var formats  = new List<string> { "String", "Int64", "Boolean" };

CalculatedTableBuilder.Create(Model, "_CALC - Products", entries, colNames, formats, "Example calculated table");
```

---

## Notes

- The library uses **dynamic reflection** to resolve Tabular Editor’s internal enums (e.g., `DataType`, `ExtendedPropertyType`) at runtime.
- This makes it version-tolerant across Tabular Editor 2 builds.
- No reference to `TabularEditor.TOMWrapper.dll` is required.

---

## License

It is provided for internal use and automation of semantic model management in **Tabular Editor 2**.