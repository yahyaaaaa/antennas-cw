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
T_R = (cable.temp + lna.temp)/cable.gain + (filter.temp)/(cable.gain * lna.gain * filter.gain) + (mixer.temp + if_amp.temp)/(cable.gain * lna.gain * filter.gain * mixer.gain) # receiver temp

N_0 = kB * B * G_R * (Ta + T_R) # output noise power in W
P_r = ratio(dB(N_0) + SNR) / G_R # required received signal power in W
G_r = dB(P_r) - EIRP + L_a + L_p # antenna gain in dB
d_r = (c/(f * np.pi)) * np.sqrt(ratio(G_r)/0.7) * 100 # diameter in cm, aperture efficiency = 70% 

d = 60 * np.ones([100, 500]) # diameter = 60cm

# plotting

ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, d_r, color=(1,1,0.4,0.6))
ax.plot_wireframe(X, Y, d, color=(0.4,0.4,0.4,0.3))
ax.contour(X, Y, d_r - d, zdir='z', offset=61, levels=[0])
ax.set_title('antenna diameter vs LNA gain, noise figure')
ax.set_xlabel('LNA gain (dB)')
ax.set_ylabel('LNA noise figure (dB)')
ax.set_zlabel('antenna diameter (cm)')
ax.set_zlim([40,110])
ax.view_init(0, -45)
plt.show()
