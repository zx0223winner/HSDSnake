#!/bin/bash


path=`pwd`

echo -e "The current directory will be added to your \$PATH environmental variable\n\n>> $path\n"

sleep 1

echo Setting the \$PATH variable in the \~\/.bashrc file


echo "\n# added by DupGen_finder" >> ~/.bashrc

echo PATH=$path/scripts/DupGen_finder:\$PATH >> ~/.bashrc
#sed -i '$a PATH='$path':\$PATH' ~/.bashrc
sleep 1

echo Loading the new \$PATH into the current shell session

#echo -e "...\n"


sleep 1

echo Done!
