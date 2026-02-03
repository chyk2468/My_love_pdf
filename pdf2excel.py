import tabula
import pandas as pd
from io import BytesIO

def pdf_to_excel(file, tables_only):
    output = BytesIO()
    
    lattice = True if tables_only else False
    stream = not lattice
    
    try:
        dfs = tabula.read_pdf(file, pages='all', lattice=lattice, stream=stream, multiple_tables=True)
    except Exception:
        file.seek(0)
        dfs = []
        
    if not dfs:
        df = pd.DataFrame(["No tables found"])
        dfs = [df]

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, df in enumerate(dfs):
            sheet_name = f"Table_{i+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
    output.seek(0)
    return output
