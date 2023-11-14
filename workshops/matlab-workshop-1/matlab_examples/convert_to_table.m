% Takes all NetCDF files and writes them to .xml files as a matlab table
% script takes some time to run
% file data_all.xml is for all trials
% data_active_pos_fb.xml contains only active trials where feedback_type ==1
% data_active_pos_fb_response_only.xml contains only active trials where feedback_type ==1 and only wheel speeds before the response time

files = dir("data/processed/neuropixels/*.nc"); % Remember to add folder data to path!!!
wanted_col_names = ["trial", "active_trials","feedback_type", "response_type", "response_time" ];

mother_table = convert_file_to_table(files(1).name, wanted_col_names);


for n=2 : length(files)
    fprintf('progress: %d / %d \n', n, length(files));
    file = files(n).name;
    tab_ = convert_file_to_table(file, wanted_col_names);
    mother_table = [mother_table; tab_];
   
end
cols_to_write = ["trial", "mouse", "session_date","response_time", "wheel_speed"];
%write all data
writetable(mother_table(:, cols_to_write), 'data_all.xml')
%clear mother_table 

%write only active trials with positive feedback
data = mother_table;
data = data(data.active_trials==1 & data.feedback_type==1,:);
writetable(data(:, cols_to_write), 'data_active_pos_fb.xml');
clear data

% write only active trials with positive feedback and include wheel speed
% only during response
data = readtable('data_active_pos_fb.xml');
data.response_time_bin = round(data.response_time* 1000 / 10); %time bins are 10ms
for i =1 : height(data)
    rb = data{i,"response_time_bin"};
    if (rb < 250)         
         wh = NaN(size(data{i, "wheel_speed"}));
         wh(1:rb) = data{i,"wheel_speed"}(1:rb);
         data{i,"wheel_speed"}= wh;
    end 
end
writetable(data(:, cols_to_write), 'data_active_pos_fb_response_only.xml');

%move files to data directory
files = dir('./*.xml');
mkdir data/matlab_table
for i=1 : length(files)
    movefile(files(i).name, "data/matlab_table")
end

function my_table = convert_file_to_table(file, wanted_col_names)
    table_index = 1;
    my_data = struct();
    mouse_name = ncread(file, 'mouse');
    session_date = ncread(file, 'session_date');
    trial = ncread(file, "trial");
    wheel = ncread(file, "wheel");
    for k=1 : length(trial)
       for l =1: length(wanted_col_names)
             data_ = ncread(file,wanted_col_names(l));
             my_data(table_index).(wanted_col_names(l)) =  data_(k);
       end
       my_data(table_index).("mouse") =mouse_name;
       my_data(table_index).("session_date") =session_date;
       my_data(table_index).("wheel_speed") =wheel(:,k);
       table_index = table_index +1;
    end
    my_table = struct2table(my_data, 'AsArray',true);
end
