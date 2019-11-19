from iquant3d_terminal import *
iq3t = iq3t('data','206Pb',20) #data folder, time_standard_element, washout_time
iq3t.run()
iq3t.clustering(12)
iq3t.finish_code()
