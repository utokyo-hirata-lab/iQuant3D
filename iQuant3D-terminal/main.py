from iquant3d_terminal import *
iq3t = iq3t('data','53Cr',washout=30,threshold=1E4) #data_folder, time_standard_element, washout_time, bold_width
#iq3t.run_test()
#iq3t.run_rapid()
iq3t.run(norm='13C')
iq3t.multi_layer('57Fe')
iq3t.multi_layer('31P')
iq3t.finish_code()
