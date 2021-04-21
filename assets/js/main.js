
(function ($) {
    "use strict";

    /*------------------------
    detect IE
    ------------------------*/
    var t;
    (-1 != (t = navigator.userAgent.toLowerCase()).indexOf("msie") || -1 != t.indexOf("trident")) && $("body").addClass("ie");

    /*------------------------
    gallery
    ------------------------*/
    $(".zoom-gallery").length && $(".zoom-gallery").each(function () {
        $(this).magnificPopup({
            delegate: "a.ne-zoom",
            type: "image",
            gallery: {
                enabled: true,
                tPrev: 'قبلی',
                tNext: 'بعدی',
                tCounter: '<span class="mfp-counter">%curr% از %total%</span>'
            }
        })
    });

    /*------------------------
    top search button
    ------------------------*/
    $(document).on("click", "#top-search-form .search-button", function (a) {
        return a.preventDefault(), $(this).prev("input.search-input").animate({
            opacity: "toggle"
        }, 500, "linear"), false
    });

    /*------------------------
    load more button
    ------------------------*/
    $(".loadmore").on("click", "a", function (e) {
        e.preventDefault();
        var t = $(this),
            n = t.parents(".menu-list-wrapper").find(".menu-list .menu-item.hidden").slice(0, 3);
        if (n.length) {
            n.css({
                opacity: 0
            });
            n.promise().done(function () {
                n.removeClass("hidden");
                n.show().animate({
                    opacity: 1
                }, 500);
            });
        } else {
            t.text("آیتم دیگری وجود ندارد");
        }
    });

    /*------------------------
    mobile menu
    ------------------------*/
    // $("nav#dropdown").meanmenu({
    //     siteLogo: "<div class='mobile-menu-nav-back'><a href='/' class='logo-mobile'><img src=''/></a></div>"
    // });

    /*------------------------
    scroll up button
    ------------------------*/
    (new WOW).init(), $.scrollUp({
        scrollText: '<i class="fa fa-angle-double-up"></i>',
        easingType: "linear",
        scrollSpeed: 900,
        animation: "fade"
    });

    /*------------------------
    sidemenu
    ------------------------*/
    $("#wrapper").on("click", "#side-menu-trigger a.menu-bar", function (a) {
        a.preventDefault();
        var t = $(this),
            n = $(this).parents("body").find(">#wrapper"),
            o = $("<div />").addClass("offcanvas-mask");
        return n.addClass("open").append(o), t.addClass("open"), t.next(".menu-times").removeClass("close"), document.getElementById("offcanvas-body-wrapper").style.left = "0", false
    });

    $("#wrapper").on("click", "#side-menu-trigger a.menu-times", function (a) {
        a.preventDefault();
        var t = $(this);
        return $("#offcanvas-body-wrapper").attr("style", ""), t.prev(".menu-bar").removeClass("open"), t.addClass("close"), o(), false
    });

    $("#wrapper").on("click", "#offcanvas-nav-close a", function (e) {
        return o(), false
    });

    $(document).on("click", "#wrapper.open .offcanvas-mask", function () {
        o()
    });

    $(document).on("keyup", function (e) {
        27 === e.which && (e.preventDefault(), o())
    });

    /*------------------------
    archive select
    ------------------------*/
    $("#archive-search select.select2").length && $("#archive-search select.select2").select2({
        theme: "classic",
        dropdownAutoWidth: true,
        width: "100%"
    });

    /*------------------------
    isotope
    ------------------------*/
    $(window).on("load", function () {
        $("#preloader").fadeOut("slow", function () {
            $(this).remove()
        });

        var a = $(".ne-isotope");
        a.length > 0 && a.each(function () {
            var a = $(this),
                t = a.find(".isotope-classes-tab a.current").attr("data-filter"),
                n = a.find(".featuredContainer").isotope({
                    filter: t,
                    originLeft: false,
                    animationOptions: {
                        duration: 750,
                        easing: "linear",
                        queue: false
                    }
                });
            a.find(".isotope-classes-tab").on("click", "a", function () {
                var a = $(this);
                a.parent(".isotope-classes-tab").find("a").removeClass("current"), a.addClass("current");
                var t = a.attr("data-filter");
                return n.isotope({
                    filter: t,
                    originLeft: false,
                    animationOptions: {
                        duration: 750,
                        easing: "linear",
                        queue: false
                    }
                }), false
            })
        });

        var t = $(".ne-isotope-all");
        if (t.length > 0) {
            var n = t.find(".isotope-classes-tab a.current").attr("data-filter");
            var o = t.find(".featuredContainer").isotope({
                filter: n,
                originLeft: false,
                animationOptions: {
                    duration: 750,
                    easing: "linear",
                    queue: false
                }
            });
            t.find(".isotope-classes-tab").on("click", "a", function () {
                var a = $(this);
                a.parent(".isotope-classes-tab").find("a").removeClass("current"), a.addClass("current");
                var t = a.attr("data-filter");
                return o.isotope({
                    filter: t,
                    originLeft: false,
                    animationOptions: {
                        duration: 750,
                        easing: "linear",
                        queue: false
                    }
                }), false
            })
        }

    });

    /*------------------------
    accordions
    ------------------------*/
    var s = $("#accordion");
    s.children(".panel").children(".panel-collapse").each(function () {
        $(this).hasClass("in") && $(this).parent(".panel").children(".panel-heading").addClass("active")
    });
    s.on("show.bs.collapse", function (a) {
        $(a.target).prev(".panel-heading").addClass("active")
    })
        .on("hide.bs.collapse", function (a) {
            $(a.target).prev(".panel-heading").removeClass("active")
        });

    /*------------------------
    contact form
    ------------------------*/
    var form = $("#contact-form");
    var form_message = form.find(".form-response");

    form.length && form.validator().on("submit", function (e) {

        if (!e.isDefaultPrevented()) {

            e.preventDefault();

            $.ajax({

                url: "php/mail.php",
                type: "POST",
                data: form.serialize(),

                beforeSend: function () {
                    form_message.html("<div class='alert alert-primary'><p>در حال ارسال ...</p></div>");
                },

                success: function (response) {
                    if (response === "success") {
                        form[0].reset();
                        form_message.html("<div class='alert alert-success'><p>پیام شما با موفقیت ارسال شد.</p></div>");
                    } else if (response === "error") {
                        form_message.html("<div class='alert alert-danger'><p>خطا در ارسال پیام.</p></div>");
                    } else {
                        form_message.html("<div class='alert alert-warning'><p>" + response + "</p></div>");
                    }
                },

                error: function () {
                    form_message.html("<div class='alert alert-danger'><p>خطا در ارسال پیام.</p></div>");
                }
            });
        } else {
            form_message.html("<div class='alert alert-warning'><p>لطفا همه فیلد های ضروری را وارد نمایید.</p></div>");
        }
    });

    /*------------------------
    login form
    ------------------------*/
    $(".login-form").on("click", ".form-cancel", function (a) {
        a.preventDefault();
        $(this).parents(".modal-content").find('.modal-header .close').click();
    });

    /*------------------------
    google map
    ------------------------*/
    $("#googleMap").length && (window.onload = function () {
        var e = {
                mapTypeControlOptions: {
                    mapTypeIds: ["Styled"]
                },
                center: new google.maps.LatLng(38.064947, 46.327591),
                zoom: 14,
                disableDefaultUI: true,
                mapTypeId: "Styled"
            },
            a = document.getElementById("googleMap"),
            t = new google.maps.Map(a, e),
            n = (new google.maps.Marker({
                position: t.getCenter(),
                animation: google.maps.Animation.BOUNCE,
                icon: "img/map-marker.png",
                map: t
            }), new google.maps.StyledMapType([{
                featureType: "water",
                elementType: "geometry.fill",
                stylers: [{
                    color: "#b7d0ea"
                }]
            }, {
                featureType: "road",
                elementType: "labels.text.fill",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "road",
                elementType: "geometry.stroke",
                stylers: [{
                    visibility: "off"
                }]
            }, {
                featureType: "road.highway",
                elementType: "geometry",
                stylers: [{
                    color: "#c2c2aa"
                }]
            }, {
                featureType: "poi.park",
                elementType: "geometry",
                stylers: [{
                    color: "#b6d1b0"
                }]
            }, {
                featureType: "poi.park",
                elementType: "labels.text.fill",
                stylers: [{
                    color: "#6b9a76"
                }]
            }], {
                name: "Styled"
            }));
        t.mapTypes.set("Styled", n)
    });

    /*------------------------
    carousel
    ------------------------*/
    $(".ne-carousel").each(function () {
        var a = $(this),
            t = a.data("loop"),
            n = a.data("items"),
            o = a.data("margin"),
            s = (a.data("stage-padding"), a.data("autoplay")),
            r = a.data("autoplay-timeout"),
            i = a.data("smart-speed"),
            l = a.data("dots"),
            d = a.data("nav"),
            p = a.data("nav-speed"),
            c = a.data("r-x-small"),
            m = a.data("r-x-small-nav"),
            u = a.data("r-x-small-dots"),
            f = a.data("r-x-medium"),
            g = a.data("r-x-medium-nav"),
            v = a.data("r-x-medium-dots"),
            y = a.data("r-small"),
            h = a.data("r-small-nav"),
            w = a.data("r-small-dots"),
            b = a.data("r-medium"),
            C = a.data("r-medium-nav"),
            k = a.data("r-medium-dots"),
            T = a.data("r-Large"),
            x = a.data("r-Large-nav"),
            D = a.data("r-Large-dots"),
            S = a.data("center");

        a.owlCarousel({
            rtl: true,
            loop: !!t,
            items: n || 4,
            lazyLoad: true,
            margin: o || 0,
            autoplay: !!s,
            autoplayTimeout: r || 1e3,
            smartSpeed: i || 250,
            dots: !!l,
            nav: !!d,
            navText: ['<i class="fa fa-angle-right" aria-hidden="true"></i>', '<i class="fa fa-angle-left" aria-hidden="true"></i>'],
            navSpeed: !!p,
            center: !!S,
            responsiveClass: true,
            responsive: {
                0: {
                    items: c || 1,
                    nav: !!m,
                    dots: !!u
                },
                480: {
                    items: f || 2,
                    nav: !!g,
                    dots: !!v
                },
                768: {
                    items: y || 3,
                    nav: !!h,
                    dots: !!w
                },
                992: {
                    items: b || 4,
                    nav: !!C,
                    dots: !!k
                },
                1200: {
                    items: T || 5,
                    nav: !!x,
                    dots: !!D
                }
            }
        })
    });

    /*------------------------
    header adjustments
    ------------------------*/
    var header_height = $(".header-menu-fixed").outerHeight();

    $(window).on("load resize", function () {

        var mean_height = $(window).height() - $(".mobile-menu-nav-back").outerHeight();
        $(".mean-nav > ul").css("height", mean_height + "px");

        if ($(".header-menu-fixed").outerHeight() > header_height) {
            header_height = $(".header-menu-fixed").outerHeight();
        }

        if (window.innerWidth < 992) {
            $("body.mean-container").css("margin-top", 0);
            $("body.mean-container #wrapper").css("background-position-y", 0);
            $(".add-top-margin").css({
                "margin-top": 0
            });
        } else {
            $(".add-top-margin").css({
                "margin-top": header_height + "px"
            });
        }
    });

    /*------------------------
    sticky header
    ------------------------*/
    $(window).on("scroll load resize", function () {
        var a = $("#sticker"),
            t = a.outerHeight(),
            n = $(window).scrollTop(),
            o = window.innerWidth,
            s = $("#header-layout1"),
            r = $("#header-layout2");
        if (o > 991) {
            var i = 1;
            r.length && (i = r.find(".header-top-bar").outerHeight()), n >= i ? (s.length && a.addClass("stick"), r.length && (a.addClass("stick"), $(".main-menu-area").addClass("header-menu-fixed"), $("body").css({
                "margin-top": t + "px"
            }), $("#wrapper").css({
                "background-position-y": "-" + t + "px"
            }))) : (a.removeClass("stick"), r.length && (a.removeClass("stick"), $(".main-menu-area").removeClass("header-menu-fixed"), $("body").css({
                "margin-top": 0
            }), $("#wrapper").css({
                "background-position-y": 0
            })))
        }
    });

    /*------------------------
    masonry gallery
    ------------------------*/
    $(".masonry-items").masonry({
        itemSelector: ".masonry-item",
        columnWidth: ".masonry-item"
    });

    /*------------------------
    youtube popup
    ------------------------*/
    var n = $(".popup-youtube");

    function o() {
        var a = $("body").find(">#wrapper"),
            t = $("#side-menu-trigger a.menu-times");
        a.removeClass("open").find(".offcanvas-mask").remove(), $("#offcanvas-body-wrapper").attr("style", ""), t.prev(".menu-bar").removeClass("open"), t.addClass("close")
    }

    n.length && n.magnificPopup({
        disableOn: 700,
        type: "iframe",
        mainClass: "mfp-fade",
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    /*------------------------
    search width control
    ------------------------*/
    $(window).on("load resize", function () {

        var $width = 0;

        if (window.innerWidth < 768) {
            $width = $('.mobile-menu-nav-back').width() - $('.main-menu-area .header-action-item').width() - 119;
        } else if (window.innerWidth < 992) {
            $width = $('.mobile-menu-nav-back').width() - $('.main-menu-area .header-action-item').width() - 127;
        } else {
            if ($('.header-style1').length > 0 || $('.header-style6').length > 0 || $('.header-style7').length > 0) {
                $width = $('.main-menu-area .container').width() - $('.main-menu-area .logo-area').width() - $('.main-menu-area .header-action-item').width() - 96;
            } else if ($('.header-style2').length > 0) {
                $width = $('.main-menu-area .container').width() - $('.main-menu-area .header-action-item').width() - 78;
            } else if ($('.header-style3').length > 0 || $('.header-style4').length > 0) {
                $width = $('.main-menu-area .container').width() - $('.main-menu-area .header-action-item').width() - 111;
            } else if ($('.header-style5').length > 0) {
                $width = $('.main-menu-area .container').width() - $('.main-menu-area .header-action-item').width() - 173;
            }
        }

        if ($width) {
            $('.main-menu-area .search-input').width($width);
        }
    });

})(jQuery);
