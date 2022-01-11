$('.toggle-btn').click(function () {
    $('.navbar').toggleClass('active');
});
$(document).ready(function(){
   
    setInterval(()=>{
        if(window.innerWidth<500){
            $('ul li').click(function(){
                $(this).siblings().removeClass("active");
                $(this).toggleClass("active");
                console.log("hello");
                
            });
        }
    },10);
    $('.search-bar').click(function(){
        $(".search-sub-menu").toggleClass('active');
    })

});