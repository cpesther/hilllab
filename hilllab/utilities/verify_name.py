# Christopher Esther, Hill Lab, 5/18/2026
from difflib import get_close_matches
from .warning import warn

def verify_name(name, valid_names, cutoff=0.8, print_output=True):

    """
    Checks whether a name (often variable) is in a list of valid ones. 
    Returns true if so, if not present, returns false and provides 
    name suggestions via fuzzy matching, if possible. 

    ARGUMENTS:
        name (string): the user-provided name to be verified
        valid_names (list): a list of valid strings 
        cutoff (float): the matching cutoff used in fuzzy search
        print_output (bool): if true, function will throw warnings suggesting
            other possible valid names in the case of a mismatch
    """

    # Check if provided name is in the list of valid names
    if name in valid_names:
        return True

    # Otherwise go through our resolution logic
    else:
        
        # Find close match from list of provided names
        matches = get_close_matches(name, valid_names, n=5, cutoff=cutoff)

        # If printing the output, create the message
        if print_output:
        
            if len(matches) == 0:
                matched_list = ', '.join(f"'{n}'" for n in valid_names)
                message = f"'{name}' is not a valid value. \n\nPlease try one of the following:\n{matched_list}"
                warn(msg=message)
        
            elif len(matches) == 1:
                message = f"'{name}' is not a valid value. Perhaps you meant {matches[0]}?"
                warn(msg=message)
        
            else:
                matched_list = '\n'.join(matches)
                message = f"'{name}' is not a valid value. \n\nPerhaps you meant one of the following:\n{matched_list}"
                warn(msg=message)

        # Return false, since we coulnd't verify the current input
        return False
