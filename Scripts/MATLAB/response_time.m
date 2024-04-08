% Plots raw pressure data with a second order approximation

clear all; close all;

% Parse Excel files for data:
% ----------------------------------------------------------------------

% Load the Excel file as a cell array of strings
data = readcell('Response_zero_volume.csv');

% Extract the time stamps, current pressure, and target pressure
time_stamps = cellfun(@(x) x, data(2:end, 1)); 
pressure = cellfun(@(x) x, data(2:end, 2)); 
target_pressure = cellfun(@(x) x, data(2:end, 3)); 

t = milliseconds(time_stamps - time_stamps(1)); % in ms

% Parse Target Pressure for non-zero indices:
% ----------------------------------------------------------------------

% Find non-zero entries
non_zero_indices = find(target_pressure);

% Initialize start and end indices
start_index = non_zero_indices(1);
end_index = start_index;

% Initialize pairs array
pairs = [];

% Iterate through non-zero indices
for i = 2:length(non_zero_indices)
    if non_zero_indices(i) == non_zero_indices(i-1) + 1
        % If consecutive, update end_index
        end_index = non_zero_indices(i);
    else
        % If not consecutive, add pair to pairs array
        pairs = [pairs; [start_index, end_index]];
        % Update start_index and end_index
        start_index = non_zero_indices(i);
        end_index = start_index;
    end
end

% Add the last pair if necessary
if start_index ~= end_index
    pairs = [pairs; [start_index, end_index]];
end

% Find the step response:
% ----------------------------------------------------------------------
time = t(pairs(1, 1):pairs(1, 1)+50);
p = -1*pressure(pairs(1, 1):pairs(1, 1)+50);
time = time - time(1);

plot(time, p);


[G,wn,zeta,tau_r]=overdamped(time, p);
tau_r;
hold on;
dt = linspace(0, 5000, 5000);

plot(step(G, dt));

title('Step Response of setting pressure with zero volume');
xlabel('Time (ms)');
ylabel('Pressure');
legend('Measured Data', 'Second Order Approximation');
