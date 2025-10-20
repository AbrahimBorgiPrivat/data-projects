import csv
from libraries.utils import path_config
from pathlib import Path

def convert_csv_to_dict(
    path: Path | str,
    delimiter: str | None = "\t",
    subset: list[str] | None = None,
):
    path = Path(path_config.RES_PATH / path)
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open("r", encoding=enc, newline="") as f:
                sample = f.read(4096)
                f.seek(0)
                delim = delimiter
                if delim is None:
                    try:
                        dialect = csv.Sniffer().sniff(sample, delimiters="\t;,")
                        delim = dialect.delimiter
                    except Exception:
                        delim = "\t"
                reader = csv.DictReader(f, delimiter=delim)
                rows = []
                for row in reader:
                    clean = {
                        (k or "").strip(): (v or "").strip()
                        for k, v in row.items() if k
                    }
                    if subset is not None:
                        clean = {k: clean.get(k, "") for k in subset}
                    rows.append(clean)
                return rows
        except UnicodeDecodeError:
            continue
    raise RuntimeError(
        "Kunne ikke læse filen med utf-8/cp1252/latin-1. "
        "Prøv at åbne filen i Notepad og gem som UTF-8, eller send et eksempel på filen."
    )

