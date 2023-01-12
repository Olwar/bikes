// api url
const api_url = "http://127.0.0.1:8000/1";

// gets all the drone data from the fastapi
async function getapi(url) {
    const response = await fetch(url);
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}

// updates the table without manual refresh
function startLiveUpdate() {
    setInterval(function() {
        getapi(api_url);
    }, 200000);
}

document.addEventListener('DOMContentLoaded', function () {
    startLiveUpdate();
});

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
// Defining the table for the drone data
function show(data) {
    let tab =  
           `<tr>
                <th>Departure Time</th>
                <th>Return Time</th>
                <th>Departure Station Id</th>
                <th>Departure Station Name</th>
                <th>Return Station Id</th>
                <th>Return Station Name</th>
                <th>Covered Distance (m)</th>
                <th>Duration (sec.)</th>
            </tr>`;
    for (r of data) {
        tab += `
        <table>
            <tr>
                <td>${r[0]}</td>
                <td>${r[1]}</td>
                <td>${r[2]}</td>
                <td>${r[3]}</td>
                <td>${r[4]}</td>
                <td>${r[5]}</td>
                <td>${r[6]}</td>
                <td>${r[7]}</td>
            </tr>
        </table>`;
    }
    document.getElementById("rides").innerHTML = tab;
}
