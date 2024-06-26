nasm -f elf64 shellcode.asm -o shellcode.o
ld shellcode.o -o shellcode

objdump -D shellcode

objdump -d shellcode -M intel | grep '[0-9a-f]:' | grep -v 'file' | cut -f2 -d: | cut -f1-7 -d' ' | tr -s ' ' | tr '\t' ' ' | sed 's/ $//g' | sed 's/ /\\x/g' | paste -d '' -s | sed 's/^/"/' | sed 's/$/"/g'

