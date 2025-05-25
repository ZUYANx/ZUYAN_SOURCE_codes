<?php
// ========== SETTINGS ==========
$developer = "MR SILENT";
$wallet_address = "EQB1cU8lQPKrA_XYIhZJFLlNCTQK_2LmMZBoqLQH9keD7U5L9"; // Target wallet address

// ========== FORM HANDLE ==========
if (isset($_POST['send'])) {
    $to = $_POST['to'];
    $amount = $_POST['amount'];
    $txid = strtoupper(bin2hex(random_bytes(12)));
    $status = "Success";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>TON Fake Payment | CS CYBER TEAM</title>
    <style>
        body {
            background: url("https://media.giphy.com/media/t6ABYvwhP8yng4OHPy/giphy.gif") no-repeat center center fixed;
            background-size: cover;
            color: #00ff99;
            font-family: monospace;
            text-align: center;
        }
        .box {
            margin-top: 50px;
            background: rgba(0,0,0,0.6);
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
        }
        input, button {
            padding: 10px;
            border-radius: 5px;
            border: none;
            margin: 5px;
            width: 80%;
        }
        .success {
            background: #001f1f;
            border: 1px solid #00ff99;
            margin-top: 20px;
            padding: 10px;
            border-radius: 8px;
        }
        a {
            color: #00ffff;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>TON Fake Transaction Sender</h2>
        <form method="post">
            <input type="text" name="to" placeholder="Receiver Wallet Address" required><br>
            <input type="text" name="amount" placeholder="Amount (TON)" required><br>
            <button type="submit" name="send">Send (Fake)</button>
        </form>

        <?php if(isset($status)): ?>
            <div class="success">
                <h3>Fake Payment Sent!</h3>
                <p><strong>To:</strong> <?php echo htmlspecialchars($to); ?></p>
                <p><strong>Amount:</strong> <?php echo htmlspecialchars($amount); ?> TON</p>
                <p><strong>TXID:</strong> <?php echo $txid; ?></p>
                <p><strong>Status:</strong> <?php echo $status; ?></p>
            </div>
        <?php endif; ?>

        <br><br>
        <a href="https://t.me/CS_CYBER_TEAM">Join CS CYBER TEAM</a><br>
        <small>Developed by <?php echo $developer; ?></small>
    </div>
</body>
</html>