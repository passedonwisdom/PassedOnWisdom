
            function myFunction() {
                var x = document.getElementById("myTopnav");
                if (x.className === "topnav") {
                x.className += " responsive";
                } else {
                x.className = "topnav";
                }
            }
        

    
              window.onscroll = function() {scrollFunction()};
              
              function scrollFunction() {
                if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
                  document.getElementById("myTopnav").style.opacity = "0.8";
                  document.getElementById("myTopnav").style.boxShadow = "#1a1919 0px 0.5px 2px";
                  document.getElementById("top").style.display = "block";

                } else {
                  document.getElementById("myTopnav").style.opacity = "1";
                  document.getElementById("myTopnav").style.boxShadow = "0px 0px 0px";
                  document.getElementById("top").style.display = "none";
                }
              }

              function block(){
                document.getElementById("dropdown").style.display = "block";
            }
            function none(){
                document.getElementById("dropdown").style.display = "none";
            }
            function topFunction() {
              document.body.scrollTop = 0;
              document.documentElement.scrollTop = 0;
            }
