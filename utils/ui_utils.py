from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, AgGridTheme

def render_aggrid(dataframe, key, height, selection_mode='multiple', update_mode=GridUpdateMode.MODEL_CHANGED, theme=AgGridTheme.STREAMLIT):
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode=selection_mode, use_checkbox=True)
    
    gridOptions = gb.build()
    
    return AgGrid(
        dataframe,
        gridOptions=gridOptions,
        enable_enterprise_modules=False,
        update_mode=update_mode,
        theme=theme,
        height=height,
        key=key
    )
