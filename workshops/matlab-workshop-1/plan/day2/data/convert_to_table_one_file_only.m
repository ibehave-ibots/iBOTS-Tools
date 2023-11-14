
files = dir("/home/ben/ibots/iBOTS-Tools/workshops/matlab-workshop-1/plan/day2/data/*.nc"); % Remember to add folder data to path!!!
wanted_col_names = ["trial", "active_trials","feedback_type", "response_type","gocue", "response_time", "feedback_time" ];

mother_table = convert_file_to_table(files(1).name, wanted_col_names);



% write only certain columns
output_table = mother_table(mother_table.active_trials==1,:);
writetable(output_table, 'wheel_speed.xml')


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
