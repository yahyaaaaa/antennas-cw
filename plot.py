import matplotlib.pyplot as plt
import numpy as np
from calculations import *

# varying gain and nf for lna

lna_gain_dB_vec = np.linspace(10, 40, 500)
lna_nf_vec = np.linspace(0, 3, 100)

X, Y = np.meshgrid(lna_gain_dB_vec, lna_nf_vec)

lna = component(X, Y, Ti, True)

# calculations

G_R = cable.gain * lna.gain * filter.gain * mixer.gain * if_amp.gain # receiver gain
T_R = (cable.temp + lna.temp)/cable.gain + (filter.temp + mixer.temp)/(cable.gain * lna.gain * filter.gain) + (if_amp.temp)/(cable.gain * lna.gain * filter.gain * mixer.gain) # receiver temp

N_0 = kB * B * G_R * (Ta + T_R) # output noise power in W
P_r = ratio(dB(N_0) + SNR_dB) / G_R # required received signal power in W
G_r_dB = dB(P_r) - EIRP_dBW + L_a_dB + L_p_dB # antenna gain in dB
d_r = (c/(f * np.pi)) * np.sqrt(ratio(G_r_dB)/0.65) * 100 # diameter in cm, aperture efficiency = 65% 

d = 60 * np.ones([100, 500]) # diameter = 60cm

# plotting

ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, d_r, color=(1,1,0.4,0.6))
ax.plot_wireframe(X, Y, d, color=(0.4,0.4,0.4,0.3))
ax.contour(X, Y, d_r - d, zdir='z', offset=61, levels=[0])
ax.set_title('antenna diameter vs LNA gain, noise figure (IF amp gain, NF = 17.6dB, 0.57dB)')
ax.set_xlabel('LNA gain (dB)')
ax.set_ylabel('LNA noise figure (dB)')
ax.set_zlabel('antenna diameter (cm)')
ax.set_zlim([np.min(d_r), np.max(d_r)])

plt.figure()
ax2 = plt.axes(projection='3d')
ax2.plot_wireframe(X, Y, G_r_dB, color='black')
ax2.set_title('antenna gain vs LNA gain, noise figure (IF amp gain, NF = 17.6dB, 0.57dB)')
ax2.set_xlabel('LNA gain (dB)')
ax2.set_ylabel('LNA noise figure (dB)')
ax2.set_zlabel('antenna gain (dB)')
ax2.set_zlim([np.min(G_r_dB), np.max(G_r_dB)])
plt.show()