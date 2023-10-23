% Takes all NetCDF files and writes them to a .xml file as a matlab table
% script takes some time to run
% table contains only active trials where feedback_type ==1

files = dir("data/processed/neuropixels/*.nc"); % Remember to add folder data to path!!!
wanted_col_names = ["trial", "active_trials","feedback_type", "response_type" ];

mother_table = convert_file_to_table(files(1).name, wanted_col_names);


for n=2 : length(files)
    fprintf('progress: %d / %d \n', n, length(files));

    file = files(n).name;
    tab_ = convert_file_to_table(file, wanted_col_names);
    mother_table = [mother_table; tab_];
    mother_table = mother_table((mother_table.active_trials==1),:); % get only active trials
    mother_table = mother_table((mother_table.feedback_type==1),:); % only trials where feedback was positive
end
% write only certain columns
output_table = mother_table(:, ["trial", "mouse", "session_date", "wheel_speed"]);
writetable(output_table, 'data_all.xml')

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