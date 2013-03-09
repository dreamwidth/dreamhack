// Set up two different ways to test if the page is loaded yet.
// The proper way is using DOMContentLoaded, but only Mozilla supports it.
{
    // Others
    DOM.addEventListener(window, "load", LiveJournal.initPage);

    // Mozilla
    DOM.addEventListener(window, "DOMContentLoaded", LiveJournal.initPage);
}
