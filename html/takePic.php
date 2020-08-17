<?php
$f = $_GET["f"];

try {
	$output = passthru("python3 shot.py $f");
	echo $output;
} catch (Exception $e) {
	echo "Ajaj, chybka: ", $e->getMessage(), "\n";
}
?>
