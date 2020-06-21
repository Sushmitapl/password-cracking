import sys
import crypt
from threading import Thread, Event
import time
import queue


# Function to get the password for single user
def getPasswordSingleUser(return_que, linux_username_password_list, sub_list):
    password_found = False
    for linux_user_passwd in linux_username_password_list:
        user_passwd = linux_user_passwd.split(':')
        user = user_passwd[0]
        password = user_passwd[1]
        linux_salt_passwd = password.split("$")
        if not linux_salt_passwd[0]:
            del linux_salt_passwd[0]
        for eachPassword in sub_list:
            hashedGuess = str(
                crypt.crypt(eachPassword, "$" + str(linux_salt_passwd[0]) + "$" + str(linux_salt_passwd[1]) + "$"))
            if hashedGuess == password:
                print("Found Password for {} : {}".format(user, eachPassword))
                password_found = True
                break;
    return_que.put(password_found)


# Function to get the password for multiple users
def getPasswordMultipleUser(return_que, list_common_passwords, sub_list):
    userFound = False
    for user_list in sub_list:
        user_passwd = user_list.split(':')
        user = user_passwd[0]
        password = user_passwd[1]
        linux_salt_passwd = password.split("$")
        if not linux_salt_passwd[0]:
            del linux_salt_passwd[0]
        for eachPassword in list_common_passwords:
            hashedGuess = str(
                crypt.crypt(eachPassword, "$" + str(linux_salt_passwd[0]) + "$" + str(linux_salt_passwd[1]) + "$"))
            if hashedGuess == password:
                print("Found Password for {} : {}".format(user, eachPassword))
                userFound = True
                break;

    return_que.put(userFound)


# splitting the list into chunks for multithreading
def listChunks(pass_list, chunks):
    for i in range(0, len(pass_list), chunks):
        yield pass_list[i:i + chunks]


def main():
    # Define the list of the threads
    listOfThreads = []
    return_que = queue.Queue()
    deleting_list = False;

    # read the common password file
    with open(sys.argv[1], 'r') as f:
        list_common_passwords = [line.strip() for line in f]

    # read the Password file
    with open(sys.argv[2], 'r') as f:
        linux_username_password_list = [line.strip() for line in f]

    # Condition to determine the lists to be divided into chunks
    if len(linux_username_password_list) > 1:
        new_linux_username_password_list = list(listChunks(linux_username_password_list, 5))
        for sub_list in new_linux_username_password_list:
            listOfThreads.append(
                Thread(target=getPasswordMultipleUser, args=(return_que, list_common_passwords, sub_list)))
    else:
        new_List_of_Common_Passwords = list(listChunks(list_common_passwords, 10))
        print("new_List_of_Common_Passwords : ", new_List_of_Common_Passwords)
        for sub_list in new_List_of_Common_Passwords:
            listOfThreads.append(
                Thread(target=getPasswordSingleUser,
                       args=(return_que, linux_username_password_list, sub_list)))

    # Start the threads in the list
    for thread in listOfThreads:
        thread.start()

    # Waits for threads to terminate
    for thread in listOfThreads:
        thread.join()
        while not return_que.empty():
            if return_que.get():
                print("Password Search Complete.")
                deleting_list = True;
                del listOfThreads

    # Print if no password found.
    if not deleting_list:
        print("Password Search Complete.No Password found")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main()
    else:
        print("Run the tool as ./cracker.py <list_of_common_password> <list_of_password_username>")
