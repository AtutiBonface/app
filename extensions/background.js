chrome.runtime.onInstalled.addListener(function() {
   
  chrome.contextMenus.create({
    id : "imageContextMenus",
    title: "Download Image",
    contexts : ["image"]
  });

  
});

chrome.contextMenus.onClicked.addListener((info, tab)=>{
    if(info.menuItemId ===  'imageContextMenus'){        
        chrome.scripting.executeScript({
            target : {tabId : tab.id},
            func : (image)=>{
                alert(image.srcUrl)
                const link = document.createElement('a')
                link.href = image.srcUrl
                link.download = 'image';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link)                
            },
            args: [info]
        })
    }
    });
  

  