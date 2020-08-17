<?php
$values = $_GET["values"];
$pic = $_GET["pic"];

$file = fopen("settings.txt", "w");
fwrite($file, $values);
fclose($file);

if ($pic == 1){
	$file = fopen("status.txt", "w");
	fwrite($file, "1");
	fclose($file);
}

echo "hotovo :D";
?>
