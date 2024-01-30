serialportlist("available");

arduinoObj = serialport("COM5",9600)';

arduinoObj.UserData = struct("Data",[],"Count",1);

configureCallback(arduinoObj,"terminator",@readData);
%configureCallback(arduinoObj,"byte", 1 , @readData);


function readData(src, ~)

% Read the ASCII data from the serialport object.
while true
    data = readline(src)
    fileID = fopen('matlabStream.txt','a');
    fprintf(fileID, data);
    fclose(fileID);
end
% Convert the string data to numeric type and save it in the UserData
% property of the serialport object.
%src.UserData.Data(end+1) = str2double(data);

% Update the Count value of the serialport object.
src.UserData.Count = src.UserData.Count + 1;

% If 1001 data points have been collected from the Arduino, switch off the
% callbacks and plot the data.
%if src.UserData.Count > 1001
%    configureCallback(src, "off");
%    plot(src.UserData.Data(2:end));
%end
end


