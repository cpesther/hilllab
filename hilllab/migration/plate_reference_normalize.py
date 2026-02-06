# Christopher Esther, Hill Lab, 2/6/2026

def plate_reference_normalize(bundle, reference_columns, reference_eta):

    """
    Normalizes the data in a bundle using reference column(s) with a known
    eta value by adjusting the radius. 

    ARGUMENTS:
        bundle (migration.Bundle): the data bundle after processing
        reference_columns (list): the numbers of the columns containing
            the reference capillaries.
        reference_eta (float): the viscosity of the reference columns 
            in millipascal seconds (mPa•s)

    RETURNS:
        output_bundle (migration.Bundle): the bundle with the included
            normalized data. 
    """

    # Print a warning and ask for confirmation before proceeding
    print('ALERT: This function only works on plates where every column' \
    'uses a probe of the same radius and contains at least one reference ' \
    'column with a known eta.')
    confirmation = input('Ready to proceed? [y]/n: ')

    if (confirmation.upper() != 'Y') or (confirmation != ''):
        raise ValueError('Confirmation not accepted')
