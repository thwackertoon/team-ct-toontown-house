<?php

function fgetcont($filepath) {
    $f = fopen($filepath,"rb");
    $size = filesize($filepath);
    $data = fread($f,$size);
    fclose($f);
    return $data;
}

function fputcont($filepath,$data) {
    $f = fopen($filepath,"rb");
    fwrite($f,$data);
    fclose($f);
}

function gzdecode($data) 
{ 
   return zlib_decode(substr($data,10,-8)); 
} 

    
            $data = gzdecode($data);
            $chr1 = chr(1);
            $data = explode($chr1,$data);
        }
        
        else $data=array();
        $this->files = array();
        
        if (count($data) >= 2) {
        
            $_range = range(0,count($data),2);
            
        }
?>