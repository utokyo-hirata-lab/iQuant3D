from iquant3d_terminal_TOF import *
iq3t = iq3t('data','121Sb',25,100) #data_folder, time_standard_element, washout_time, bold_width
#iq3t.run_test()
#iq3t.run_rapid()
iq3t.run()
#iq3t.get_element_list('data/imagingTest_20191209_12h44m04s_AS.csv')
#iq3t.clustering(6)
"""
iq3t.multi_layer('25Mg')
iq3t.multi_layer('27Al')
iq3t.multi_layer('51V')
iq3t.multi_layer('53Cr')
iq3t.multi_layer('55Mn')
iq3t.multi_layer('63Cu')
iq3t.multi_layer('121Sb')
iq3t.multi_layer('206Pb')
"""
iq3t.finish_code()
