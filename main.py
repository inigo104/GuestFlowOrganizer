from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from airtable_app import get_combined_dataframe, generate_html_table

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def get_table():
    combined_df = get_combined_dataframe()
    table_html = generate_html_table(combined_df)

    return f'''
    <html>
    <head>
        <style>
            table {{border-collapse: collapse; table-layout: fixed; width: 100%;}}
            th, td {{border: 1px solid black; padding: 8px; overflow: hidden;}}
            th {{background-color: #f2f2f2; position: sticky; top: 0;}}
        </style>
        <script>
            function toggleEmptyRows() {{
                var checkBox = document.getElementById("hideEmptyRows");
                var rows = document.querySelectorAll("tr");
                rows.forEach(row => {{
                    var hourCell = row.cells[1]; // La columna 'Hora' es la segunda columna (índice 1)
                    if (hourCell && hourCell.innerHTML.trim() === "") {{
                        row.style.display = checkBox.checked ? "none" : "table-row";
                    }}
                }});
            }}
        </script>
    </head>
    <body>
        <label>
            <input type="checkbox" id="hideEmptyRows" onclick="toggleEmptyRows()" checked>
            Ocultar filas con 'Hora' vacía
        </label>
        <a href="/combined_data.csv" download="combined_data.csv">Descargar CSV</a>
        {table_html}
    </body>
    </html>
    '''

@app.get('/combined_data.csv', response_class=FileResponse)
async def get_combined_data_csv():
    return FileResponse('combined_data.csv', media_type='text/csv', filename='combined_data.csv')