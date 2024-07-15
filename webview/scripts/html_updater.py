html_updater_script = """
const htmlUpdater = new WebSocket(`ws://[=[host]=]:[=[port]=]/[=[html_updater_endpoint]=]`);

htmlUpdater.onmessage = function(event) {
    document.getElementById("main_update_content").innerHTML = event.data;
};
"""