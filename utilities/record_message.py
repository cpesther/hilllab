# Christopher Esther, 08/15/2025
from datetime import datetime
from IPython.display import clear_output

def record_message(message, active=True, print_message=True, print_time=True,
                   clear_print=False):

    """
    Saves a user-provided message to a CSV log file in the app data 
    folder of the system. Should only used during monitoring/development.

    ARGUMENTS:
        message (str): the message to be added to the log file.
        active (bool): allows us to "turn off" writing easily when
            incorporated into other functions without needing to nest 
            this function within a conditional.
        print_message (bool): controls whether the message is also 
            printed to the console. Useful to avoid needing both this
            function and a print statement to display a message. This
            arg is not affected by the active argument. Defaults to False.
    """

    if active:

        # Import the path to the log file
        from . import LOG_FILE_PATH

        # Open the log file and write the message
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(f'{str(datetime.now().timestamp())},{message}\n')

    if clear_print:
        try:
            clear_output(wait=True)
        except:
            pass

    if print_message:

        if print_time:
            time_value = str(datetime.now().time().replace(microsecond=0))
            print(f'[{time_value}] {message}')
        
        else:
            print(message)

