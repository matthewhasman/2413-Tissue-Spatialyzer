function [G,wn,zeta, tau_r, tau_e]=overdamped(t, y)
    s = tf('s');
    FV = y(end);
    ten = FV*0.1;
    tnin = FV*0.9;
    texp = FV*0.63;
    tau_ten = t(find(y > ten, 1));
    tau_nine = t(find(y > tnin, 1));
    tau_e = t(find(y > texp, 1));
    tau_r = tau_nine - tau_ten;
    ratio = tau_r/tau_e;
    % if tau_r/tau_e > 2, no longer second order
    if ratio > 2
        sigma = 1/tau_e;
        G = FV*sigma/(s + sigma);
        wn = sigma;
        zeta = 0;
    else 
        zeta = tau_e/(3.86*tau_e - 1.83*tau_r);
        disp(zeta);
        wn = 2.1*zeta/(tau_e);
        G = FV * (wn^2)/(s^2 + 2*zeta*wn*s + wn^2);
end