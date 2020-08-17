<?php

$dir = __DIR__ . "/gallery";
$images = scandir($dir);

$response = "";
foreach ($images as $img)
{
	if ($img != "." && $img != "..")
	{
		$response .= $img . "|";
	}
}
echo $response;

?>
