const express = require('express');
const { execSync } = require('child_process');
const app = express();
const port = 8200;

function getSystemInfo() {
    const ipAddress     = execSync("hostname -I").toString().trim();
    const processes     = execSync("ps -ax").toString();
    const diskSpace     = execSync("df -h /").toString();
    const uptime        = execSync("uptime -p").toString();
    return {
        ip_address  : ipAddress,
        processes   : processes,
        disk_space  : diskSpace,
        uptime      : uptime
    };
}

app.get('/', 
        (req, res) => {
    res.json(getSystemInfo());
});

app.listen(port, () => {
    console.log(`Service2 listening at http://0.0.0.0:${port}`);
});
