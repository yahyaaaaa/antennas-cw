import numpy as np

r = lambda x : round(x, 4 - int(np.floor(np.log10(abs(x)))) - 1) # rounding lambda function

R = 6.378E6 # radius of earth in metres
h = 3.5786E7 # height of geocentric satellites in metres
sigma = R / (R + h)

# coordinates of earth station in bydgoszcz, poland

e_lat = np.deg2rad(53.1)
e_long = np.deg2rad(18.1)

# longitude of sub-satellite point

sat_long = np.deg2rad(19.2)
delta_long = abs(e_long - sat_long) # deg, difference in longitudes between earth station and sub-satellite point
beta = np.arccos(np.cos(e_lat) * np.cos(delta_long))

# elevation angle of satellite

El = np.arctan((np.cos(beta) - sigma) / np.sin(beta))

# azimuth angle of satellite

if e_lat > 0 and sat_long > e_long:
    Az = np.pi - np.arctan(np.tan(delta_long) / np.sin(e_lat))
elif e_lat > 0 and sat_long < e_long:
    Az = np.pi + np.arctan(np.tan(delta_long) / np.sin(e_lat))
elif e_lat < 0 and sat_long > e_long:
    Az = np.arctan(np.tan(delta_long) / np.sin(e_lat))
elif e_lat < 0 and sat_long < e_long:
    Az = 2 * np.pi - np.arctan(np.tan(delta_long) / np.sin(e_lat))

# satellite range

sat_range = 6.6235 * R * ((np.sin(beta)) / (np.cos(El)))

if __name__ == '__main__':
    print(np.rad2deg(beta))
    print(f"""satellite latitide =       0.0 deg
satellite longitude =      {round(np.rad2deg(sat_long), 1)} deg
earth station elevation =  {round(np.rad2deg(El), 1)} deg
earth station azimuth =    {round(np.rad2deg(Az), 1)} deg
satellite range =          {r(sat_range)/1000} km""")