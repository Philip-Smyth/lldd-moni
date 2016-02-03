<?php
$q = intval($_GET['q']);

$con = mysqli_connect('localhost','root','password','discover')
if (!$con){
	die('Could not connect: ' . mysqli_error($con));
}

#mysqli_select_db($con, "discover");
$sql="SELECT * FROM nodes WHERE OS = '".$q."'";
$result = mysqli_query($con,$sql);
#
#echo $result;

echo "<table>
<tr>
<th>Id</th>
<th>Hostname</th>
<th>MAC_Addr</th>
<th>IP_Addr</th>
<th>OS</th>
<th>OS_Vrs</th>
<th>OS_Type</th>
<th>OS_Acc</th>
</tr>";
echo "</table>"
if ($result->num_rows > 0){
	#while($row = mysqli_fetch_array($result)){
		#echo "<tr>";
		#echo "<td>" . $row['Id'] . "</td>";
		#echo "<td>" . $row['Hostname'] . "</td>";
		#echo "<td>" . $row['MAC_Addr'] . "</td>";
		#echo "<td>" . $row['IP_Addr'] . "</td>";
		#echo "<td>" . $row['OS'] . "</td>";
		#echo "<td>" . $row['OS_Vrs'] . "</td>";
		#echo "<td>" . $row['OS_Type'] . "</td>";
		#echo "<td>" . $row['OS_Acc'] . "</td>";
		#echo "</tr>";
	#}
	
} else {
	echo "Empty";
}
;

mysqli_close($con);
?>