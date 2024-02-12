#ASLR derandomization
sudo sysctl -w kernel.randomize_va_space=0



gcc -o exploit2 exploit2.c


gcc -o exploit1 exploit2.c


gcc -o vulnerable2 -z execstack -fno-stack-protector vulnerable2.c
gcc -o vulnerable1 -z execstack -fno-stack-protector vulnerable1.c

gcc -o address -z execstack -fno-stack-protector address.c

sudo chown root address
sudo chmod 4755 address

sudo chown root vulnerable2
sudo chmod 4755 vulnerable2

sudo chown root vulnerable1
sudo chmod 4755 vulnerable1

