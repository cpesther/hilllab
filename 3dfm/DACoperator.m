% Christopher Esther, Hill Lab, 10/1/2025

function v = DACoperator(inputs, final_degauss, Nrepeat, board, channels, srate, Vrange)
% DACOPERATOR Sends an input vector to specified channels on a DAC board.
%
% Sends the input vector to specified channels on the specified DAC board. 
% Primarily used as the back-end for a custom signal generator UI.
%
% ARGUMENTS:
%   inputs   : M x N matrix of input samples (in Volts), with M samples per channel.
%   Nrepeat  : Number of times to repeat the input vector (default = 0).
%   board    : DAC board number, or 'daqtest' (default) for testing on systems without hardware.
%   channels : 1 x N vector of channel indices (default = 0:N-1).
%   srate    : Sampling rate in Hz (default = 10000).
%   Vrange   : 1 x 2 vector specifying voltage range for all channels (default = [-10 10]).
%
% RETURNS:
%   data     : The output data structure from the DAC operation.

% Check validity of arguments
if (nargin < 1 || isempty(inputs)) 
    error('DACoperator: Input matrix is empty or not provided');
else 
    [M, N] = size(inputs);
end

if (nargin < 2 || isempty(Nrepeat))  
    Nrepeat = 0;          
end

if (nargin < 3 || isempty(board))  
    board = 'daqtest';             
    logentry('No board specified.  Using virtual board "daqtest" as default');   
end

if (nargin < 4 || isempty(channels))   
    channels = 0:(N-1);  
    logentry(['DACoperator: Using default AO channels: 0 to ', num2str(N-1)]);
end

if (nargin < 5 || isempty(srate))   
    srate  = 10000;	
    logentry(['Sampling rate defaulted to ', num2str(srate), 'Hz']);
end

if (nargin < 6 || isempty(Vrange))   
    Vrange = [-5 5];	
    logentry(['DACoperator: Voltage range defaulted as ', num2str(Vrange(1)), ' to ', num2str(Vrange(2)), ' volts']);
end

if (N ~= length(channels))
    error('DACoperator: No of columns in input matrix does not match with no of channels');
end

% Calculate some initial waveform characteristics
waveform_period = (M - 1) / (srate - 1); 
full_period = waveform_period * (Nrepeat + 1);

% Print info to console
logentry(['Each waveform is ' num2str(waveform_period) ' seconds.']);
logentry(['The number of repeats is: ' num2str(Nrepeat)]);
logentry(['Full sequence period is: ' num2str(full_period) ' seconds.']);

% Clip data to remain within the specified voltage range
inputs = max(inputs, Vrange(1));  % clip to the lower bound
inputs = min(inputs, Vrange(2));  % and the upper bound

% Check for configured board
if strcmp(board, 'PCIe-6738')

    try
        % Get a list of available DAQ devices and extract model names
        dlist = daqlist;
        daqname = dlist.Model;

        % Verify that the detected device matches PCIe-6738
        if contains(daqname, 'PCIe-6738')
           
            logentry('Starting DAq.')             % Log start of DAQ session
            dq = daq('ni');                       % Create DAQ object for National Instruments hardware
            dq.Rate = srate;                      % Set DAQ sampling rate
            
            logentry('Adding channels.');         
            core_number = [1 2 3 4 5 6];          % Define core channel indices
            channel_ao(1,:) = ["ao0" "ao16" "ao6" "ao4" "ao2" "ao18"];  % Channel mapping (based on breakout box wiring)
            
            % Loop through channels and add them as voltage outputs
            for k = 1:size(core_number,2)
                ao(k) = addoutput(dq, "Dev2", channel_ao(k), "Voltage"); 
            end
            
            % Display configured DAQ channels
            logentry('Channels configured as ...'); 
            dq.Channels
            
            % Write data here
            start(dq,'repeatoutput');            % Start DAQ output in repeat mode
            start_time = postixtime(datetime('now'));  % Record start time in seconds since epoch
            write(dq, inputs);                   % Send input data (errors if hardware is in use by another DAQ object)
            pause(full_period + 0.1);            % Wait for signal duration plus 0.1s buffer
            logentry('Stopping Signal.');        
            stop(dq);                            % Stop DAQ output
            write(dq, final_degauss);            % Send final degaussing signal
            pause(0.5);                          % Short pause to ensure output finishes

            % Clean everything up and reset
            logentry('Zeroing and reseting DAq.');
            start(dq,'continuous');
            write(dq, zeros(srate/2,size(core_number,2)));  % send continuous zeroes
            pause(0.5);  % in seconds
            stop(dq);

            % Remove channels and reset the DAQ system
            removechannel(dq, 1:size(core_number,2));
            daqreset;
            logentry('The DAq board was reset.');

        else
            % Detected board is not PCIe-6738, use virtual board instead
            logentry('The DAq board is not PCIe-6738. Using daqtest.');
            board = 'daqtest';
        end
        
    % Handle errors during board detection or signal sending
    catch
        if contains(daqname, 'PCIe-6738')
            % PCIe-6738 detected but failed to send signal, fallback to virtual board
            logentry('Error sending signal with PCIe-6738. Defaulting to "daqtest".');
        else
            % No NI DAQ boards found, use virtual board
            logentry('No NI DAQ boards found. Defaulting to "daqtest" virtual board.');
        end
        board = 'daqtest';  % force to virtual board if any other error occurs
    end

