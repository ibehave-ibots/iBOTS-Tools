
% initialise variables to store data
count = 0;
data_to_plot = 0;
 
plotGraph = plot(count,data_to_plot,'kx-' ); %Set up Plot

serialConnection = serialport("COM5",9600,Timeout=10); % connect to arduino
try
    while ishandle(plotGraph) %Loop when Plot is Active will run until plot is closed 
        serialData = readline(serialConnection); % read data from arduino
        data = jsondecode(serialData); % convert json string to struct
        count = count +1;
        data_to_plot(count)= data.value; % add new data to list
        set(plotGraph,'XData',[1:count],'YData',data_to_plot); % update plot
        pause(0.05);
    end
catch 
    delete(serialConnection)
    disp('Plot Closed and arduino object has been deleted')
end 

