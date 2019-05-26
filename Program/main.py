################################### main.py ####################################
# Author:_________________| University:____________________| Std no:__________ #
# _______ John Paul Mendy |____________ Leeds University __|________ sc15jpm _ #
################################################################################
#Purpose:                                                                      #
#         This is a program to test the File transform python FileExists.      #
#         User information will be taken and used for navigation and decision  #
#         on what file format to export their document to.                     #
################################################################################
from time import sleep
#from File_Transform import Transformer

#in_funs = ['get_csv','get_eml','get_ics','get_html','get_tex']
in_names = ['CSV','EML','ICS','HTML','TEX']
#out_funs = ['mk_csv','mk_eml','mk_ics','mk_html','mk_tex']

################################################################################
print('_'*73+'\n'+'_'*28+' File Transformer '+'_'*27+'\n'+'_'*73)
print("#"*30+ ' Quick Guide '+ 30*'#')
print('(i)\tPlease store all the files you need in the ../Test_Files folder\t#')
print('(ii)\tChoose your software to convert from                          \t#')
print('(iii)\tChoose file name                                             \t#')
print('(iv)\tChoose software to tranfrom into                              \t#')
#sleep(5)

#ift = Transformer()
print("\nPlease Select the file to transfrom")
for i in range(len(in_names)):print('[%d]\t%s' % ((i+1), in_names[i]))
usrIn = input('Choice : ')
fil = input('Filename(without file extension): ')

try:
    val = int(usrIn)-1
    if val < len(in_names) and val >= 0:
        function = 'get_'+in_names[val].lower())
        print('Opening %s' %(function))
        ift.pick_format(function,fil)
        if ift.table != []: print('Data Successfully retrieve\n',80*'#')
    else: raise Exception('File data failed unpackage')
        in_names.pop(val)
        print("\nPlease Select File Destination by its number")
        for i in range(len(in_names)):print('[%d]\t%s' % ((i+1), in_names[i]))
        out = ("Choice : ")
        val2 = int(out)-1
        function = 'mk_'+in_names[val2].lower())
        ift.pick_format(function,fil)
    else: raise Exception('That value is out of range')
except ValueError:
    print('Please enter an Int')
