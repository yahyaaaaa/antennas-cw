import numpy as np

def dB(ratio):
    return 10*np.log10(ratio)


def ratio(dB):
    return 10**(dB/10)


class component:

    def __init__(self, gain_dB, nf, Ti):
        self.gain_dB = gain_dB                      # gain in dB
        self.gain = ratio(self.gain_dB)             # gain in ratio
        self.nf = nf                                # noise figure (in dB)
        self.nF = ratio(self.nf)                    # noise factor (in ratio)
        if gain_dB > 0: # if the component is active
            self.temp = Ti * (ratio(self.nf) - 1)   # noise temp if active
        else: # if the component is passive
            self.temp = Ti * (1 - self.gain)        # noise temp if passive


# physical properties
c = 299792458 # speed of light
kB = 1.38E-23 # boltzmann's constant
Ti = 298 # ambient temp
Ta = 151.8 # antenna temp

# system properties

SNR = 9 # required SNR in dB
f = 11.634E9 # operating frequency
B = 26E6 # system bandwidth
EIRP = 51 # EIRP in dBW
L_a = 1.50 # rain attenuation in dB
L_p = 205.5 # path_loss in dB

# lna properties
# https://www.analog.com/media/en/technical-documentation/data-sheets/hmc8401.pdf

lna_gain_dB = 14.5 # lna gain in dB
lna_nf = 1.7 # lna noise figure in dB

# if amplifier properties
# https://www.skyworksinc.com/-/media/SkyWorks/Documents/Products/401-500/SKY67101_396LF_201266I.pdf

if_gain_dB = 17.6 # if amp gain in dB
if_nf = 0.57 # if amp noise figure in dB

# initialising components

cable = component(-0.5, 0.5, Ti)
lna = component(lna_gain_dB, lna_nf, Ti)
filter = component(-0.5, 0.5, Ti)
mixer = component(-6.5, 6.5, Ti)
if_amp = component(if_gain_dB, if_nf, Ti)

# calculations

G_R = cable.gain * lna.gain * filter.gain * mixer.gain * if_amp.gain # receiver gain
T_R = (cable.temp + lna.temp)/cable.gain + (filter.temp)/(cable.gain * lna.gain * filter.gain) + (mixer.temp + if_amp.temp)/(cable.gain * lna.gain * filter.gain * mixer.gain) # receiver temp

T_s = G_R * (Ta + T_R) # system temp

N = kB * B * T_s # noise power in W
P_r = ratio(dB(N) + SNR) # signal power in W
G_r = dB(P_r) - EIRP + L_a + L_p # antenna gain in dB

D_r = ratio(G_r) / cable.gain # directivity (assume that antenna is perfectly matched with feedline)
d_r = (c/(f * np.pi)) * np.sqrt(D_r/0.55) # diameter, aperture efficiency = 65% 


r = lambda x : round(x, 4 - int(np.floor(np.log10(abs(x)))) - 1) # rounding lambda function

system = [cable, lna, filter, mixer, if_amp]
for c in system:
    print(c.gain_dB, r(c.gain), c.nf, round(c.temp))

print(f"""receiver temperature      T_R = {round(T_R)} K
system temperature        T_s = {round(T_s)} K
noise power               N_r = {r(dB(N))} dBW
required signal power     P_r = {r(dB(N) + SNR)} dBW
antenna gain              G_r = {r(G_r)} dB
antenna diameter          d_r = {r(d_r)} m""")