const  button = document.getElementById('btn')


button.addEventListener('click', ()=>{
    chrome.runtime.sendMessage({type: "link", url : "thisisbonface.imaginekenya.site/home.png"}, (response)=>{
        
    })

})

