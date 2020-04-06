<?php
$src_file;
$in_file;
$out_file;
$rc_file;
$jexam;
$path;
$parser_only=FALSE;
$interpreter_only=FALSE;
$recursive=FALSE;
$parser_file;
$header_done=false;
function getparams(){
    $longopts = array(
        "help",
        "directory:",
        "recursive",
        "parse-script:",
        "parse-only",
        "int-script:",
        "int-only",
        "jexamxml:",
    );
    $options = getopt("", $longopts);
    global $src_file;
    global $in_file;
    global $out_file;
    global $rc_file;
    global $jexam;
    global $path;
    global $parser_only;
    global $parser_file;
    global $interpreter_only;
    global $interpreter_file;
    global $recursive;
foreach ($options as $index => $value) {
    switch ($index) {
        case "help":
            echo "toto je napoveda";
            break;
        case "directory":
            $path = $value;
            break;
        case "recursive":
            $recursive = TRUE;
            break;
        case "parse-script":
            $parser_file = $value;
            break;
        case "int-script":
            $interpreter_file = $value;
            break;
        case "parse-only":
            if ($interpreter_only == TRUE) {
                exit(11);
            }
            $parser_only = TRUE;
            break;
        case "int-only":
            if ($parser_only == TRUE) {
                exit(11);
            }
            $interpreter_only = TRUE;
            break;
        case "jexamxml":
            $jexam = $value;
            break;
    }
}
}
function get_files($type, $array, $path){
    $output_array=array();
    global $recursive;
    $cdir=scandir($path);
    $a=0;
    foreach ($cdir as $entry) {
        if ($entry == ".." || $entry == ".") {
            continue;
        }
        if(is_dir($path."/".$entry) && $recursive == true) {
            $output_array=array_merge($output_array,get_files($type, $array, $path . "/" . $entry));
            $a=count($output_array);
        }
        if ($type === "src") {
            if (preg_match("/.*\.src/", $entry)) {
                $output_array[$a] = $path . "/" . $entry;
                $a++;
            }
        }
        elseif ($type === "out"){
            $length=count($array);
            for($i=0; $i < $length; $i++){
                $match=substr($array[$i], strpos($array[$i], "/"));
                $match=pathinfo($match, PATHINFO_FILENAME);
                $match .=".out";
                if($match === $entry){
                    $output_array[$i] = $path . "/" . $entry;
                }
            }
        }
        elseif ($type === "rc"){
            $length=count($array);
            for($i=0; $i < $length; $i++){
                $match=substr($array[$i], strpos($array[$i], "/"));
                $match=pathinfo($match, PATHINFO_FILENAME);
                $match .=".rc";
                if($match === $entry){
                    $output_array[$i] = $path . "/" . $entry;
                }
            }
        }
    }
    return $output_array;
}
getparams();
if ($parser_only == true) {
    $src_array = get_files("src", "none", $path);
    $outfileshell;
    $i = 0;
    $number_bad_files = 0;
    $e = 0;
    $result_parse = 5;
    $result_interpret;
    $bad_file = "";
    $passed = 0;
    $d = 0;
    while ($i < count($src_array)) {
        $without_extension = substr_replace($src_array[$i], "", -4);
        $outfile = $without_extension . ".out";
        $rc_file = $without_extension . ".rc";
        if ($interpreter_only == false) {
            $command = "php " . $parser_file . " < " . $src_array[$i] . " > out.file";
            exec($command, $outfileshell, $result_parse);
        }
        if ($parser_only == false) {
            $command = "python3.8 " . $interpreter_file . " --source=" . $src_array[$i] . " --input=" . $inputfile . " > out.file";
            exec($command, $outfileshell, $result_interpret);
        }
        $exist = is_file($outfile);
        if ($exist == false) {
            $i++;
            continue;
        }
        $exist = is_file($rc_file);
        if ($exist == false) {
            $i++;
            continue;
        }
        $rc_value = file_get_contents($rc_file);
        if ($rc_value != $result_interpret) {
            $bad_file .= "<tr><td>RC error</td> <td>" . $src_array[$i] . "</td></tr>";
            $number_bad_files++;
            $i++;
            continue;
        }
        if ($rc_value != 0) {
            $passed++;
            $i++;
            continue;
        }
        if ($parser_only == false) {
            $command = "diff out.file " . $outfile;
        }
        if ($interpreter_only == false) {
            if ($rc_value != $result_parse) {
                $bad_file .= "<tr><td>RC error</td> <td>" . $src_array[$i] . "</td></tr>";
                $number_bad_files++;
                $i++;
                continue;
            }
            $command = "java -jar " . $jexam . " ./out.file " . "./" . $outfile;
        }
        exec($command, $outfileshell, $result);
        if ($result_parse == 0 || $result_interpret == 0) {
            $passed++;
        } else {
            $bad_file .= "<tr><td>JEXAMXL error</td> <td>" . $src_array[$i] . "</td></tr>";
            $number_bad_files++;
        }
        $i++;
    }
    if ($parser_only == true) {
        $type = "Parse";
    }
    $output_html = "<HTML><BODY style=\"margin: 0 auto; width: 1280px;\"><H1>Vysledky testux</H1><H3>Typ testu: " . $type . "</H3>";
    $output_html .= "<table>" . "<tr><td>Proslo</td><td>Neproslo</td></tr><tr><td>" . $passed . "</td><td>" . $number_bad_files . "</td></tr></table>";
    $output_html .= "<H3>Chybne testy:</H3><table><tr><td>Typ chyby</td><td>Soubor</td></tr>" . $bad_file . "</table>";
}
if ($interpreter_only == true) {
    $src_array = get_files("src", "none", $path);
    $outfileshell;
    $i = 0;
    $number_bad_files = 0;
    $e = 0;
    $result_parse = 5;
    $result_interpret;
    $bad_file = "";
    $passed = 0;
    $d = 0;
    while ($i < count($src_array)) {
        $without_extension = substr_replace($src_array[$i], "", -4);
        $outfile = $without_extension . ".out";
        $inputfile = $without_extension . ".in";
        $rc_file = $without_extension . ".rc";
        if(is_file($inputfile) != true){
            $inputfile="";
        }
        $command = "python3.8 " . $interpreter_file . " --source=" . $src_array[$i] . " --input=" . $inputfile . " > out.file";
        exec($command, $outfileshell, $result_interpret);
        $exist = is_file($outfile);
        if ($exist == false) {
            $i++;
            continue;
        }
        $exist = is_file($rc_file);
        if ($exist == false) {
            $i++;
            continue;
        }
        $rc_value = file_get_contents($rc_file);
        if ($rc_value != $result_interpret) {
            $bad_file .= "<tr><td>RC error</td> <td>" . $src_array[$i] . "</td></tr>";
            $number_bad_files++;
            $i++;
            continue;
        }
        if ($rc_value != 0) {
            $passed++;
            $i++;
            continue;
        }
        $command = "diff out.file " . $outfile;
        exec($command, $outfileshell, $result);
        if ($result_interpret == 0) {
            $passed++;
        } else {
            $bad_file .= "<tr><td>DIFF ERROR</td> <td>" . $src_array[$i] . "</td></tr>";
            $number_bad_files++;
        }
        $i++;
    }
    if ($interpreter_only == true) {
        $type = "Interpreter";
    }
    $output_html = "<HTML><BODY style=\"margin: 0 auto; width: 1280px;\"><H1>Vysledky testux</H1><H3>Typ testu: " . $type . "</H3>";
    $output_html .= "<table>" . "<tr><td>Proslo</td><td>Neproslo</td></tr><tr><td>" . $passed . "</td><td>" . $number_bad_files . "</td></tr></table>";
    $output_html .= "<H3>Chybne testy:</H3><table><tr><td>Typ chyby</td><td>Soubor</td></tr>" . $bad_file . "</table>";
}
$close_body="</BODY></HTML>";
$output_html.=$close_body;
echo($output_html);
echo "\n\n\n KONECNY VYSLEDEK:".$passed . "/".$i;
?>