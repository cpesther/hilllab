% Christopher Esther, Hill Lab, 10/1/2025
% Kris Ford, CISMM, 11/17/2008

function varargout = varforce_drive_synced_gui(varargin)
% VARFORCE_DRIVE_SYNCED_GUI launches the GUI for running the variable force 
% calibration experimental protocol for 3DFM.
%
% USAGE:
%   VARFORCE_DRIVE_SYNCED_GUI       - Creates a new GUI instance or raises the existing singleton.
%   H = VARFORCE_DRIVE_SYNCED_GUI   - Returns the handle to a new GUI or the existing singleton.
%   VARFORCE_DRIVE_SYNCED_GUI('CALLBACK',hObject,eventData,handles,...) 
%                                   - Calls the local function CALLBACK with the specified inputs.
%   VARFORCE_DRIVE_SYNCED_GUI('Property','Value',...) 
%                                   - Creates a new GUI or raises the existing singleton, applying
%                                     property/value pairs before varforce_drive_gui_OpeningFcn executes. 
%                                     Invalid properties stop execution.
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @varforce_drive_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @varforce_drive_gui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before varforce_drive_gui is made visible.
function varforce_drive_gui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to varforce_drive_gui (see VARARGIN)

    % Choose default command line output for varforce_drive_gui
    handles.output = hObject;

    % Update handles structure
    guidata(hObject, handles);

    % UIWAIT makes varforce_drive_gui wait for user response (see UIRESUME)
    % uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = varforce_drive_gui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    % Get default command line output from handles structure
    varargout{1} = handles.output;



function edit_calibrator_viscosity_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_calibrator_viscosity_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_maxforce_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_maxforce_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on selection change in popupmenu_daqboard.
function popupmenu_daqboard_Callback(hObject, eventdata, handles)


% --- Executes during object creation, after setting all properties.
function popupmenu_daqboard_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on button press in pushbutton_confirmDAq.
function pushbutton_confirmDAq_Callback(hObject, eventdata, handles)


function edit_daq_frequency_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_daq_frequency_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function lbl_duration_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function lbl_duration_CreateFcn(hObject, eventdata, handles)

% --- Executes on button press in pushbutton_autopulse.
function pushbutton_autopulse_Callback(hObject, eventdata, handles)

% --- Executes on selection change in listbox_voltages.
function listbox_voltages_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function listbox_voltages_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on selection change in listbox_pulsewidths.
function listbox_pulsewidths_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function listbox_pulsewidths_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_deg_tau_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_deg_tau_CreateFcn(hObject, eventdata, handles)

if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit_deg_freq_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_deg_freq_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in pushbutton_start.
function pushbutton_start_Callback(hObject, eventdata, handles)

    DAQid = get(handles.popupmenu_daqboard, 'String');
    DAQid_idx = get(handles.popupmenu_daqboard, 'Value'); 
    params.myDAQid = char(DAQid(DAQid_idx));
    
    params.DAQ_sampling_rate = str2num(get(handles.edit_daq_frequency, 'String'));
    params.NRepeats = str2num(get(handles.edit_sequences, 'String'));     
    pole_geometry = get(handles.popupmenu_geometry, 'String');
    pole_geometry_idx = get(handles.popupmenu_geometry, 'Value');
    params.my_pole_geometry = char(pole_geometry(pole_geometry_idx));
    
    deg_loc = get(handles.popupmenu_deg_loc, 'String');
    deg_loc_idx = get(handles.popupmenu_deg_loc, 'Value'); 
    params.deg_loc = char(deg_loc(deg_loc_idx));
    
    if get(handles.checkbox_full_degauss, 'Value') 
        params.degauss      = 'on';
        params.deg_tau      = str2num(get(handles.edit_deg_tau, 'String'));
        params.deg_freq     = str2num(get(handles.edit_deg_freq, 'String'));
        params.voltages     = [5 0]; % cleaning up with max voltage case
        params.pulse_widths = [0.5 0.5]; 
        params              = varforce_drive(params);
    end 
     
    params.voltages             = str2num(get(handles.edit_voltages, 'String'));
    params.pulse_widths         = str2num(get(handles.edit_pulsewidths, 'String'));
    params.duration             = str2num(get(handles.lbl_duration, 'String'));
    params.calibrator_viscosity = str2num(get(handles.edit_calibrator_viscosity, 'String'));
    params.bead_radius          = str2num(get(handles.edit_bead_radius, 'String'));  
    params.calibum              = str2num(get(handles.edit_calibum, 'String'));
    params.deg_tau              = str2num(get(handles.edit_deg_tau, 'String'));
    params.deg_freq             = str2num(get(handles.edit_deg_freq, 'String'));
    params.fps                  = str2num(get(handles.edit_fps, 'String'));

    if get(handles.checkbox_degauss, 'Value');
        params.degauss = 'on';
    else
        params.degauss = 'off';
    end

    % Starting the run by sending information to varforce_drive function.
    logentry('Starting DAC run...');

    % Get the file name where all relevant data must be saved
    if get(handles.checkbox_save_metadata, 'Value')
        filename = get(handles.edit_filename, 'String');
    end

    % Start video recording and signal generation here, both on their own 
    % timer object for simultaneous execution. 

    % Timer for video recording
    vidTimer = timer('ExecutionMode','singleShot', ...
                     'StartDelay', 0, ...
                     'TimerFcn', @(~,~) record_synced_video(filename));
    
    % Timer for DAQ output
    sigTimer = timer('ExecutionMode','singleShot', ...
                     'StartDelay', 0, ...
                     'TimerFcn', @(~,~) varforce_drive(params, filename));
    
    % Start both timers
    start(vidTimer);
    start(sigTimer);

    logentry('DAC run is finished.');                               

