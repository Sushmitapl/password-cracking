## Only for Educational Purpose ##

# Linux Password Cracking Tool
The tool can be used to crack Linux Password File using dictionary method. It uses multithreading to perform the password search thus, improving the efficiency of the attack.

## Getting Started
The tool requires two input:\
wordlist: common password file\
Linux password file: It can be retrieved by using /etc/passwd and /etc/shadow of a Linux machine. 

Following command can be used to run the tool:
```
python3 cracker.py <wordlist> <linux_password_file>
```
