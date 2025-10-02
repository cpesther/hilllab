% Christopher Esther, Hill Lab, 10/1/2025
% Kris Ford, CISMM, 11/17/2008

function params_out = varforce_drive(params, filename)
% VARFORCE_DRIVE Executes the variable force calibration protocol for 3DFM
%
% ARGUMENTS:
%   params : structure with the following fields
%       .myDAQid           string, 'daqtest'        DAQ board identifier
%       .DAQ_sampling_rate int, 100000              Sampling rate in Hz
%       .NRepeats          int, 0                   Number of times to repeat the input signal
%       .my_pole_geometry  string, 'pole4-flat'     3DFM pole geometry
%       .voltages          vector, [0 1 2 3 4 5]    Pulse voltages in Volts
%       .pulse_widths      vector, [1 1 1 1 1 1]    Pulse widths in seconds
%       .degauss           {on} | off               Include degauss at 0 Volts
%       .deg_tau           scalar, 0.0012           Degauss decay constant
%       .deg_freq          scalar, 10000            Degauss frequency
%       .fps               int, 120                 Frames per second
%
%       Required fields are marked with a star (*)
%       Default values are shown in braces {} or defined after the data type
%
% RETURNS:
%   params_out : structure with updated parameters after calibration

% Handle the argument list
if nargin < 1 | isempty(params) || ~exist('params', 'var')
    params = [];
    logentry('No input parameter structure defined. Assuming defaults.');
end

if ~isfield(params, 'myDAQid')
    params.myDAQid = 'daqtest';
    logentry('No myDAQid defined.  Defaulting to daqtest.');
end

if ~isfield(params, 'DAQ_sampling_rate')
    params.DAQ_sampling_rate = 100000;
    logentry('No sampling rate defined.  Defaulting to 100 [kHz].');
end

if ~isfield(params, 'NRepeats')
    params.NRepeats = 0;
    logentry('No NRepeats defined.  Defaulting to 0 repeats of input signal.');
end

if ~isfield(params, 'my_pole_geometry')
    params.my_pole_geometry = 'pole1-flat';
    logentry('No geometry specified.  Defaulting to pole1-flat geometry.');
end

if ~isfield(params, 'voltages')
    params.voltages = [0 1 2 3 4 5];
    logentry('No voltages defined.  Defaulting to [0 1 2 3 4 5] Volts.');
end

if ~isfield(params, 'pulse_widths')
    params.pulse_widths = [1 1 1 1 1 1];
    logentry('No pulse widths defined.  Defaulting to 1 [sec] width for each pulse.');
end

if ~isfield(params, 'deg_tau')
    params.deg_tau = .0012;
    logentry('No degauss time constant specified.  Defaulting to rapid degauss (tau=.0012).');
end

if ~isfield(params, 'deg_freq')
    params.deg_freq = 10000;
    logentry('No degauss frequency specified.  Defaulting to rapid degauss (f=10000).');
end

if ~isfield(params, 'degauss')
    params.degauss = 'on';
    logentry('No choice made for degauss.  Assuming you want to degauss.');
end

if ~isfield(params, 'deg_loc')
    params.deg_loc = 'end';
    logentry('No choice made for degauss location.  Assuming you want it in the middle of the zero pulse.');
end

if ~isfield(params, 'fps')
    params.fps = 120;
    logentry('No choice made for frames per second.  Assuming you want rate of 120 fps.');
end
    
myDAQid           = params.myDAQid;
DAQ_sampling_rate = params.DAQ_sampling_rate;
NRepeats          = params.NRepeats;
my_pole_geometry  = params.my_pole_geometry;
voltages          = params.voltages;
pulse_widths      = params.pulse_widths; 
degauss           = params.degauss;
deg_loc           = params.deg_loc;
deg_tau           = params.deg_tau;
deg_freq          = params.deg_freq;
fps               = params.fps;

% Check for equal vector lengths for voltages and pulse lengths
if length(voltages) ~= length(pulse_widths)
    error('voltage and pulse_widths are not same length.');
end

% Setup hardware
nDACout = 6;  % determined by hardware, nCoils = 6
duration = sum(pulse_widths);

% Define which poles are going to be excited and in what way.
switch my_pole_geometry
    case 'pole4-flat'
        poles_to_excite_pos = 4;
        poles_to_excite_neg = [1 2 6];
        dominant_coil = 4;
    case 'pole1-flat'
        poles_to_excite_pos = 1;
        poles_to_excite_neg = [3 4 5];
        dominant_coil = 1;
    case 'wakeforest612'
        poles_to_excite_pos = [6 1 2];
        poles_to_excite_neg = [3 4 5];
        dominant_coil = 1;
    case '3pole-246'
        poles_to_excite_pos = [2];
        poles_to_excite_neg = [4 6];        
        dominant_coil = 2;
    case '3pole-135'
        poles_to_excite_pos = [1];
        poles_to_excite_neg = [3 5];        
        dominant_coil = 1;
    case '3pole-351'
        poles_to_excite_pos = [3];
        poles_to_excite_neg = [1 5];        
        dominant_coil = 3;        
    case '3pole-513'
        poles_to_excite_pos = [5];
        poles_to_excite_neg = [1 3];        
        dominant_coil = 5;        
    case '4pole-1245'
        poles_to_excite_pos = [1 2];
        poles_to_excite_neg = [4 5];        
        dominant_coil = 1;        
    case '4pole-4512'
        poles_to_excite_pos = [4 5];
        poles_to_excite_neg = [1 2];        
        dominant_coil = 4;       
    case 'SAP'
        poles_to_excite_pos = [1];
        poles_to_excite_neg = [];        
        dominant_coil = 1;               
    otherwise
        error(['Pole geometry ' my_pole_geometry ' not recognized.']);
