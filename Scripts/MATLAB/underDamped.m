function [G,wn,zeta, FV]=underDamped(UD_x, UD_y, time_scale)
    % Find dt
    s = tf('s');
    length_prime = size(UD_x);
    length = length_prime(1);
    lower_bound = length - floor(length/100);
    delta_t = (UD_x(end)*time_scale/length);

    % Find FV:
    FV = UD_y(length);

    % Find overshoot by calculating max value of signal
    overshoot = max(UD_y);
    OS = (overshoot - FV)/FV;

    % Find damping coefficient using formula:
    zeta = -1*log(OS)/sqrt((pi^2 + log(OS)^2));
    beta = sqrt(1 - zeta^2);

    % Find Wp using peak time:
    Tp = mean(find(UD_y == max(UD_y)) * delta_t);
    wnp = pi/(beta*Tp);

    % Rise Time: 
    % Find first instance of experimental data that reaches the final value:
    Tr = UD_x(find(UD_y > FV, 1))*1e-3;
    wnr = 1/(beta*Tr)*(pi - atan(beta/zeta));

    wn = (wnr + wnp)/2;
    G = FV * (wn^2)/(s^2 + 2*zeta*wn*s + wn^2);

end


