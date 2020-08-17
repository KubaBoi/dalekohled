<?php
$img = $_GET["img"];

function remove($image)
{
	if (!unlink("gallery/$image"))
	{
		echo "Tohle sem nemoh smazat $image :(";
	}
	else
	{
		echo "Smazáno :D";
	}
}

if ($img == "*")
{
	$dir = __DIR__ . "/gallery";
	$images = scandir($dir);
	foreach ($images as $im)
	{
		remove($im);
	}
}
else
{
	remove($img);
}
?>
