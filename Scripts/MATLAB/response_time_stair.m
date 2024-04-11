clear all; close all;

% Parse Excel files for data:
% ----------------------------------------------------------------------

% Load the Excel file as a cell array of strings
data = readcell('200uLGood.csv');

% Extract the time stamps, current pressure, and target pressure
time_stamps = cellfun(@(x) x, data(2:end, 1)); 
pressure = cellfun(@(x) x, data(2:end, 2)); 
target_pressure = cellfun(@(x) x, data(2:end, 3)); 
flow = cellfun(@(x) x, data(2:end, 4)); 
target_flow = cellfun(@(x) x, data(2:end, 5)); 

t = milliseconds(time_stamps - time_stamps(1)); % in ms
% Parse Target Pressure for non-zero indices:
% ----------------------------------------------------------------------

target = target_flow;

% Find non-zero entries
non_zero_indices = find(target_flow);

% Initialize start and end indices
start_index = non_zero_indices(1);
end_index = start_index;

% Initialize pairs array
pairs = [];

% Iterate through non-zero indices
for i = 2:length(non_zero_indices)
    if target_flow(non_zero_indices(i)) == target_flow(non_zero_indices(i-1))
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
hold off;
hold on;

% for a = 1:length(pairs)
%     time = t(pairs(a, 1):pairs(a, 2));
%     Q = abs(flow(pairs(a, 1):pairs(a, 2)));
%     time = time - time(1);
%     Q = Q - Q(1);
% 
%     plot(time, Q);
% 
%     [G,wn,zeta,FV] = underDamped(time, Q, 1e-3);
% 
%     dt = linspace(0, 8.1, 8104);
%     plot(step(G, dt));
% end

time = t(pairs(1, 1):pairs(1, 2));
Q = abs(flow(pairs(1, 1):pairs(1, 2)));
time = time - time(1);
Q = Q - Q(1);

plot(time, Q);

% [G,wn,zeta,FV] = underDamped(time, Q, 1e-3);

dt = linspace(0, 8.1, 8104);
plot(step(G, dt));

title('Step Response of Flow Rate');
xlabel('Time (ms)');
ylabel('Flowrate');
legend('Measured Data', 'Second Order Approximation');

info = stepinfo(G);