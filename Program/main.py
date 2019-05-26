################################### main.py ####################################
# Author:_________________| University:____________________| Std no:__________ #
# _______ John Paul Mendy |____________ Leeds University __|________ sc15jpm _ #
################################################################################
#Purpose:                                                                      #
#         This is a program to test the File transform python FileExists.      #
#         User information will be taken and used for navigation and decision  #
#         on what file format to export their document to.                     #
################################################################################
#from time import sleep
from File_Transform import Transformer

# List of file formats for name pick
in_names = ['CSV','EML','ICS','HTML','TEX']

################################################################################
# Tutorial on the go
print('_'*73+'\n'+'_'*28+' File Transformer '+'_'*27+'\n'+'_'*73)
print("#"*30+ ' Quick Guide '+ 30*'#')
print('(i)\tPlease store all the files you need in the ../Test_Files folder\t#')
print('(ii)\tChoose your software to convert from                          \t#')
print('(iii)\tChoose file name                                             \t#')
print('(iv)\tChoose software to tranfrom into                              \t#')

# Create the transform object and get the name to print
ift = Transformer()
print("\nPlease Select the number of file type to transfrom")
for i in range(len(in_names)):print('[%d]\t%s' % ((i+1), in_names[i]))
usrIn = input('Choice : ')
fil = input('Filename(without file extension): ')

try:
    # call the function to read from user choices
    val = int(usrIn)-1
    if val < len(in_names) and val >= 0:
        function = 'get_'+in_names[val].lower()
        print('Opening %s' %(function))
        ift.pick_format(function,fil)
        if ift.table != []: print('Data Successfully retrieve\n',80*'#')
        else: raise Exception('File data failed unpackage')

        # Now remove the file format we used to display the rest
        in_names.pop(val)

        #get and erro check data
        print("\nPlease Select File Destination by its number")
        for i in range(len(in_names)):print('[%d]\t%s' % ((i+1), in_names[i]))
        print('[%d]\t%s' % ((len(in_names)+1), "All"))
        out = input("Choice : ")
        val2 = int(out)-1
        # If all is selected create all the files
        if val2 == len(in_names):
            for i in in_names:
                function = 'mk_'+i.lower()
                ift.pick_format(function,fil)
        elif val2 > len(in_names) or val < 0: raise Exception('Value out of range')
        else:
            # Save the file in new format
            function = 'mk_'+in_names[val2].lower()
            ift.pick_format(function,fil)
    else: raise Exception('That value is out of range')
except ValueError:
    print('Please enter an Int')