% --- Executes on button press in pushbutton_close.
function pushbutton_close_Callback(hObject, eventdata, handles) %#ok<*INUSD>
        close(varforce_drive_gui);
        
function edit_voltages_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_voltages_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_pulsewidths_Callback(hObject, eventdata, handles)
    duration = sum(str2num(get(handles.edit_pulsewidths, 'String')));
    numSequences = str2num(get(handles.edit_sequences, 'String'));
    set(handles.lbl_duration, 'String', num2str(duration*numSequences));

% --- Executes during object creation, after setting all properties.
function edit_pulsewidths_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end
    
% --- Executes on selection change in popupmenu_calibrators.
function popupmenu_calibrators_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function popupmenu_calibrators_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_temperature_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_temperature_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_bead_radius_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_bead_radius_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_maxdist_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_maxdist_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_noisefloor_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_noisefloor_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_desiredSNR_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_desiredSNR_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on selection change in popupmenu_geometry.
function popupmenu_geometry_Callback(hObject, eventdata, handles)


% --- Executes during object creation, after setting all properties.
function popupmenu_geometry_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function edit_sequences_Callback(hObject, eventdata, handles)
    duration = sum(str2num(get(handles.edit_pulsewidths, 'String')));
    numSequences = str2num(get(handles.edit_sequences, 'String'));
    set(handles.lbl_duration, 'String', num2str(duration*numSequences));

% --- Executes during object creation, after setting all properties.
function edit_sequences_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

% --- Executes on button press in checkbox_save_metadata.
function checkbox_save_metadata_Callback(hObject, eventdata, handles)

function edit_filename_Callback(hObject, eventdata, handles)

% --- Executes during object creation, after setting all properties.
function edit_filename_CreateFcn(hObject, eventdata, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end


% --- Executes on button press in checkbox_degauss.
function checkbox_degauss_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox_degauss (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox_degauss


% --- Executes on button press in degauss_now_button.
% % % % % % % % % % % % % % % % % % % % 
%  funtion imediatly degausses pole tip with a 5 volt maximum degauss. does
%  not overwrite metadata file. Useful for complete degauss in advance of
%  expiriment
%  sets all params = to those that will provide a full degauss. basicaly a
%  hack that enters the same things the user could but without making them
%  take the time or have to reset the params. also pervents writing over
%  data file with the record of a degauss pulse.
% % % % % % % % % % % % % % % % % % % % 
function degauss_now_button_Callback(hObject, eventdata, handles)

    params.deg_loc = char('beginning');
    params.myDAQid              = char('PCIe-6738');
    params.DAQ_sampling_rate    = 100000;
    params.NRepeats             = 1; 
    pole_geometry               = get(handles.popupmenu_geometry, 'String');
    pole_geometry_idx           = get(handles.popupmenu_geometry, 'Value');
    params.my_pole_geometry     = char(pole_geometry(pole_geometry_idx));
    params.degauss              = 'on';
    params.deg_tau              = str2double(get(handles.edit_deg_tau, 'String'));
    params.deg_freq             = str2double(get(handles.edit_deg_freq, 'String'));
    params.voltages             = [5 0];
    params.pulse_widths         = [0.5 0.5];
    params.duration             = .1;
    params.calibrator_viscosity = [];
    params.bead_radius          = [];  
    params.calibum              = [];
    params.fps                  = str2num(get(handles.edit_fps, 'String'));
    
    logentry('Starting Degauss run...');  
    params = varforce_drive(params);
    pause(params.duration);
    logentry('Degauss run is finished.');
                            

% --- Executes on button press in checkbox_full_degauss.
function checkbox_full_degauss_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox_full_degauss (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox_full_degauss

% =========================================================================
% Everything below this point are functions related to computation and data
% handling/display, and not the gui (although the handles structure is used).
% =========================================================================

function logentry(txt)
    logtime = datetime('now');
    logtimetext = [ '(' num2str(logtime(1),  '%04i') '.' ...
                   num2str(logtime(2),        '%02i') '.' ...
                   num2str(logtime(3),        '%02i') ', ' ...
                   num2str(logtime(4),        '%02i') ':' ...
                   num2str(logtime(5),        '%02i') ':' ...
                   num2str(round(logtime(6)), '%02i') ') '];
     headertext = [logtimetext 'varforce_drive_gui: '];
     
     fprintf('%s%s\n', headertext, txt);

   




function edit_calibum_Callback(hObject, eventdata, handles)
% hObject    handle to edit_calibum (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_calibum as text
%        str2double(get(hObject,'String')) returns contents of edit_calibum as a double


% --- Executes during object creation, after setting all properties.
function edit_calibum_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_calibum (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu_deg_loc.
function popupmenu_deg_loc_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu_deg_loc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns popupmenu_deg_loc contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu_deg_loc


% --- Executes during object creation, after setting all properties.
function popupmenu_deg_loc_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu_deg_loc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit_fps_Callback(hObject, eventdata, handles)
% hObject    handle to edit_fps (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_fps as text
%        str2double(get(hObject,'String')) returns contents of edit_fps as a double


% --- Executes during object creation, after setting all properties.
function edit_fps_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_fps (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
