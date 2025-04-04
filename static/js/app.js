!(function (n) {
  "use strict";
  function a() {
    for (
      var e = document
          .getElementById("topnav-menu-content")
          .getElementsByTagName("a"),
        t = 0,
        n = e.length;
      t < n;
      t++
    )
      "nav-item dropdown active" === e[t].parentElement.getAttribute("class") &&
        (e[t].parentElement.classList.remove("active"),
        e[t].nextElementSibling.classList.remove("show"));
  }
  function e() {
    document.webkitIsFullScreen ||
      document.mozFullScreen ||
      document.msFullscreenElement ||
      (console.log("pressed"), n("body").removeClass("fullscreen-enable"));
  }
  document.addEventListener("scroll", function () {
    var e;
    (e = document.getElementById("page-topbar")) &&
      (50 <= document.body.scrollTop || 50 <= document.documentElement.scrollTop
        ? e.classList.add("topbar-shadow")
        : e.classList.remove("topbar-shadow"));
  }),
    n("#side-menu").metisMenu(),
    n("#sidebar-btn").on("click", function (e) {
      e.preventDefault(),
        n("body").toggleClass("sidebar-enable"),
        992 <= n(window).width()
          ? n("body").toggleClass("sidebar-collpsed")
          : n("body").removeClass("sidebar-collpsed");
    }),
    n("body,html").click(function (e) {
      var t = n("#sidebar-btn");
      t.is(e.target) ||
        0 !== t.has(e.target).length ||
        e.target.closest("div.vertical-menu") ||
        n("body").removeClass("sidebar-enable");
    }),
    n("#sidebar-menu a").each(function () {
      var e = window.location.href.split(/[?#]/)[0];
      this.href == e &&
        (n(this).addClass("active"),
        n(this).parent().addClass("mm-active"),
        n(this).parent().parent().addClass("mm-show"),
        n(this).parent().parent().prev().addClass("mm-active"),
        n(this).parent().parent().parent().addClass("mm-active"),
        n(this).parent().parent().parent().parent().addClass("mm-show"),
        n(this)
          .parent()
          .parent()
          .parent()
          .parent()
          .parent()
          .addClass("mm-active"));
    }),
    n(".navbar-nav a").each(function () {
      var e = window.location.href.split(/[?#]/)[0];
      this.href == e &&
        (n(this).addClass("active"),
        n(this).parent().addClass("active"),
        n(this).parent().parent().addClass("active"),
        n(this).parent().parent().parent().addClass("active"),
        n(this).parent().parent().parent().parent().addClass("active"),
        n(this)
          .parent()
          .parent()
          .parent()
          .parent()
          .parent()
          .addClass("active"));
    }),
    n(document).ready(function () {
      var e;
      0 < n("#sidebar-menu").length &&
        0 < n("#sidebar-menu .mm-active .active").length &&
        300 < (e = n("#sidebar-menu .mm-active .active").offset().top) &&
        ((e -= 300),
        n(".vertical-menu .simplebar-content-wrapper").animate(
          { scrollTop: e },
          "slow"
        ));
    }),
    n('[data-toggle="fullscreen"]').on("click", function (e) {
      e.preventDefault(),
        n("body").toggleClass("fullscreen-enable"),
        document.fullscreenElement ||
        document.mozFullScreenElement ||
        document.webkitFullscreenElement
          ? document.cancelFullScreen
            ? document.cancelFullScreen()
            : document.mozCancelFullScreen
            ? document.mozCancelFullScreen()
            : document.webkitCancelFullScreen &&
              document.webkitCancelFullScreen()
          : document.documentElement.requestFullscreen
          ? document.documentElement.requestFullscreen()
          : document.documentElement.mozRequestFullScreen
          ? document.documentElement.mozRequestFullScreen()
          : document.documentElement.webkitRequestFullscreen &&
            document.documentElement.webkitRequestFullscreen(
              Element.ALLOW_KEYBOARD_INPUT
            );
    }),
    document.addEventListener("fullscreenchange", e),
    document.addEventListener("webkitfullscreenchange", e),
    document.addEventListener("mozfullscreenchange", e),
    n(".right-bar-toggle").on("click", function (e) {
      n("body").toggleClass("right-bar-enabled");
    }),
    n(document).on("click", "body", function (e) {
      0 < n(e.target).closest(".right-bar-toggle, .right-bar").length ||
        n("body").removeClass("right-bar-enabled");
    }),
    (function () {
      if (document.getElementById("topnav-menu-content")) {
        for (
          var e = document
              .getElementById("topnav-menu-content")
              .getElementsByTagName("a"),
            t = 0,
            n = e.length;
          t < n;
          t++
        )
          e[t].onclick = function (e) {
            "#" === e.target.getAttribute("href") &&
              (e.target.parentElement.classList.toggle("active"),
              e.target.nextElementSibling.classList.toggle("show"));
          };
        window.addEventListener("resize", a);
      }
    })(),
    [].slice
      .call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
      .map(function (e) {
        return new bootstrap.Tooltip(e);
      }),
    [].slice
      .call(document.querySelectorAll('[data-bs-toggle="popover"]'))
      .map(function (e) {
        return new bootstrap.Popover(e);
      }),
    n(window).on("load", function () {
      n("#status").fadeOut(), n("#preloader").delay(350).fadeOut("slow");
    }),
    (function () {
      var t = document.documentElement;
      t.hasAttribute("data-bs-theme") &&
      "light" == t.getAttribute("data-bs-theme")
        ? sessionStorage.setItem("data-layout-mode", "light")
        : "dark" == t.getAttribute("data-bs-theme") &&
          sessionStorage.setItem("data-layout-mode", "dark"),
        null == sessionStorage.getItem("data-layout-mode")
          ? t.setAttribute("data-bs-theme", "light")
          : sessionStorage.getItem("data-layout-mode") &&
            t.setAttribute(
              "data-bs-theme",
              sessionStorage.getItem("data-layout-mode")
            );
      var e = document.getElementById("light-dark-mode");
      e &&
        e.addEventListener("click", function (e) {
          t.hasAttribute("data-bs-theme") &&
          "dark" == t.getAttribute("data-bs-theme")
            ? (t.setAttribute("data-bs-theme", "light"),
              sessionStorage.setItem("data-layout-mode", "light"))
            : (t.setAttribute("data-bs-theme", "dark"),
              sessionStorage.setItem("data-layout-mode", "dark"));
        });
      var n = document.getElementById("layout-dir-btn");
      n &&
        n.addEventListener("click", function (e) {
          t.hasAttribute("dir") && "rtl" == t.getAttribute("dir")
            ? (t.setAttribute("dir", "ltr"),
              document
                .getElementById("bootstrap-style")
                .setAttribute("href", "/static/css/bootstrap.min.css"),
              document
                .getElementById("app-style")
                .setAttribute("href", "/static/css/app.min.css"),
              (this.innerHTML = "RTL"))
            : (t.setAttribute("dir", "rtl"),
              document
                .getElementById("bootstrap-style")
                .setAttribute("href", "/static/css/bootstrap-rtl.min.css"),
              document
                .getElementById("app-style")
                .setAttribute("href", "/static/css/app-rtl.min.css"),
              (this.innerHTML = "LTR"));
        });
    })(),
    Waves.init();
})(jQuery);
