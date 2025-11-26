% Christopher Esther, Hill Lab, 10/1/2025

function print_message(text)
    % Generic function for writing messages to terminal in a nicely
    % formatted manner. 

   
    logtime = datetime('now');
    logtimetext = sprintf('[%s]', string(logtime, 'HH:mm:ss'));
    headertext = string(logtimetext) + ": ";
    fprintf('%s%s\n', headertext, text);
end