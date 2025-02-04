# GRACE FUNCTIONS
import numpy as np
import matplotlib.pyplot as plt
import collections
from . import gps_ts_functions, gps_io_functions


Paired_TS = collections.namedtuple('Paired_TS', [
    'dtarray',
    'north', 'east', 'vert',
    'N_err', 'E_err', 'V_err',
    'u', 'v', 'w']);
# u, v, w are GRACE model displacements in east, north, and up.


def pair_GPSGRACE(GPS_TS, GRACE_TS):
    # This resamples the GRACE data to match GPS that is within the range of GRACE, and forms a common time axis.
    gps_decyear = gps_ts_functions.get_float_times(GPS_TS.dtarray)
    grace_decyear = gps_ts_functions.get_float_times(GRACE_TS.dtarray);  # the decimal years of all the grace obs points
    decyear, dtarray = [], [];
    north_gps, east_gps, vert_gps = [], [], [];
    N_err, E_err, V_err = [], [], [];
    for i in range(len(GPS_TS.dtarray)):  # this if-statement is happening because GPS is more current than GRACE
        if min(GRACE_TS.dtarray) < GPS_TS.dtarray[i] < max(GRACE_TS.dtarray):
            decyear.append(gps_decyear[i]);
            dtarray.append(GPS_TS.dtarray[i])
            north_gps.append(GPS_TS.dN[i]);
            east_gps.append(GPS_TS.dE[i]);
            vert_gps.append(GPS_TS.dU[i]);
            N_err.append(GPS_TS.Sn[i]);
            E_err.append(GPS_TS.Se[i]);
            V_err.append(GPS_TS.Su[i]);
    grace_u = np.interp(decyear, grace_decyear, GRACE_TS.dE);
    grace_v = np.interp(decyear, grace_decyear, GRACE_TS.dN);
    grace_w = np.interp(decyear, grace_decyear, GRACE_TS.dU);
    my_paired_ts = Paired_TS(dtarray=dtarray, north=north_gps, east=east_gps, vert=vert_gps, N_err=N_err, E_err=E_err,
                             V_err=V_err, u=grace_u, v=grace_v, w=grace_w);
    return my_paired_ts;


def plot_grace(station_name, filename, out_dir):
    grace_ts = gps_io_functions.read_grace(filename);
    plt.figure();
    plt.plot_date(grace_ts.dtarray, grace_ts.u, '-b');
    plt.plot_date(grace_ts.dtarray, grace_ts.v, '-g');
    plt.plot_date(grace_ts.dtarray, grace_ts.w, '-r');
    plt.legend(['east', 'north', 'vertical']);
    plt.grid(True);
    plt.xlabel('Time');
    plt.ylabel('Displacement (mm)');
    plt.savefig(out_dir + station_name + "_gracets.eps");
    return;
