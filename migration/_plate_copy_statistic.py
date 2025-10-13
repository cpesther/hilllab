# Christopher Esther, Hill Lab, 9/25/2025

def plate_copy_statistic(bundle, columns_include=[], table='eta', 
                         value='mean', format='column'):

    """
    Copies one selected statistic from the summary tables for a selected 
    range of columns to the clipboard for pasting into Excel or 
    another analysis software.

    ARGUMENTS:
        bundle (migration.Bundle): the bundle with results
        columns_include (list): list of integers of the numbers of the columns 
            for which data should be copied.
        table (string): the table from which the data should be copied. 
            Acceptable values include either 'eta' or 'D'. 
        value (string): the value/statistic that should be copied. 
            Acceptable values include 'Median', 'Mean', 'Weighted Mean', 
            'Final 8hr Mean', 'CV', 'Minimum', 'Maximum', or 'Outliers'. 
        format (string): either 'column' or 'row' controlling how the 
            results are formatted when pasted. 
    """

    # Create the full column names for easier pulling
    if len(columns_include) == 0:
        full_cols = bundle.data.clean.columns
    else:
        full_cols = []
        for column in columns_include: 
            full_cols.append(f'Column {column}')
    
    # Check that the requested value actually exists
    if value not in bundle.results.plate_summary_eta.index:
        pass
    else:
        console.print('ERROR: Unrecognized value!', style=c_red)
        console.print(f'Acceptable values include {results.plate_summary_eta.index.to_numpy()}',
                      highlight=False, style=c_subtle)
        raise StopExecution()
    
    # Now navigate to the correct requested table
    if table == 'eta':
        copy_values = results.plate_summary_eta[full_cols].loc[value].to_numpy()
    
    elif table == 'D':
        copy_values = results.plate_summary_D[full_cols].loc[value].to_numpy()
    
    else:
        console.print('ERROR: Unrecognized table!', style=c_red)           

    # Create the copy dataframe based on the provided format argument
    if format == 'column':
        copy_df = pd.DataFrame({'values': copy_values})
    else:
        copy_df = pd.DataFrame([copy_values])

    # Copy the df to the clipboard without headers or index
    copy_df.to_clipboard(excel=True, header=False, index=False)

    console.print('Statistics copied to clipboard!', style=c_green)
    console.print('They can now be pasted into Excel or another tabular software.', style=c_subtle)
    return
