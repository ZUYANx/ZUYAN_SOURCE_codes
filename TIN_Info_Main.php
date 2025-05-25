<?php
// Author : https://t.me/x_LMNx9
// Team : https://t.me/TEAM_LMNx9

if (!isset($_GET['tin']) || empty($_GET['tin'])) {
    die(json_encode(["error" => "TIN parameter is required."]));
}
$tin = $_GET['tin'];
function fetch_certificate($tin, $cookie = null) {
    $url = "https://secure.incometax.gov.bd/ViewCertiifcate";
    $data = "NEW_TIN=" . urlencode($tin);
    $headers = [
        "Host: secure.incometax.gov.bd",
        "content-length: " . strlen($data),
        "sec-ch-ua-platform: \"Android\"",
        "x-requested-with: XMLHttpRequest",
        "user-agent: Mozilla/5.0 (Linux; Android 11; RMX3231 Build/RP1A.201005.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.164 Mobile Safari/537.36",
        "accept: */*",
        "sec-ch-ua: \"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Android WebView\";v=\"132\"",
        "content-type: application/x-www-form-urlencoded",
        "sec-ch-ua-mobile: ?1",
        "origin: https://secure.incometax.gov.bd",
        "sec-fetch-site: same-origin",
        "sec-fetch-mode: cors",
        "sec-fetch-dest: empty",
        "referer: https://secure.incometax.gov.bd/ViewCertiifcate",
        "accept-encoding: gzip, deflate, br, zstd",
        "accept-language: en-US,en;q=0.9",
        "cookie: " . ($cookie ?? "ASP.NET_SessionId=iifyb1ka1h33e1rg2q3awr41"),
        "priority: u=1, i"
    ];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_ENCODING, "gzip, deflate, br");
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return [$response, $http_code];
}
list($response, $http_code) = fetch_certificate($tin);
if ($http_code != 200) {
    if ($http_code == 400) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://secure.incometax.gov.bd/Registration/Login");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Host: secure.incometax.gov.bd",
            "Content-Length: 41",
            "Cache-Control: max-age=0",
            "Sec-CH-UA: \"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Android WebView\";v=\"132\"",
            "Sec-CH-UA-Mobile: ?1",
            "Sec-CH-UA-Platform: \"Android\"",
            "Origin: https://secure.incometax.gov.bd",
            "Content-Type: application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests: 1",
            "User-Agent: Mozilla/5.0 (Linux; Android 11; RMX3231 Build/RP1A.201005.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.164 Mobile Safari/537.36",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "X-Requested-With: mark.via.gp",
            "Sec-Fetch-Site: same-origin",
            "Sec-Fetch-Mode: navigate",
            "Sec-Fetch-User: ?1",
            "Sec-Fetch-Dest: document",
            "Referer: https://secure.incometax.gov.bd/Registration/Login",
            "Accept-Encoding: gzip, deflate, br, zstd",
            "Accept-Language: en-US,en;q=0.9",
            "Cookie: ASP.NET_SessionId=33e1rg2q3; browserMismatched=true; browserChecked=true",
            "Priority: u=0, i"
        ]);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, "LOGON_NAME=tc287dhaka&LOGON_PASS=mhdct287");
        $response = curl_exec($ch);
        $response_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($response_code == 302) {
            list($response, $http_code) = fetch_certificate($tin);
            if ($http_code != 200) {
                die(json_encode(["error" => "Failed to fetch data. HTTP code: " . $http_code]));
            }
        } else {
            die(json_encode(["error" => "Failed to fetch data. HTTP code: " . $http_code]));
        }
    } else {
        die(json_encode(["error" => "Failed to fetch data. HTTP code: " . $http_code]));
    }
}
$response = preg_replace('/<div class="before_footer" id="div_print_command">.*?<\/div>/s', '', $response);
preg_match('/TIN\s*:\s*(\d+)/', $response, $tin_match);
preg_match('/Name\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $name_match);
preg_match('/Father\'s Name\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $father_name_match);
preg_match('/Mother\'s Name\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $mother_name_match);
preg_match('/Current Address\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $current_address_match);
preg_match('/Permanent Address\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $permanent_address_match);
preg_match('/Previous TIN\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $previous_tin_match);
preg_match('/Status\s*:\s*<span style="font-weight: bold;">\s*(.*?)\s*<\/span>/', $response, $status_match);
preg_match('/Date\s*:\s*(.*?)\s*<\/td>/', $response, $date_match);
$result = [
    "TIN" => $tin_match[1] ?? null,
    "Name" => $name_match[1] ?? null,
    "Father's Name" => $father_name_match[1] ?? null,
    "Mother's Name" => $mother_name_match[1] ?? null,
    "Current Address" => $current_address_match[1] ?? null,
    "Permanent Address" => $permanent_address_match[1] ?? null,
    "Previous TIN" => $previous_tin_match[1] ?? null,
    "Status" => $status_match[1] ?? null,
    "Date" => $date_match[1] ?? null,
    "Owner" => "https://t.me/TEAM_LMNx9"
];
header("Content-Type: application/json");
echo json_encode($result);
?>