// Create a XMLHttpRequest object to handle REST calls
// TODO: Switch to fetch API
let request = new XMLHttpRequest();  


///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////


// Reset and clear all components on the page
// window.onload = clear_and_reset_all()


///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////


function http_request_helper(method, ip, port, endpoint, args_dict){
    ////////////////////////////////////////////////
    // Usage:
    //      GET
    //          let time = http_request_helper('GET', picell_ip, '5000', 'get_time')
    //      POST
    //          let response = http_request_helper('POST', null, '', apc_on_off, {'fixture_euid':fixture_euid_selected})
    ////////////////////////////////////////////////

    // Adding any passed arguments in key:value dict format
    argText = ''
    if (args_dict != null){
        argText += '?'
        for(let key in args_dict){
            let value = args_dict[key]
            argText = argText + key + '=' + value + '&'
        }
    }
    argText = argText.substring(0, argText.length - 1);

    // Forming the request
    if (ip != null){
        // Sending request to remote location (picell)
        request_url = 'http://' + ip + ':' + port + '/' + endpoint + argText
    } else {
        // Sending request to local flask server
        request_url = endpoint + argText
    }
    console.log('Sending Request: ' + request_url)

    // Sending the request
    try {
        request.open(method.toUpperCase(), request_url, false);
        request.setRequestHeader('Access-Control-Allow-Origin', '*')
        request.send();
        return request.responseText;
    } catch(error) {
        console.warn("ERROR: Failed to send request. Response: " + error)
        return null;
    }
    
}


///////////////////////////////////////////////////////////////////////////////////////////////////


function start_slideshow() {
    // Starting the image slideshow
    let response = http_request_helper('POST', null, 5555, 'start')
    start_doing_stuff()
}

function stop_slideshow() {
    // Stopping the image slideshow
    let response = http_request_helper('POST', null, 5555, 'stop')
    stop_doing_stuff()
}

///////////////////////////////////////////////////////////////////////////////////////////////////

// Do something at a regular interval
function start_doing_stuff() {
    // If doing_stuff is already doing, stop doing it
    if ((typeof doing_stuff_timer !== 'undefined')) {
        clearInterval(doing_stuff_timer);  
    }
    // Start data acquisition timer at regular integral
    doing_stuff_timer = setInterval(function() { doing_stuff() }, 500);
}
function stop_doing_stuff() {
    // Stopping PyBoard dim value data acquisition
    clearInterval(doing_stuff_timer);
}
function doing_stuff() {
    // do stuff here
    let response = http_request_helper('GET', null, 5555, 'status')
    success = (response != null) ? JSON.parse(response)['success'] : false;

    if (success) {
        document.getElementById("img-last-preview").src = JSON.parse(response)['img_last']['img_last_rel_path'];
        document.getElementById("img-last-filepath").innerText = JSON.parse(response)['img_last']['img_last_rel_path']

        document.getElementById("img-now-preview").src = JSON.parse(response)['img_now']['img_now_rel_path'];
        document.getElementById("img-now-filepath").innerText = JSON.parse(response)['img_now']['img_now_rel_path']
    } else {
        console.error('Failed to get current image information')
    }
}



// Setting Inner texts of element
// document.getElementById("picell-name").innerText = '-';

//////////////////////////////////////////////////////////////////

// Disabling element
// document.getElementById("btn-reboot-picell").disabled = true;

//////////////////////////////////////////////////////////////////

// Removing all listed in a select menu
// let fixture_power_select = document.getElementById("picell-power-fixture");
// let length = fixture_power_select.options.length;
// for (i = 0; i < length; i++) {
//     fixture_power_select.options[i] = null;
// }
// let length = fixture_power_select.options.length = 0;
// fixture_power_select.disabled = true;  // Disabling select

//////////////////////////////////////////////////////////////////

// Populating a select menu
// for(let i in fixture_sm_firmware){
//     if (!(isNaN(fixture_sm_firmware[i][0]))) {  // Omit any falsh binary that does not start with a number
//         let flash_version_option = document.createElement("option");  // Creating a select option
//         flash_version_option.text = fixture_sm_firmware[i];  // Adding the fixture name to the option
//         flash_version_select.add(flash_version_option);  // Adding the option to the select
//     }
// }
// flash_version_select.disabled = false

//////////////////////////////////////////////////////////////////

// Do something on the expension of a accordian panel
// $('#accordion3').on('show.bs.collapse', function () {
//     // When accordion panel expands do stuff ...
// });

//////////////////////////////////////////////////////////////////

// Do something at a regular interval
// function start_doing_stuff() {
//     // If doing_stuff is already doing, stop doing it
//     if ((typeof doing_stuff_timer !== 'undefined')) {
//         clearInterval(doing_stuff_timer);  
//     }
//     // Start data acquisition timer at regular integral
//     doing_stuff_timer = setInterval(function() { doing_stuff() }, 500);
// }
// function stop_doing_stuff() {
//     // Stopping PyBoard dim value data acquisition
//     clearInterval(doing_stuff_timer);
// }
// function doing_stuff() {
//     // do stuff here
// }

//////////////////////////////////////////////////////////////////

// // Showing  modal, then do something after it appears
// let apc_on_off_text = (apc_on_off == 'apc_on') ? 'up' : 'down'
// document.getElementById('modalLoader-text').innerText = '<Modal Message Here>'
// $('#modalLoader').modal('show');

// // After loading modal has appeared, proceed to send request
// $('#modalLoader').on('shown.bs.modal', async function (e) {
//     let success = false
//     // Define the function
//     async function do_something(){
//         // Do something here
//         // success = ?
//     };

//     // Execute the function
//     await do_something();

//     // Hiding loading modal after execution
//     setTimeout(function () { 
//         $('#modalLoader').modal('hide');
//     }, 2000);

//     // Show a warning modal if request has failed
//     $('#modalLoader').on('hide.bs.modal', async function (e) {
//         if (success == false){
//             document.getElementById('modalWarning-text').innerText = '<Error Message Here>'
//             $('#modalWarning').modal('show');
//         }
//     })
// })