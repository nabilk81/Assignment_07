#------------------------------------------#
# Title: CDInventory.py
# Desc: CD Inventory: Working with the pickle module, binary file and structured error handling.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# NKnight, 2022-Mar-06, Updating File
# NKnight, 2022-Mar-13, Updating file to include 
# structure error handling and using a binary file
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
intIDDel = ''


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod 
    def user_input_proc():
        """
        Function to put user data into a list of dictionaries

        Args:
            None.

        Returns
            None.

        """
        user_lst = IO.user_input()
        dicRow = {'ID': user_lst[0], 'Title': user_lst[1], 'Artist': user_lst[2]}
        lstTbl.append(dicRow)
        return


    @staticmethod 
    def del_row():
        """
        Function to delete rows in memory
        
        Args:
            None

        Returns
        -------
        None.

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from binary file using the pickle module to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table, one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        """
        with open(file_name, 'rb') as objFile:
            table = pickle.load(objFile)
        return table

    @staticmethod
    def write_file(table, file_name):
        """
        Function to save cd inventory from memory to binary file using the pickle module
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns
        -------
        None.

        """

        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)
        


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        #print(table)
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

   
    @staticmethod
    def user_input():
        """Function to get user input for CD inventory to put into memory
        
        Arg:  none
        
        Return: list of user inputs 
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        intID = int(strID)
        user_lst = [intID, strTitle, stArtist]
        return user_lst

    

try:
# 1. When program starts, read in the currently saved Inventory
    FileProcessor.read_file(strFileName)
except FileNotFoundError as e:
    e = 'No such CD Inventory file exists, please enter CD info and save'
    print(e + '\n')
    #print(type(e), e, __doc__, sep = '|n')
except EOFError as e:
    e = 'Empty File, please enter CD Inventory to be saved'
    print(e)
    # 2. start main loop

while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    try:
        strChoice = IO.menu_choice()
    except:
        print('Please choose an option from the menu: l, a, i, d, s or x')

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            try:
                lstTbl = FileProcessor.read_file(strFileName)
            except FileNotFoundError as e:
                print('\n')
                e = 'File not found: The CD Inventory file does not exist!'
                print(e +'\n')
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist

        # 3.3.2 Add item to the table
        try:
            DataProcessor.user_input_proc()
        except ValueError as e:
            print('\n')
            e = 'The ID you entered is not an integer, please try again!'
            print(e + '|n')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('\n')
            e = 'Oh No!! You didn\'t enter an interger, try again!'
            print(e)
        # 3.5.2 search thru table and delete CD
        try:
            DataProcessor.del_row()
        except ValueError as e:
            e = 'The ID you entered is not an integer, please try again!'
            print(e + '\n')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        try:
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        except:
            print('You did not enter y or n, please try again')
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(lstTbl, strFileName)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




