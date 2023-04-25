param([string]$mode = "gen-input")

$n = 5
$is_all_eig = 1
$Rmin = 1
$Rmax = $n
$eigens = 1..$n
$is_set_solution = 1
$solutions = 1..$n

$eigen_accuracy = 0.0001
$opt_accuracy = 0.0001
$seidel_accuracy = 0.0001

$n > .\temp
$is_all_eig >> .\temp

if (1 -eq $is_all_eig) {
    foreach ($val in $eigens) {
        $val >> .\temp
    }
} else {
    $Rmin >> .\temp
    $Rmax >> .\temp
}

$is_set_solution >> .\temp

if (0 -ne $is_set_solution) {
    foreach ($val in $solutions) {
        $val >> .\temp
    }
}

Get-Content .\temp | .\Test3_W7_64x.exe > $null

if ("test" -eq $mode) {
    .\main.py $eigen_accuracy $opt_accuracy $seidel_accuracy > .\temp
    foreach ($line in Get-Content .\temp) {
        if ($line -like "Eigenvalues:*") {
            $words = $line.Split(' ')
            $res_values = 3..$words.Count
            for ($i = 0; $i -lt $res_values.Count; $i++) {
                $res_values[$i] = $words[$i+1] -as [double]
            }
            $res_values = $res_values | Sort-Object
            if (1 -eq $is_all_eig) {
                $eigens = $eigens | Sort-Object
                $dif = $false
                for ($i = 0; $i -lt $res_values.Count; $i++) {
                    if ([Math]::Abs($res_values[$i] - $eigens[$i]) -gt $eigen_accuracy) {
                        $dif = $true
                    }
                }
                if ($dif) {
                    "Eigenvalues incorrect"
                } else {
                    "Eigenvalues correct"
                }
            } else {
                if (($res_values[0] -ge $Rmin) -and ($res_values[-1] -le $Rmax)) {
                    "Eigenvalues correct"
                } else {
                    "Eigenvalues incorrect"
                }
            }
        }
        if ($line -like "Optimal roots:*") {
            $words = $line.Split(' ')
            $res_values = 4..$words.Count
            for ($i = 0; $i -lt $res_values.Count; $i++) {
                $res_values[$i] = $words[$i+2] -as [double]
            }
            if (0 -eq $is_set_solution) {
                $solutions = 1..$n
            }
            $res_values = $res_values | Sort-Object
            $solutions = $solutions | Sort-Object
            $dif = $false
            for ($i = 0; $i -lt $res_values.Count; $i++) {
                if ([Math]::Abs($res_values[$i] - $solutions[$i]) -gt $opt_accuracy) {
                    $dif = $true
                }
            }
            if ($dif) {
                "Optimal roots incorrect"
            } else {
                "Optimal roots correct"
            }
        }
        if ($line -like "Seidel roots:*") {
            $words = $line.Split(' ')
            $res_values = 4..$words.Count
            for ($i = 0; $i -lt $res_values.Count; $i++) {
                $res_values[$i] = $words[$i+2] -as [double]
            }
            if (0 -eq $is_set_solution) {
                $solutions = 1..$n
            }
            $res_values = $res_values | Sort-Object
            $solutions = $solutions | Sort-Object
            $dif = $false
            for ($i = 0; $i -lt $res_values.Count; $i++) {
                if ([Math]::Abs($res_values[$i] - $solutions[$i]) -gt $seidel_accuracy) {
                    $dif = $true
                }
            }
            if ($dif) {
                "Seidel roots incorrect"
            } else {
                "Seidel roots correct"
            }
        }
    }
}

Remove-Item .\temp -Force -Confirm:$false