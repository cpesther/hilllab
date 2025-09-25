# Christopher Esther, Hill Lab, 8/29/2025
import os
from pathlib import Path
import time
import pandas as pd

def plate_export_bundle(bundle):
    
    """Exports all of the values stored in a bundle object to an Excel
    file for easier manual editing.
    
    ARGUMENTS:
        bundle (migration.Bundle): the bundle object to be saved
    """
    
    file_name = f'{Path(bundle.data.path).stem}.1dpre.xlsx'
    full_path = os.path.join(os.path.dirname(bundle.data.path), file_name)

    # Skip export if a bundle has already been exported
    if os.path.exists(full_path):
        print('ALERT: Bundle already exists. Did not export a new one')
        return 

    # Otherwise write everything to an Excel file
    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:

        # Write in a little warning on the first page
        warning_text = """This .1dpre.xlsx file contains a full set of 1DMA experimental 
        data that has already been preprocessed. It is saved in this format to avoid repeating 
        preprocessing in the future. You are welcome to explore and copy from this file, but 
        altering its structure or modifying the data may make it incompatible with the 
        algorithm. Please proceed with caution."""
        warning = {'Warning!': warning_text}
        pd.DataFrame(warning, index=[0]).to_excel(writer, sheet_name='warning', index=False)
        
        # The data itself
        bundle.data.raw.to_excel(writer, sheet_name='bundle.data.raw')
        bundle.data.normalized.to_excel(writer, sheet_name='bundle.data.normalized')
        bundle.data.clean.to_excel(writer, sheet_name='bundle.data.clean')
        bundle.data.average.to_excel(writer, sheet_name='bundle.data.average', index=False)

        # Profiling data
        bundle.data.peaks_raw.to_excel(writer, sheet_name='bundle.data.peaks_raw', index=False)
        bundle.data.peaks_final.to_excel(writer, sheet_name='bundle.data.peaks_final', index=False)
        bundle.data.ranges_raw.to_excel(writer, sheet_name='bundle.data.ranges_raw', index=False)
        bundle.data.ranges_final.to_excel(writer, sheet_name='bundle.data.ranges_final', index=False)

        # Package up and save the experimental conditions
        conditions = {
            'interval_minutes': [bundle.data.interval_minutes],
            'delay_minutes': [bundle.data.delay_minutes],
            'load_rate_minutes': [bundle.data.load_rate_minutes],
            'temperature_K': [bundle.data.temperature_K],
            'method': [bundle.data.method]
        }
        pd.DataFrame(bundle.data.radii_nm, index=[0]).to_excel(writer, sheet_name='bundle.data.radii_nm', index=False)
        pd.DataFrame(conditions).to_excel(writer, sheet_name='bundle.data.conditions', index=False)  # everything else

        # And the overflow metadata table
        bundle.data.overflow_meta.to_excel(writer, sheet_name='bundle.data.overflow_meta', index=False)

        # Package up and save the metadata
        metadata = {
            'path': [bundle.data.path],
            'extended': [bundle.data.extended],
            'num_columns': [bundle.data.num_columns],
            'num_rows': [bundle.data.num_rows],
            'num_reads': [bundle.data.num_reads]
        }
        pd.DataFrame(metadata, index=[0]).to_excel(writer, sheet_name='bundle.data.metadata')

        # Add some metadata regarding this preparation
        preparation_metadata = {
            'datetime_prepared': time.time(),
            'user_prepared': os.getlogin()
        }
        pd.DataFrame(preparation_metadata, index=[0]).to_excel(writer, sheet_name='preparation_metadata')
        
    print('Bundle export complete')