% Handle user-specified or unrecognized board names
elseif strcmp(board, 'daqtest') 
    % User explicitly selected virtual test
    logentry('"daqtest" selected. Running virtual test.');
else
    % Board name does not match installed hardware, fallback to virtual board
    logentry('Board name does not match installed hardware. Defaulting to "daqtest" virtual board.');
    board = 'daqtest';
end

% Calculate some extra data and information
tend = (length(inputs)*(Nrepeat+1) + length(final_degauss) - 1) / (srate-1);  % duration of signal in seconds
t = (0:1/(srate-1):tend)';   % Column vector of time points
Nt = numel(t);               % Total number of time points

% Record start time if using virtual DAQ for testing
%if strcmp(board, 'daqtest')
%    start_time = posixtime(datetime('now'));  % Seconds since epoch
%end

% Pritn out a bunch of information
logentry(['Board ID: ' board]);
logentry(['Sampling Rate: ' num2str(srate)]);
logentry(['Voltage Range: [' num2str(Vrange(1)) ' ' num2str(Vrange(2)) ']']);
logentry(['Number of repeats: ' num2str(Nrepeat)]);
logentry(['Writing to output channels: ' num2str(channels(:)')]);
r_start_time = datetime(start_time, 'ConvertFrom', 'posixtime');  % start time as readable string
logentry(['Start time: ' string(r_start_time)]);
logentry('Signals to send to DAQ channels are plotted.');        

% Build full signal including repeats and final degaussing
try
    fullinput = zeros(length(t), size(inputs,2));                             % Preallocate full input matrix
    fullinput(1:length(inputs)*(Nrepeat+1),:) = repmat(inputs, Nrepeat+1, 1); % Repeat inputs Nrepeat+1 times
    fullinput(length(inputs)*(Nrepeat+1)+1:end,:) = final_degauss;            % Append final degaussing signal
catch
    % Handle case where input signal exceeds available memory or array limits
    logentry('Input is too long. Shorten the experiment duration or the sampling rate.');
    v = 0;
    beep;     % Audible alert
    return;   % Exit function
end

% Determine decimation factor for faster plotting
% High sample counts can slow plotting; decimation reduces points
% Note: Decimation may make degauss signal appear different from the actual output
if Nt > 1e7
    factor = 1e5;
elseif Nt > 1e6
    factor = 1e4;
elseif Nt > 1e5
    factor = 1e3;
elseif Nt > 1e4
    factor = 1e2;
elseif Nt > 1e3
    factor = 10;
else
    factor = 1;
end

% Perform decimation
t_p = downsample(t, factor);                  % Downsample time vector
fullinput_p = downsample(fullinput, factor);  % Downsample input signal

% Check if decimation resulted in unexpected vector length
if length(t_p) == length(fullinput)
    logentry('t_p is equal to fullinput'); 
end

% Print decimation factor used for plotting
logentry(['Plotting vector is decimated 1:' num2str(factor)]);

% Create a figure to display signal
figure;
plot(t_p, fullinput_p);
axis([0 t(end) Vrange(1) Vrange(2)]);    
title('DAQ Output');
xlabel('time (s)');
ylabel('Voltage (V)');
set(gca, 'FontSize', 12);

% Return the start time
v = start_time;

end

%% Generic console printing function
function logentry(txt)
    logtime = datetime('now');
    logtimetext = ['(' num2str(logtime(1), '%04i') '.' ...
                   num2str(logtime(2), '%02i') '.' ...
                   num2str(logtime(3), '%02i') ', ' ...
                   num2str(logtime(4), '%02i') ':' ...
                   num2str(logtime(5), '%02i') ':' ...
                   num2str(round(logtime(6)), '%02i') ') '];
    headertext = [logtimetext 'DACoperator: '];
     
    fprintf('%s%s\n', headertext, txt);
end