end

% INITIAL MATH:  precondition the output matrix to all zeros and define the
% time vector that will give normal mortals an idea of what's going on.
t = [0 : 1/(DAQ_sampling_rate - 1) : duration]'; % daq sampling rate = number of scans for any 1s time interval. So time steps delta_t correspond to 1/(samp. rate - 1)s
signal = zeros(length(t), nDACout);


% SETUP OUTPUT MATRIX:  This section defines the output matrix that will be
% sent to DAQ board according to the experimental details defined above.

events = cumsum(pulse_widths);

% DEGAUSS CODE
if strcmp(degauss, 'on')
    max_voltage_amplitude = max(voltages); % V
    idx = find(voltages == 0);
    degauss_duration = (pulse_widths(idx)/2); % seconds
    degt = [0 : 1/(DAQ_sampling_rate - 1) : degauss_duration]';
    degauss_vector = max_voltage_amplitude * exp(-degt/deg_tau) .* cos(2*pi*deg_freq*degt);    
% 
%     figure(88); 
%     plot(degt, degauss_vector);
%     title('Degauss signal sent in center of zero volt pulse');
%     xlabel('time [s]');
%     ylabel('Volts');    
end



for k = 1 : length(voltages)
    
    if k == 1
        idx = find(t <= events(k));
    else
        idx = find(t <= events(k) & t > events(k-1));
    end

    if voltages(k) == 0 & strcmp(degauss, 'on')
        
        % when degauss is enabled there is a pulse of zero volts for 1/2 time
        % set by user. Then degause vector is inserted and allowed to decay
        % for the remaining half of the 'zero' pulse. it has esentially no
        % effect after 8 milliseconds but this keeps the clock consistent
        % real zero period
        signal(idx , poles_to_excite_pos) = 0;
        signal(idx , poles_to_excite_neg) = 0; 
        
        if strcmp(deg_loc, 'end')                 
            % sets up assignment location in signal for degauss_vector. 
            start_degauss = max(idx) - length(degauss_vector) + 1;
            end_degauss   = max(idx);
             
            % degauss_vector written into 'zero' pulse signal
            signal(start_degauss:end_degauss, poles_to_excite_pos) = repmat(degauss_vector(:)/length(poles_to_excite_pos), 1, length(poles_to_excite_pos));
            signal(start_degauss:end_degauss, poles_to_excite_neg) = - repmat(degauss_vector(:)/length(poles_to_excite_neg), 1, length(poles_to_excite_neg));                 
        end
        
        if strcmp(deg_loc, 'beginning')
             % sets up assignment location in signal for degauss_vector. 
             start_degauss = min(idx);
             end_degauss   = min(idx) + length(degauss_vector) - 1;
             
             % degauss_vector written into 'zero' pulse signal
             signal(start_degauss:end_degauss, poles_to_excite_pos) = repmat(degauss_vector(:)/length(poles_to_excite_pos), 1, length(poles_to_excite_pos));
             signal(start_degauss:end_degauss, poles_to_excite_neg) = - repmat(degauss_vector(:)/length(poles_to_excite_neg), 1, length(poles_to_excite_neg));
             
        end  
        
    else
        signal(idx, poles_to_excite_pos) = voltages(k);
        signal(idx, poles_to_excite_neg) = - voltages(k)/length(poles_to_excite_neg);
    end

end
logentry('signal matrix prepared');

% logentry(['voltages: ' num2str(length(voltages))]);
% figure;
%     plot(t, signal);
%     axis([0 t(end) Vrange(1) Vrange(2)]);    
%     title('Signal');
%     xlabel('time (s)');
%     ylabel('Voltage (V)');
%     set(gca, 'FontSize', 12);

% prepare a degauss signal matrix to be added at the very end of the experiemnt
deg_dur = mean(pulse_widths)/2; 
deg_t = [0 : 1/(DAQ_sampling_rate - 1) : deg_dur]'; 
final_degauss = zeros(length(deg_t)*2, nDACout);
deg_vec =  max_voltage_amplitude * exp(-deg_t/deg_tau) .* cos(2*pi*deg_freq*deg_t);
final_degauss(end-length(deg_vec)+1:end,poles_to_excite_pos) = repmat(deg_vec(:)/length(poles_to_excite_pos), 1, length(poles_to_excite_pos)); 
final_degauss(end-length(deg_vec)+1:end,poles_to_excite_neg) = - repmat(deg_vec(:)/length(poles_to_excite_neg), 1, length(poles_to_excite_neg));


% Start experiment.  Call DACoperator. Call pulnix software. etc..
channels = [1:nDACout];
Vrange = [-5 5];

timeout = DACoperator(signal, final_degauss, NRepeats, myDAQid, channels, DAQ_sampling_rate, Vrange);

% attaching outputs to the output structure
params_out = params;
params_out.sent_signal = signal;
params_out.start_time = timeout;
params_out.dominant_coil = dominant_coil;

% Save the params to a file
save(filename, '-struct', 'params_out');          
logentry(['Saved metadata to file: ' filename '.']);
                   
% -------------
function logentry(txt)
    logtime = clock;
    logtimetext = [ '(' num2str(logtime(1),  '%04i') '.' ...
                   num2str(logtime(2),        '%02i') '.' ...
                   num2str(logtime(3),        '%02i') ', ' ...
                   num2str(logtime(4),        '%02i') ':' ...
                   num2str(logtime(5),        '%02i') ':' ...
                   num2str(round(logtime(6)), '%02i') ') '];
     headertext = [logtimetext 'varforce_cal_drive: '];
     
     fprintf('%s%s\n', headertext, txt);
