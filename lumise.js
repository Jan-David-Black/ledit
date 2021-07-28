jQuery.loadScript = function (url, callback) {
    jQuery.ajax({
        url: url,
        dataType: 'script',
        success: callback,
        async: true
    });
}

if (typeof someObject == 'undefined') $.loadScript('https://docs.opencv.org/3.4.0/opencv.js', function(){
    //Stuff to do after someScript has loaded
});

// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'raw'
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: data // body data type must match "Content-Type" header
    });
    return response.text(); // parses JSON response into native JavaScript objects
  }
  

function testImg() {						
    var format = "png",
        include_base = false,
        full = true,
        overflow = false,
        stage = lumise.stage(),
        func = "download";
    
    lumise.get.el('zoom').val('100').trigger('input');

    lumise.f("checking your design");	

    var psize = lumise.get.size();
    
    lumise.fn.uncache_large_images(function() {
                
        lumise.fn.download_design({
            type: 'png',
            orien: psize.o,
            height: psize.h,
            width: psize.w,
            include_base: include_base,
            callback: function(data) {
                
                /*
                *	 Revert cache of large images
                */
                
                lumise.fn.uncache_large_images(null, true);
                if (data.length < 10)
                    return alert(lumise.i(36));

                
                postData('http://localhost:8000', data.replace("data:image/png;base64,",""))
                .then(data => {
                  console.log(data); // JSON data parsed by `data.json()` call
                  if(data === "True"){lumise.cart.add_cart('button add cart click');
                  }else{alert("Your design is not sufficiently connected")}
                  lumise.f();
                });
            }	
        });
        
    });

}
$('#lumise-cart-action').click(testImg);