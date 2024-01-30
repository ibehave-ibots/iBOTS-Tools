fileName = "matlabStream.txt";
if exist(fileName)
    delete(fileName)
end
s = serialport("COM5",9600,Timeout=10);
%s = serial('COM5'); % change this to desired Arduino board port
%set(s,'BaudRate',9600); % baud rate for communication
%fopen(s); % open the comm between Arduino and MATLAB

ButtonHandle = uicontrol('Style', 'PushButton', ...
                         'String', 'Stop loop', ...
                         'Callback', 'delete(gcbf)');

while true 
    data = readline(s);
    fileID = fopen(fileName,'a');
    fprintf(fileID, data);
    fclose(fileID);
    pause(0.05);
    if ~ishandle(ButtonHandle)
        disp('Loop stopped by user');
    break;
    end
end


delete(s)