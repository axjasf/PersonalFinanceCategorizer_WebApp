from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, AgGridTheme
import pandas as pd

def render_aggrid(dataframe: pd.DataFrame, key: str, height: int):
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gridOptions = gb.build()
    
    AgGrid(
        dataframe,
        gridOptions=gridOptions,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme=AgGridTheme.STREAMLIT,
        height=height,
        fit_columns_on_grid_load=True,
        key=key
    )
