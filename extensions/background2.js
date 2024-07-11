
const handle_websockets = (link)=>{
    var socket = new WebSocket("ws://127.0.0.1:65432");
      console.log("Attempting to establish WebSocket connection...");

      socket.onopen = function(event) {
          console.log("Socket connection established.");
          socket.send(link);
         
      };

      socket.onerror = function(error) {
          console.error("Socket error:", error);
      };

      socket.onclose = function(event) {
          console.log("Socket connection closed.");
      };
}



chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.type === "link") {
      var link = message.url;
      handle_websockets(link)
  }

 
  sendResponse({ message: "Thanks for the message!" });

 
  return true;
});
chrome.runtime.onInstalled.addListener(()=>{
    chrome.contextMenus.create({
        id: "imageContextMenus",
        title : "Download with BlackJuice",
        contexts :["image", "audio", "video"]
    })
})

chrome.contextMenus.onClicked.addListener((data, tab)=>{
    if(data.menuItemId === "imageContextMenus"){
        
        chrome.scripting.executeScript({
            target : {tabId : tab.id},
            func: handle_websockets,
            args : [data.srcUrl]
        })
    }
    
})

