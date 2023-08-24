<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div id="background">
    
    <h1>How it works</h1>
    <p><i>AI will propose you solutions one at a time. You evaluate them and tell the AI. You can always propose solutions and steer the AI.</i></p>
    
    <div class="slideshow-container">

    <div class="mySlides fade">
        <img src="Pictures/Picture1.png" style="width:350px">
    </div>
    
    <div class="mySlides fade">
        <img src="Pictures/Picture2.png" style="width:350px">
    </div>
    
    <div class="mySlides fade">
        <img src="Pictures/Picture3.png" style="width:350px">
    </div>
    
    </div>
    <br>
    
    <div style="text-align:center">
        <span class="dot"></span> 
        <span class="dot"></span> 
        <span class="dot"></span> 
    </div>

    <div style="text-align: right;">
        <form action="/Demo/define.php">
            <input type="submit" value="Ready" class="button" style="width: 20%;"/>
        </form>
    </div>
    </div>
 
    <style>
        .mySlides {
            display: none;
        }
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        /* Slideshow container */
        .slideshow-container {
            max-width: 1000px;
            position: relative;
            margin: auto;
        }
        .active {
            background-color: #717171;
        }
    </style>
    
    <script>
        let slideIndex = 0;
        showSlides();
        
        function showSlides() {
          let i;
          let slides = document.getElementsByClassName("mySlides");
          let dots = document.getElementsByClassName("dot");
          for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";  
          }
          slideIndex++;
          if (slideIndex > slides.length) {slideIndex = 1}    
          for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
          }
          slides[slideIndex-1].style.display = "block";  
          dots[slideIndex-1].className += " active";
          setTimeout(showSlides, 2000); // Change image every 2 seconds
        }
    </script>

    </body>
</html>

