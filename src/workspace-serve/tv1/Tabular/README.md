# Tabular – Automation Toolkit for Tabular Editor

This folder contains the scripts and helper library used to automate and manage the Tabular model for the **TV1 - Reporting** project.

It includes:
- Custom Power BI / Tabular Editor scripts (`.csx` files)
- A reusable C# library **TabularEditorCLITool.dll** with helper classes that extend Tabular Editor’s scripting API

---

## 🧱 Folder Structure

```
workspace-serve/
│
├─ tv1/                   
│   ├─ SemanticModel/
│   │   └─ ... 
│   └─ Tabular/ # Folder containing KPI and DAX measure scripts
│       ├─ KPI_MEASURES.csx
│       └─ MEASURES/ 
│           ├─ FORMULA_ONE.dax
│           └─ ...
│
└─ TabularEditorCLITool/       # Compiled helper DLL project
    ├─ MeasureBuilderClass.cs
    ├─ CalculationGroupBuilder.cs
    ├─ FieldParameterBuilder.cs
    ├─ MCodeTableBuilder.cs
    ├─ RelationshipBuilder.cs
    ├─ TabularEditorCLITool.csproj
    └─ bin/Release/netstandard2.0/TabularEditorCLITool.dll
```

---

## ⚙️ Requirements

### 1. **.NET SDK**
Install the [.NET 8 SDK (x64)](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Verify installation:
```powershell
dotnet --version
```

### 2. **Tabular Editor 2**
Download and install [Tabular Editor 2 (v2.27 or newer)](https://tabulareditor.com/)

Make sure it’s available at:
```
C:\Program Files (x86)\Tabular Editor\TabularEditor.exe
```

---

## 🧩 Build the Helper Library

1. Navigate to the `TabularEditorCLITool` folder:
   ```powershell
   cd "src\workspace-serve\gamma\Tabular\TabularEditorCLITool"
   ```

2. Build the library:
   ```powershell
   dotnet build -c Release
   ```

3. The compiled DLL will be available here:
   ```
   src\workspace-serve\gamma\Tabular\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll
   ```

---

## 📦 How to "Install" / Use the Library

There’s no separate installation step.  
You simply reference the compiled DLL in any Tabular Editor `.csx` script like this:

```csharp
#r "netstandard"
#r ".\src\workspace-serve\gamma\Tabular\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;
```

Tabular Editor automatically loads the DLL when executing the script.

---

## 🧠 Provided Helper Classes

| Class | Purpose |
|-------|----------|
| `MeasureBuilder` | Create and format measures dynamically |
| `CalculationGroupBuilder` | Create calculation groups and items |
| `FieldParameterBuilder` | Create field parameter tables |
| `MCodeTableBuilder` | Create physical tables from M (Power Query) code |
| `RelationshipBuilder` | Create or update relationships between tables |

All builders are written using `dynamic` types, so they work directly with Tabular Editor’s in-memory model objects.

---

## ▶️ Example: Running a Measure Creation Script

Example: `KPI_MEASURES.csx`

```csharp
#r "netstandard"
#r ".\src\workspace-serve\gamma\Tabular\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES - CUSTOM");

var basePath = System.Environment.CurrentDirectory + @".\src\workspace-serve\gamma\Tabular\Measures\KPI\MEASURES";

var measureList = new List<string[]> {
    new[] { "REALISERET",
            System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "REALISERET.dax")).Replace("\"", "\"\""),
            "KPI \\ REALISERET", "",
            MeasureBuilder.FormatStrings["danish_currency"], "true" }
};

MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
```

### Run it from PowerShell:

```powershell
& "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe" `
  ".\src\workspace-serve\gamma\GamMa - Reporting.SemanticModel\definition\model.tmdl" `
  -S ".\src\workspace-serve\gamma\Tabular\Measures\KPI\KPI_MEASURES.csx" -D
```

### What happens:
1. The script loads `TabularEditorCLITool.dll`.
2. It ensures the `_MEASURES - CUSTOM` table exists.
3. It reads the DAX definition from `REALISERET.dax`.
4. It creates or overwrites the `[REALISERET]` measure inside your model.

---

## 🧰 Common Paths & Tips

| Path | Description |
|------|--------------|
| `src\workspace-serve\gamma\Tabular\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll` | Compiled helper library |
| `src\workspace-serve\gamma\Tabular\Measures\KPI\KPI_MEASURES.csx` | Example automation script |
| `src\workspace-serve\gamma\Tabular\Measures\KPI\REALISERET.dax` | DAX source file for the measure |

**Tip:**  
Always use relative paths when running from your project root (`GamMa - Reporting`) so the script remains portable across environments.

---

## 🔍 Troubleshooting

| Issue | Cause | Fix |
|--------|--------|-----|
| `CS0012: Typen 'System.Object' er defineret i en assembly, der ikke refereres til` | Tabular Editor’s script runtime needs the .NET Standard bridge | Add `#r "netstandard"` before referencing the DLL |
| `Stien må ikke være en tom streng` | The script was run from the GUI and no working directory was set | Use `Directory.GetCurrentDirectory()` or pass `-D` parameters in CLI |
| Build errors in Visual Studio Code | Missing SDK | Install .NET 8 SDK and reopen the terminal |

---

## 📜 License

This code is part of the GamMa - Reporting project and is provided for internal use and demonstration.