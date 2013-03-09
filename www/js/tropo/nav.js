// Tropospherical Navigation JavaScript
//
// Authors:
//     Janine Costanzo <janine@netrophic.com>
//     Jesse Proulx <jproulx@jproulx.net>
//     Elizabeth Lubowitz <grrliz@gmail.com>
//
// Copyright (c) 2009 by Dreamwidth Studios, LLC.
//
// This program is NOT free software or open-source; you can use it as an
// example of how to implement your own site-specific extensions to the
// Dreamwidth Studios open-source code, but you cannot use it on your site
// or redistribute it, with or without modifications.
//

var Tropo = new Object();

Tropo.init = function () {
    // add event listeners to all of the top-level nav menus
    var topnavs = DOM.getElementsByClassName($('menu'), "topnav");
    topnavs.forEach(function (topnav) {
        DOM.addEventListener(topnav, "mouseover", function (evt) { Tropo.showSubNav(topnav.id) });
        DOM.addEventListener(topnav, "mouseout", function (evt) { Tropo.hideSubNav() });
    });
}

Tropo.hideSubNav = function () {
    var topnavs = DOM.getElementsByClassName($('menu'), "topnav");
    var subnavs = DOM.getElementsByClassName($('menu'), "subnav");
    topnavs.forEach(function (topnav) {
        DOM.removeClassName(topnav, "hover");
    });
    subnavs.forEach(function (subnav) {
        DOM.removeClassName(subnav, "hover");
    });
}

Tropo.showSubNav = function (id) {
    Tropo.hideSubNav();

    if (!$(id)) return;
    DOM.addClassName($(id), "hover");
}

LiveJournal.register_hook("page_load", Tropo.init);
