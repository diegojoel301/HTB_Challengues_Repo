undefined8 main(void)

{
  int r1;
  time_t time_val;
  long in_FS_OFFSET;
  uint u_time;
  uint r2;
  long i;
  FILE *fd;
  size_t fd_ptr;
  void *ptr;
  FILE *fd1;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
                    /* Leer el contenido del flag
                        */
  fd = fopen("flag","rb");
  fseek(fd,0,2);
  fd_ptr = ftell(fd);
  fseek(fd,0,0);
  ptr = malloc(fd_ptr);
  fread(ptr,fd_ptr,1,fd);
  fclose(fd);
  time_val = time((time_t *)0x0);
  u_time = (uint)time_val;
  srand(u_time);
  for (i = 0; i < (long)fd_ptr; i = i + 1) {
    r1 = rand();
    *(byte *)((long)ptr + i) = *(byte *)((long)ptr + i) ^ (byte)r1;
    r2 = rand();
    r2 = r2 & 7;
    *(byte *)((long)ptr + i) =
         *(byte *)((long)ptr + i) << (sbyte)r2 | *(byte *)((long)ptr + i) >> 8 - (sbyte)r2;
  }
  fd1 = fopen("flag.enc","wb");
  fwrite(&u_time,1,4,fd1);
  fwrite(ptr,1,fd_ptr,fd1);
  fclose(fd1);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
