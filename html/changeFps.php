<?php
$file = fopen("status.txt", "w");
fwrite($file, "0");
fclose($file);
echo "Zmena statu otovo :D";
?>
